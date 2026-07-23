# LLM Wiki App

A small Python app for generating and maintaining a Markdown-based wiki with the help of an LLM. The project reads source notes from the wiki source folder, prompts an LLM to draft or update pages, and writes the resulting content into the repository's wiki structure.

## What this app does

The app is designed to help you:

- build a lightweight wiki from source notes
- generate concept pages and comparison pages
- update existing pages when new source material is added
- create an audit report for content quality and link consistency

The main workflow lives in [src/build_wiki.py](src/build_wiki.py), and the LLM integration is handled in [src/utils/llm_client.py](src/utils/llm_client.py).

## Project structure

- `src/main.py` - entry point for the initial build workflow
- `src/build_wiki.py` - page generation and update workflow logic
- `src/utils/llm_client.py` - LLM request wrapper
- `src/utils/file_manager.py` - file read/write helpers
- `src/wiki/` - generated wiki content and source notes

## Requirements

- Python 3.11+
- An Ollama instance running locally, or an OpenAI-compatible endpoint
- Access to an LLM model such as `gemma4:latest` via Ollama

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install the project dependencies:

   ```bash
   pip install -e .
   ```

3. Configure environment variables in a `.env` file at the project root:

   ```env
   OLLAMA_API_KEY=ollama
   OLLAMA_HOST=http://127.0.0.1:11434
   OLLAMA_MODEL=gemma4:latest
   ```

   If you are using OpenAI instead of Ollama, you can also provide the standard OpenAI variables.

## Run the app

From the project root:

```bash
python src/main.py
```

This runs the initial wiki build and generates the Markdown content under `src/wiki/`.

## Build workflow

The app currently performs the following during the initial build:

- reads the schema from `src/wiki/schema.md`
- generates concept pages for LLM Wiki, RAG, Memex, and Personal Knowledge Management
- creates a comparison page for RAG vs LLM Wiki
- regenerates the wiki index
- writes an audit report

A second update cycle is available in the code and can be enabled by uncommenting the call in `main()`.

## Generated output

After running the script, the generated content is stored in:

- `src/wiki/index.md`
- `src/wiki/concepts/`
- `src/wiki/comparisons/`
- `src/wiki/audit.md`
- `src/wiki/log.md`

## Notes

- The app is intentionally lightweight and uses Markdown as its primary knowledge representation.
- It assumes the local Ollama-compatible endpoint is available at `http://127.0.0.1:11434/v1` unless you override it.
- If you add new source notes, you can extend the update workflow to refresh the wiki pages.

## License

See the repository's license file for usage terms.

## Graphify
```bash
graphify update .
```
```bash
graphify . --backend ollama --model gemma4:latest --embeddings
```
