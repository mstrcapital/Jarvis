# Personal Knowledge Base

This directory contains the ingested knowledge from URLs.

## Structure

```
knowledge-base/
├── index.json          # Main index with metadata
├── content/           # Raw content files
│   └── YYYY-MM-DD/    # Organized by date
└── embeddings/        # (Future) Vector embeddings
```

## Usage

### Ingest URL
When user drops a URL, use `web_fetch` to get content and save it here.

### Search
Search through the index to find relevant content.
