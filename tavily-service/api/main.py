#!/usr/bin/env python3
"""
Tavily-Style Search API
Combines SearXNG (search) + Crawl4AI (content extraction)
"""

import os
import json
import asyncio
import httpx
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse, MarkdownResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Tavily-Style Search API", version="1.0.0")

# Configuration
SEARXNG_URL = os.getenv("SEARXNG_URL", "http://searxng:8080")
CRAWL4AI_URL = os.getenv("CRAWL4AI_URL", "http://crawl4ai:8000")
API_KEY = os.getenv("API_KEY", "change-this-secret-key")


class SearchRequest(BaseModel):
    query: str
    max_results: int = 5
    crawl_content: bool = True


class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    content: Optional[str] = None
    engine: str = "unknown"


class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total_results: int
    timestamp: str
    markdown: str


async def search_searxng(query: str, max_results: int = 10) -> List[Dict]:
    """Search using SearXNG"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{SEARXNG_URL}/search",
                params={
                    "q": query,
                    "format": "json",
                    "engines": "brave,mwmbl,duckduckgo",
                    "limit": max_results
                }
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("results", [])
            else:
                print(f"SearXNG error: {response.status_code}")
                return []
    except Exception as e:
        print(f"SearXNG request failed: {e}")
        return []


async def crawl_url(url: str) -> Optional[str]:
    """Crawl a URL using Crawl4AI"""
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{CRAWL4AI_URL}/crawl",
                json={
                    "urls": [url],
                    "exclude": ["*.pdf", "*.jpg", "*.png"],
                    "priority": 1
                }
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("results"):
                    return data["results"][0].get("markdown", "")
            return None
    except Exception as e:
        print(f"Crawl4AI request failed: {e}")
        return None


def generate_markdown(query: str, results: List[SearchResult]) -> str:
    """Generate markdown formatted results"""
    md = f"# Search Results: {query}\n\n"
    md += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n---\n\n"
    
    for i, result in enumerate(results, 1):
        md += f"## {i}. {result.title}\n\n"
        md += f"**URL**: {result.url}\n\n"
        md += f"**Source**: {result.engine}\n\n"
        md += f"**Snippet**:\n> {result.snippet}\n\n"
        
        if result.content:
            md += f"**Content** (first 2000 chars):\n\n"
            md += result.content[:2000]
            if len(result.content) > 2000:
                md += "\n\n*... (truncated)*\n"
        
        md += "\n---\n\n"
    
    return md


@app.get("/")
async def root():
    return {
        "service": "Tavily-Style Search API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "search": "/search?q=your query",
            "search_json": "/search/json?q=your query",
            "search_markdown": "/search/markdown?q=your query",
            "health": "/health"
        }
    }


@app.get("/health")
async def health():
    """Health check"""
    status = {"searxng": False, "crawl4ai": False}
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(f"{SEARXNG_URL}/healthz")
            status["searxng"] = r.status_code == 200
    except:
        pass
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(f"{CRAWL4AI_URL}/health")
            status["crawl4ai"] = r.status_code == 200
    except:
        pass
    
    return {"status": "healthy" if all(status.values()) else "degraded", "services": status}


@app.get("/search")
async def search(
    q: str = Query(..., description="Search query"),
    max_results: int = Query(5, ge=1, le=20, description="Maximum number of results"),
    crawl: bool = Query(True, description="Crawl content from results"),
    format: str = Query("json", regex="^(json|markdown)$", description="Output format")
):
    """Main search endpoint - returns JSON by default"""
    if not q:
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required")
    
    # Search using SearXNG
    raw_results = await search_searxng(q, max_results * 2)
    
    # Process results
    results = []
    seen_urls = set()
    
    for item in raw_results[:max_results]:
        url = item.get("url", "")
        if url in seen_urls or not url:
            continue
        seen_urls.add(url)
        
        result = SearchResult(
            title=item.get("title", "Untitled"),
            url=url,
            snippet=item.get("content", "")[:500],
            engine=item.get("engine", "unknown")
        )
        results.append(result)
    
    # Optionally crawl content
    if crawl:
        for result in results[:3]:  # Crawl top 3
            content = await crawl_url(result.url)
            if content:
                result.content = content
    
    # Generate markdown
    markdown = generate_markdown(q, results)
    
    # Return based on format
    response = {
        "query": q,
        "results": [r.model_dump() for r in results],
        "total_results": len(results),
        "timestamp": datetime.now().isoformat()
    }
    
    if format == "markdown":
        return MarkdownResponse(content=markdown)
    
    return JSONResponse(content=response)


@app.get("/search/json")
async def search_json(
    q: str = Query(...),
    max_results: int = Query(5, ge=1, le=20),
    crawl: bool = Query(True)
):
    """Search endpoint that always returns JSON"""
    # Reuse the main search logic
    raw_results = await search_searxng(q, max_results * 2)
    
    results = []
    seen_urls = set()
    
    for item in raw_results[:max_results]:
        url = item.get("url", "")
        if url in seen_urls or not url:
            continue
        seen_urls.add(url)
        
        result = SearchResult(
            title=item.get("title", "Untitled"),
            url=url,
            snippet=item.get("content", "")[:500],
            engine=item.get("engine", "unknown")
        )
        results.append(result)
    
    if crawl:
        for result in results[:3]:
            content = await crawl_url(result.url)
            if content:
                result.content = content
    
    return {
        "query": q,
        "results": [r.model_dump() for r in results],
        "total_results": len(results),
        "timestamp": datetime.now().isoformat()
    }


@app.get("/search/markdown")
async def search_markdown(
    q: str = Query(...),
    max_results: int = Query(5, ge=1, le=20),
    crawl: bool = Query(True)
):
    """Search endpoint that always returns Markdown"""
    raw_results = await search_searxng(q, max_results * 2)
    
    results = []
    seen_urls = set()
    
    for item in raw_results[:max_results]:
        url = item.get("url", "")
        if url in seen_urls or not url:
            continue
        seen_urls.add(url)
        
        result = SearchResult(
            title=item.get("title", "Untitled"),
            url=url,
            snippet=item.get("content", "")[:500],
            engine=item.get("engine", "unknown")
        )
        results.append(result)
    
    if crawl:
        for result in results[:3]:
            content = await crawl_url(result.url)
            if content:
                result.content = content
    
    markdown = generate_markdown(q, results)
    return MarkdownResponse(content=markdown)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "3000"))
    uvicorn.run(app, host="0.0.0.0", port=port)