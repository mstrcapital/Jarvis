# Tavily-Style Search Skill

## Overview

This skill provides Tavily-like search functionality for the AI agent. It combines web search with content extraction to provide comprehensive research results.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│              Tavily-Style Search API                 │
├─────────────────────────────────────────────────────┤
│  Search Layer:                                       │
│  - Primary: Brave Search (via SearXNG)              │
│  - Backup: DuckDuckGo                               │
│                                                     │
│  Content Extraction:                                │
│  - x-reader for content fetching                    │
│  - Scrapling for advanced parsing                   │
│                                                     │
│  Output: JSON + Markdown                            │
└─────────────────────────────────────────────────────┘
```

## Usage

### Basic Search

To search for information, use the following endpoints:

- **JSON**: `http://localhost:8888/search?q=YOUR_QUERY&format=json`
- **Web Interface**: `http://localhost:8888`

### Via Agent Tool

When you need to search for information:

1. **Use web_search tool** (Brave API) for quick results
2. **Use web_fetch** for detailed content from specific URLs
3. **Use x-reader** for fetching content from Chinese platforms (WeChat, Bilibili, etc.)
4. **Use scrapling** for anti-scraping protected sites

## Configuration

### Service URLs

| Service | URL | Purpose |
|---------|-----|---------|
| SearXNG | http://localhost:8888 | Meta search engine |
| x-reader | CLI tool | Content fetching |
| scrapling | Python library | Advanced parsing |

### Environment Variables

```
SEARXNG_URL=http://localhost:8888
```

## Available Engines

The search service uses these engines (in priority order):

1. **Brave** - Privacy-focused search
2. **DuckDuckGo** - Alternative search
3. **Google** - Full search coverage (if enabled)

## Notes

- SearXNG runs in Docker on port 8888
- For production, add authentication
- x-reader is pre-installed for content extraction
- scrapling is available for advanced web scraping

---

*This skill provides research capabilities for the AI agent.*