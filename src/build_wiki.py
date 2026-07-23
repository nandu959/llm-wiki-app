from pathlib import Path
import os
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI

import utils.llm_client as llm_client
import utils.md_generator as md_generator


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

load_dotenv()

#MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
MODEL = os.getenv("OLLAMA_MODEL", "gemma4:latest")


BASE_DIR = Path(__file__).resolve().parent
WIKI_DIR = BASE_DIR / "wiki"

SCHEMA_PATH = WIKI_DIR / "schema.md"
LOG_PATH = WIKI_DIR / "log.md"
AUDIT_PATH = WIKI_DIR / "audit.md"

SOURCE_FILES = {
    "karpathy": WIKI_DIR / "sources" / "karpathy-llm-wiki.md",
    "rag": WIKI_DIR / "sources" / "rag-paper.md",
    "memex": WIKI_DIR / "sources" / "as-we-may-think.md",
    "obsidian": WIKI_DIR / "sources" / "obsidian-graph-view.md",
}

OUTPUT_FILES = {
    "llm_wiki": WIKI_DIR / "concepts" / "llm-wiki.md",
    "rag": WIKI_DIR / "concepts" / "retrieval-augmented-generation.md",
    "memex": WIKI_DIR / "concepts" / "memex.md",
    "pkm": WIKI_DIR / "concepts" / "personal-knowledge-management.md",
    "comparison": WIKI_DIR / "comparisons" / "rag-vs-llm-wiki.md",
    "index": WIKI_DIR / "index.md",
}

# ------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------

def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def append_log(message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    existing = LOG_PATH.read_text(encoding="utf-8") if LOG_PATH.exists() else "# Log\n"
    updated = existing.rstrip() + f"\n\n## {timestamp}\n\n{message.strip()}\n"
    LOG_PATH.write_text(updated, encoding="utf-8")


# ------------------------------------------------------------
# Prompt builders
# ------------------------------------------------------------

def build_system_prompt(schema: str) -> str:
    return f"""
You are maintaining a small Markdown-based LLM Wiki.

Follow this schema exactly:

{schema}

Return only valid Markdown.
Do not include explanations outside the Markdown page.
Do not invent sources.
If a claim is interpretive, label it as interpretation.
Use wikilinks for internal wiki links, for example [[LLM Wiki]].
"""


def generate_concept_page(
    title: str,
    output_path: Path,
    source_context: str,
    schema: str,
) -> None:
    system_prompt = build_system_prompt(schema)

    user_prompt = f"""
Create a concept page for the LLM Wiki.

Page title:
{title}

Use the following source context:

{source_context}

The page should include:
- A clear definition
- Why the concept matters
- Key points
- Related pages using wikilinks
- A short "Source basis" section explaining which source notes support the page

Return only the Markdown page.
"""

    content = llm_client.call_llm(system_prompt, user_prompt)
    write_text(output_path, content)


def generate_comparison_page(
    output_path: Path,
    schema: str,
    source_context: str,
) -> None:
    system_prompt = build_system_prompt(schema)

    user_prompt = f"""
Create a comparison page for the LLM Wiki.

Topic:
RAG vs LLM Wiki

Use the following source context:

{source_context}

The page should include:
- A short summary
- A comparison table
- When to use RAG
- When to use LLM Wiki
- How the two can be combined
- A section called "Maintenance dimension"
- Related pages using wikilinks
- A "Source basis" section

Return only the Markdown page.
"""

    content = llm_client.call_llm(system_prompt, user_prompt)
    write_text(output_path, content)


def update_existing_page(
    page_path: Path,
    new_source_context: str,
    schema: str,
) -> None:
    existing_page = read_text(page_path)
    system_prompt = build_system_prompt(schema)

    user_prompt = f"""
Update the following existing wiki page using the new source context.

Existing page:
{existing_page}

New source context:
{new_source_context}

Rules:
- Preserve useful existing content.
- Add new information only if it improves the page.
- Do not duplicate sections.
- Add or update wikilinks if needed.
- Mark uncertainty where appropriate.
- If the new source changes or qualifies an existing claim, update the wording.
- Return the full updated Markdown page.
"""

    updated_content = llm_client.call_llm(system_prompt, user_prompt)
    write_text(page_path, updated_content)


def generate_index_page(schema: str) -> None:
    system_prompt = build_system_prompt(schema)

    page_list = []
    for path in sorted(WIKI_DIR.rglob("*.md")):
        if path.name not in {"schema.md"}:
            page_list.append(str(path.relative_to(WIKI_DIR)))

    user_prompt = f"""
Create an index page for the LLM Wiki.

The wiki currently contains these files:

{chr(10).join(page_list)}

The page should link to:
- Source pages
- Concept pages
- Comparison pages
- People pages if relevant
- Maintenance pages

Use wikilinks where possible.
Return only the Markdown page.
"""

    content = llm_client.call_llm(system_prompt, user_prompt)
    write_text(OUTPUT_FILES["index"], content)


def generate_audit_report(schema: str) -> None:
    system_prompt = build_system_prompt(schema)

    pages = []
    for path in sorted(WIKI_DIR.rglob("*.md")):
        if path.name != "schema.md":
            pages.append(f"\n\n# FILE: {path.relative_to(WIKI_DIR)}\n\n")
            pages.append(read_text(path))

    user_prompt = f"""
Review the following wiki files.

Identify:
- possible orphan pages;
- possible contradictions;
- stale or unsupported claims;
- missing links;
- duplicate concepts;
- pages that should be updated after new sources are added.

Return a Markdown audit report.
Do not fix the files directly.

Wiki content:
{''.join(pages)}
"""

    audit = llm_client.call_llm(system_prompt, user_prompt)
    write_text(AUDIT_PATH, audit)


# ------------------------------------------------------------
# Build workflows
# ------------------------------------------------------------

def run_initial_build() -> None:
    schema = read_text(SCHEMA_PATH)

    karpathy_note = read_text(SOURCE_FILES["karpathy"])
    rag_note = read_text(SOURCE_FILES["rag"])
    memex_note = read_text(SOURCE_FILES["memex"])

    all_sources = "\n\n---\n\n".join(
        [
            karpathy_note,
            rag_note,
            memex_note,
        ]
    )

    generate_concept_page(
        title="LLM Wiki",
        output_path=OUTPUT_FILES["llm_wiki"],
        source_context=karpathy_note,
        schema=schema,
    )

    generate_concept_page(
        title="Retrieval-Augmented Generation",
        output_path=OUTPUT_FILES["rag"],
        source_context=rag_note,
        schema=schema,
    )

    generate_concept_page(
        title="Memex",
        output_path=OUTPUT_FILES["memex"],
        source_context=memex_note,
        schema=schema,
    )

    generate_concept_page(
        title="Personal Knowledge Management",
        output_path=OUTPUT_FILES["pkm"],
        source_context=all_sources,
        schema=schema,
    )

    generate_comparison_page(
        output_path=OUTPUT_FILES["comparison"],
        schema=schema,
        source_context=all_sources,
    )

    generate_index_page(schema)
    generate_audit_report(schema)

    append_log(
        "- Ran initial build.\n"
        "- Generated concept pages for LLM Wiki, RAG, Memex, and Personal Knowledge Management.\n"
        "- Generated comparison page: RAG vs LLM Wiki.\n"
        "- Generated index page."
    )


def run_update_cycle() -> None:
    schema = read_text(SCHEMA_PATH)
    obsidian_note = read_text(SOURCE_FILES["obsidian"])

    update_existing_page(
        page_path=OUTPUT_FILES["llm_wiki"],
        new_source_context=obsidian_note,
        schema=schema,
    )

    update_existing_page(
        page_path=OUTPUT_FILES["pkm"],
        new_source_context=obsidian_note,
        schema=schema,
    )

    update_existing_page(
        page_path=OUTPUT_FILES["comparison"],
        new_source_context=obsidian_note,
        schema=schema,
    )

    generate_index_page(schema)
    generate_audit_report(schema)

    append_log(
        "- Added source note: Obsidian Graph View.\n"
        "- Updated LLM Wiki concept page.\n"
        "- Updated Personal Knowledge Management concept page.\n"
        "- Updated RAG vs LLM Wiki comparison page.\n"
        "- Regenerated index page.\n"
        "- Generated audit report."
    )


def main() -> None:
    run_initial_build()

    # Uncomment this after adding wiki/sources/obsidian-graph-view.md
    # run_update_cycle()

    print("LLM Wiki workflow complete.")


if __name__ == "__main__":
    main()