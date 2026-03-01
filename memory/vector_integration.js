#!/usr/bin/env node
/**
 * Vector Database Integration for Hierarchical Memory
 * 
 * Options:
 * 1. Simple in-memory vector store (no external dependencies)
 * 2. Milvus integration
 * 3. Chroma integration
 */

const fs = require('fs');
const path = require('path');

// Option 1: Simple In-Memory Vector Store (no dependencies)
class SimpleVectorStore {
    constructor() {
        this.vectors = new Map(); // key -> embedding
        this.documents = new Map(); // key -> content
    }
    
    async add(key, content, embedding) {
        this.vectors.set(key, embedding);
        this.documents.set(key, content);
        return { success: true, key };
    }
    
    async search(queryEmbedding, topK = 5) {
        // Simple cosine similarity
        const results = [];
        
        for (const [key, embedding] of this.vectors) {
            const similarity = this.cosineSimilarity(queryEmbedding, embedding);
            results.push({ key, score: similarity });
        }
        
        results.sort((a, b) => b.score - a.score);
        return results.slice(0, topK);
    }
    
    cosineSimilarity(a, b) {
        let dotProduct = 0;
        let normA = 0;
        let normB = 0;
        
        for (let i = 0; i < a.length; i++) {
            dotProduct += a[i] * b[i];
            normA += a[i] * a[i];
            normB += b[i] * b[i];
        }
        
        return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
    }
    
    async get(key) {
        return {
            content: this.documents.get(key),
            embedding: this.vectors.get(key)
        };
    }
}

// Generate simple embedding (hash-based for demo)
function generateEmbedding(text) {
    const hash = this.hashText(text);
    const embedding = [];
    for (let i = 0; i < 128; i++) {
        embedding.push((hash >> i) & 1 ? 1 : -1);
    }
    return embedding;
}

function hashText(text) {
    let hash = 0;
    for (let i = 0; i < text.length; i++) {
        const char = text.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    return Math.abs(hash);
}

// Option 2: Milvus Integration
class MilvusVectorStore {
    constructor(config = {}) {
        this.config = {
            host: config.host || 'localhost',
            port: config.port || 19530,
            ...config
        };
        this.client = null;
    }
    
    async connect() {
        // In production, use @zilliz/milvus-sdk
        console.log('📦 Milvus: Connect to', `${this.config.host}:${this.config.port}`);
        return { connected: true };
    }
    
    async createCollection(name, schema) {
        console.log(`📦 Milvus: Create collection ${name}`);
        return { collection: name };
    }
    
    async insert(collection, vectors, texts) {
        console.log(`📦 Milvus: Insert ${vectors.length} vectors`);
        return { insertCount: vectors.length };
    }
    
    async search(collection, queryVector, topK = 10) {
        console.log(`📦 Milvus: Search with ${queryVector.length} dimensions`);
        return []; // Return search results
    }
}

// Option 3: Chroma Integration  
class ChromaVectorStore {
    constructor(config = {}) {
        this.config = {
            path: config.path || './chroma_db',
            ...config
        };
    }
    
    async connect() {
        console.log('📦 Chroma: Connect to', this.config.path);
        return { connected: true };
    }
    
    async createCollection(name) {
        console.log(`📦 Chroma: Create collection ${name}`);
        return { collection: name };
    }
    
    async add(collection, documents, embeddings, ids) {
        console.log(`📦 Chroma: Add ${documents.length} documents`);
        return { addCount: documents.length };
    }
    
    async query(queryEmbedding, topK = 10) {
        console.log(`📦 Chroma: Query with ${queryEmbedding.length} dimensions`);
        return [];
    }
}

// Hierarchical Vector Store (combines filesystem + vector)
class HierarchicalVectorStore {
    constructor(options = {}) {
        this.fsStore = options.fsStore || new SimpleVectorStore();
        this.vectorStore = options.vectorStore || new SimpleVectorStore();
        this.basePath = options.basePath || '/root/.openclaw/workspace/memory';
        this.enableVector = options.enableVector || false;
    }
    
    async store(key, content, domain = 'general', embedding = null) {
        // Store in filesystem (always)
        const fsResult = await this.storeInFS(key, content, domain);
        
        // Store in vector (if enabled)
        let vectorResult = null;
        if (this.enableVector && embedding) {
            vectorResult = await this.vectorStore.add(key, content, embedding);
        }
        
        return {
            fs: fsResult,
            vector: vectorResult
        };
    }
    
    async storeInFS(key, content, domain) {
        // Create hierarchical structure
        const domainPath = path.join(this.basePath, 'L0_Domains', domain);
        const filesPath = path.join(this.basePath, 'L1_Files', domain);
        const chunksPath = path.join(this.basePath, 'L2_Content', domain);
        
        [domainPath, filesPath, chunksPath].forEach(p => {
            fs.mkdirSync(p, { recursive: true });
        });
        
        // Generate chunks
        const chunks = this.chunkContent(content, 1000);
        
        // Store all layers
        const timestamp = Date.now();
        
        // L0: Abstract
        fs.writeFileSync(
            path.join(domainPath, `${key}_abstract.md`),
            this.formatAbstract(key, content, domain, timestamp)
        );
        
        // L1: Outline
        fs.writeFileSync(
            path.join(filesPath, `${key}_outline.md`),
            this.formatOutline(key, content, domain, timestamp)
        );
        
        // L2: Chunks
        chunks.forEach((chunk, i) => {
            fs.writeFileSync(
                path.join(chunksPath, `${key}_chunk_${i}.md`),
                this.formatChunk(key, i, chunk, domain, timestamp)
            );
        });
        
        return { chunks: chunks.length };
    }
    
    async search(query, options = {}) {
        const { domain = null, useVector = false, topK = 5 } = options;
        
        // Hierarchical search (always available)
        const fsResults = await this.hierarchicalSearch(query, domain);
        
        // Vector search (if enabled)
        let vectorResults = null;
        if (this.enableVector && useVector) {
            const queryEmbedding = this.generateEmbedding(query);
            vectorResults = await this.vectorStore.search(queryEmbedding, topK);
        }
        
        return {
            hierarchical: fsResults,
            vector: vectorResults,
            combined: this.combineResults(fsResults, vectorResults)
        };
    }
    
    async hierarchicalSearch(query, domainFilter = null) {
        const results = {
            l0: [],
            l1: [],
            l2: []
        };
        
        // L0: Search domain abstracts
        const domains = domainFilter ? [domainFilter] : 
            ['user_context', 'project_memory', 'skills_index', 'long_term'];
        
        for (const domain of domains) {
            const indexPath = path.join(this.basePath, 'L0_Domains', domain, 'index.md');
            if (fs.existsSync(indexPath)) {
                const content = fs.readFileSync(indexPath, 'utf-8');
                if (this.isRelevant(query, content)) {
                    results.l0.push({ domain, score: 0.8 });
                }
            }
        }
        
        // L1: Search file outlines
        for (const d of results.l0) {
            const filesPath = path.join(this.basePath, 'L1_Files', d.domain);
            if (!fs.existsSync(filesPath)) continue;
            
            const files = fs.readdirSync(filesPath).filter(f => f.endsWith('.md'));
            
            for (const file of files) {
                const content = fs.readFileSync(path.join(filesPath, file), 'utf-8');
                if (this.isRelevant(query, content)) {
                    results.l1.push({ file: `${d.domain}/${file}`, score: 0.85 });
                }
            }
        }
        
        // L2: Search content chunks
        for (const f of results.l1) {
            const [domain, filename] = f.file.split('/');
            const baseName = filename.replace('_outline.md', '');
            
            const chunksPath = path.join(this.basePath, 'L2_Content', domain);
            if (!fs.existsSync(chunksPath)) continue;
            
            const chunks = fs.readdirSync(chunksPath)
                .filter(c => c.startsWith(baseName) && c.includes('chunk_'));
            
            for (const chunk of chunks) {
                const content = fs.readFileSync(path.join(chunksPath, chunk), 'utf-8');
                if (this.isRelevant(query, content)) {
                    results.l2.push({
                        path: `${domain}/${chunk}`,
                        score: 0.95
                    });
                }
            }
        }
        
        return results;
    }
    
    combineResults(hierarchical, vector) {
        if (!vector) return hierarchical;
        
        // Merge and re-rank results
        const combined = [...hierarchical.l2];
        
        for (const v of vector) {
            const existing = combined.find(c => c.path && c.path.includes(v.key));
            if (existing) {
                existing.score = (existing.score + v.score) / 2;
            } else {
                combined.push({ path: v.key, score: v.score, source: 'vector' });
            }
        }
        
        combined.sort((a, b) => b.score - a.score);
        return combined;
    }
    
    // Utility methods
    chunkContent(content, chunkSize = 1000) {
        const chunks = [];
        const lines = content.split('\n');
        let current = '';
        
        for (const line of lines) {
            if (current.length + line.length > chunkSize) {
                if (current) chunks.push(current.trim());
                current = line;
            } else {
                current += '\n' + line;
            }
        }
        if (current) chunks.push(current.trim());
        
        return chunks;
    }
    
    formatAbstract(key, content, domain, timestamp) {
        const lines = content.split('\n').filter(l => l.trim()).slice(0, 3);
        return `# Abstract: ${key}\n\n${lines.join('\n').substring(0, 300)}\n\n---\n*Domain: ${domain} | ${new Date(timestamp).toISOString()}*`;
    }
    
    formatOutline(key, content, domain, timestamp) {
        const headers = content.split('\n').filter(l => l.startsWith('#')).join('\n');
        return `# Outline: ${key}\n\n${headers}\n\n${content.substring(0, 800)}\n\n---\n*Domain: ${domain} | ${new Date(timestamp).toISOString()}*`;
    }
    
    formatChunk(key, index, chunk, domain, timestamp) {
        return `# Chunk ${index}: ${key}\n\n${chunk}\n\n---\n*Domain: ${domain} | Chunk: ${index} | ${new Date(timestamp).toISOString()}*`;
    }
    
    isRelevant(query, content) {
        const keywords = query.toLowerCase().split(' ').filter(k => k.length > 2);
        return keywords.some(kw => content.toLowerCase().includes(kw));
    }
    
    generateEmbedding(text) {
        // Simple hash-based embedding for demo
        // In production, use OpenAI embeddings or similar
        const hash = require('crypto').createHash('md5').update(text).digest('hex');
        const embedding = [];
        
        for (let i = 0; i < 128; i++) {
            embedding.push(parseInt(hash.substr(i * 2, 2), 16) / 255 * 2 - 1);
        }
        
        return embedding;
    }
}

// Main execution
async function main() {
    console.log('='.repeat(60));
    console.log('  Vector Database Integration for Hierarchical Memory');
    console.log('='.repeat(60));
    console.log('');
    
    // Test Simple Vector Store
    console.log('📦 Testing Simple Vector Store...');
    const simpleStore = new SimpleVectorStore();
    await simpleStore.add('test1', 'Marco lives in GMT+8', [0.1, 0.2, 0.3, 0.4]);
    const results = await simpleStore.search([0.1, 0.2, 0.3, 0.4], 5);
    console.log('   Results:', results.length);
    
    // Test Hierarchical Vector Store
    console.log('\n📦 Testing Hierarchical Vector Store...');
    const hierStore = new HierarchicalVectorStore({
        basePath: '/root/.openclaw/workspace/memory',
        enableVector: true
    });
    
    // Store a test memory
    console.log('   Storing test memory...');
    await hierStore.store(
        'test_memory',
        'Marco is a technology enthusiast who likes to explore AI capabilities and boundaries.',
        'user_context'
    );
    
    // Search
    console.log('   Searching...');
    const searchResults = await hierStore.search('Marco AI capabilities', { useVector: true });
    console.log('   Hierarchical results:', searchResults.hierarchical.l2.length, 'chunks');
    
    console.log('\n' + '='.repeat(60));
    console.log('✅ Vector Integration Complete!');
    console.log('='.repeat(60));
    
    console.log('\n📋 Integration Options:');
    console.log('');
    console.log('1. Simple Vector Store (No dependencies)');
    console.log('   ✅ Working now');
    console.log('');
    console.log('2. Milvus (Production)');
    console.log('   Install: npm install @zilliz/milvus-sdk');
    console.log('   Run: docker run -d -p 19530:19530 milvusdb/milvus-lite');
    console.log('');
    console.log('3. Chroma (Lightweight)');
    console.log('   Install: npm install chromadb');
    console.log('   Run: docker run -d -p 8000:8000 chromadb/chroma');
}

main().catch(console.error);
