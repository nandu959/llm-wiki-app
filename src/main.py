import utils.llm_client as llm_client
import utils.md_generator as md_generator
import utils.file_manager as file_manager
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
WIKI_DIR = BASE_DIR / "wiki"

SCHEMA_PATH = WIKI_DIR / "schema.md"
LOG_PATH = WIKI_DIR / "log.md"
AUDIT_PATH = WIKI_DIR / "audit.md"
RAW_PATH = WIKI_DIR / "raw"

OUTPUT_FILES = {
    "index": WIKI_DIR / "index.md",
}

def run_initial_build():
    schema = file_manager.read_text(SCHEMA_PATH)
    generate_index_page(schema)
    generate_audit_report(schema)

    append_log(
        "- Ran initial build.\n"
        "- Generated concept pages for LLM Wiki, RAG, Memex, and Personal Knowledge Management.\n"
        "- Generated comparison page: RAG vs LLM Wiki.\n"
        "- Generated index page."
    )

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
    file_manager.write_text(OUTPUT_FILES["index"], content)


def generate_audit_report(schema: str) -> None:
    system_prompt = build_system_prompt(schema)

    pages = []
    for path in sorted(WIKI_DIR.rglob("*.md")):
        if path.name != "schema.md":
            pages.append(f"\n\n# FILE: {path.relative_to(WIKI_DIR)}\n\n")
            pages.append(file_manager.read_text(path))

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
    file_manager.write_text(AUDIT_PATH, audit)


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

def update_existing_page(
    page_path: Path,
    new_source_context: str,
    schema: str,
) -> None:
    existing_page = file_manager.read_text(page_path)
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
    file_manager.write_text(page_path, updated_content)



# ------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------

def append_log(message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    existing = LOG_PATH.read_text(encoding="utf-8") if LOG_PATH.exists() else "# Log\n"
    updated = existing.rstrip() + f"\n\n## {timestamp}\n\n{message.strip()}\n"
    LOG_PATH.write_text(updated, encoding="utf-8")


def main():
    print("Hello from llm-wiki-app!")
    run_initial_build()


if __name__ == "__main__":
    main()
