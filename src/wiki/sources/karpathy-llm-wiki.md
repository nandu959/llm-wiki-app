# Source: Andrej Karpathy — LLM Wiki

## Source Type

GitHub Gist.

## Summary

Karpathy introduces LLM Wiki as an idea for using LLM agents to help build and maintain a personal Markdown knowledge base.

The idea file is designed to be copied into an LLM coding agent. The agent works with the user to build out the specifics.

The central idea is to maintain a persistent, human-readable wiki from raw sources rather than only retrieving raw chunks at query time.

The wiki acts as a compiled synthesis layer. Raw sources remain the ground truth, while the wiki stores organised concepts, summaries, links, indexes, and maintenance artefacts.

## Key Ideas

- The wiki is a persistent artefact, not a one-off answer.
- The knowledge base should compound as new sources are added.
- LLM agents can help maintain links, indexes, and logs.
- Maintenance includes detecting stale pages, contradictions, missing links, and orphan pages.
- Markdown is a natural format because both humans and coding agents can edit it.

## Related Concepts

- LLM Wiki
- RAG
- Personal knowledge management
- Coding agents
- Compiled knowledge