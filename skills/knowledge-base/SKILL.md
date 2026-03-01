---
name: knowledge-base
description: Personal Knowledge Base RAG - Save and search URLs semantically
---

# Knowledge Base Skill

## Overview

This skill enables a searchable knowledge base from saved URLs. Drop any URL → auto-ingest → semantic search later.

## What It Does

### 1. Ingestion Mode
When user drops a URL:
1. Use `web_fetch` to get content
2. Save to knowledge-base/index.json with metadata
3. Reply with confirmation (title, chunk count)

### 2. Query Mode  
When user asks a question:
1. Search the index.json for relevant matches
2. Return top results with sources and excerpts

## Files

- `knowledge-base/index.json` - Main index
- `knowledge-base/content/` - Raw content

## Usage

### Ingest
User: "Save this: https://example.com/article"

### Query
User: "What did I save about agent memory?"

## Dependencies

- `web_fetch` (built-in)
- Telegram or Slack channel for ingestion

---

*Simple RAG without vector embeddings - uses keyword/title matching*
