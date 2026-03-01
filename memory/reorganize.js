#!/usr/bin/env node
/**
 * Memory Reorganization Script
 * 
 * Convert existing flat memories to hierarchical structure
 */

const fs = require('fs');
const path = require('path');

const OLD_FILES = [
    { 
        old: '/root/.openclaw/workspace/MEMORY.md', 
        key: 'long_term_memory', 
        domain: 'long_term' 
    },
    { 
        old: '/root/.openclaw/workspace/IDENTITY.md', 
        key: 'agent_identity', 
        domain: 'user_context' 
    },
    { 
        old: '/root/.openclaw/workspace/SOUL.md', 
        key: 'agent_soul', 
        domain: 'user_context' 
    },
    {
        old: '/root/.openclaw/workspace/USER.md',
        key: 'user_marco',
        domain: 'user_context'
    },
    {
        old: '/root/.openclaw/workspace/AGENTS.md',
        key: 'workspace_agents',
        domain: 'project_memory'
    },
    {
        old: '/root/.openclaw/workspace/HEARTBEAT.md',
        key: 'heartbeat_config',
        domain: 'project_memory'
    },
    {
        old: '/root/.openclaw/workspace/TOOLS.md',
        key: 'local_tools',
        domain: 'skills_index'
    }
];

class MemoryReorganizer {
    constructor() {
        this.basePath = '/root/.openclaw/workspace/memory';
        this.initStructure();
    }
    
    initStructure() {
        const domains = ['user_context', 'project_memory', 'skills_index', 'long_term'];
        
        for (const layer of ['L0_Domains', 'L1_Files', 'L2_Content']) {
            for (const domain of domains) {
                const dirPath = path.join(this.basePath, layer, domain);
                fs.mkdirSync(dirPath, { recursive: true });
            }
        }
        
        // Skills subdirectory
        fs.mkdirSync(path.join(this.basePath, 'L1_Files', 'skills'), { recursive: true });
        fs.mkdirSync(path.join(this.basePath, 'L2_Content', 'skills'), { recursive: true });
        
        console.log('✅ Directory structure initialized');
    }
    
    async reorganize() {
        console.log('\n' + '='*60);
        console.log('  Memory Reorganization');
        console.log('='*60);
        console.log('');
        
        const results = [];
        
        for (const file of OLD_FILES) {
            if (fs.existsSync(file.old)) {
                console.log(`📦 Processing: ${file.old}`);
                
                const content = fs.readFileSync(file.old, 'utf-8');
                const stats = fs.statSync(file.old);
                
                // Create hierarchical structure
                const domainPath = path.join(this.basePath, 'L0_Domains', file.domain);
                const filesPath = path.join(this.basePath, 'L1_Files', file.domain);
                const chunksPath = path.join(this.basePath, 'L2_Content', file.domain);
                
                // Generate abstract (L0)
                const abstract = this.generateAbstract(content);
                fs.writeFileSync(
                    path.join(domainPath, `${file.key}_abstract.md`),
                    this.formatAbstract(file.key, abstract, file.domain, content)
                );
                
                // Generate outline (L1)
                const outline = this.generateOutline(content);
                fs.writeFileSync(
                    path.join(filesPath, `${file.key}_outline.md`),
                    this.formatOutline(file.key, outline, file.domain, content)
                );
                
                // Generate chunks (L2)
                const chunks = this.chunkContent(content);
                chunks.forEach((chunk, i) => {
                    fs.writeFileSync(
                        path.join(chunksPath, `${file.key}_chunk_${i}.md`),
                        this.formatChunk(file.key, i, chunk, file.domain, content)
                    );
                });
                
                const result = {
                    file: file.old,
                    key: file.key,
                    domain: file.domain,
                    chunks: chunks.length,
                    size: content.length
                };
                
                results.push(result);
                
                console.log(`   ✅ ${file.key} → ${file.domain} (${chunks.length} chunks)`);
            } else {
                console.log(`   ⏭️  Skipped: ${file.old} (not found)`);
            }
        }
        
        // Update domain indices
        this.updateIndices(results);
        
        // Generate summary
        this.generateSummary(results);
        
        return results;
    }
    
    generateAbstract(content) {
        const lines = content.split('\n').filter(l => l.trim() && !l.startsWith('//'));
        return lines.slice(0, 5).join('\n').substring(0, 500);
    }
    
    generateOutline(content) {
        const headers = content.split('\n')
            .filter(l => l.startsWith('#'))
            .join('\n');
        return (headers + '\n\n' + content.substring(0, 1500)).substring(0, 2000);
    }
    
    chunkContent(content, chunkSize = 1500) {
        const chunks = [];
        const lines = content.split('\n');
        let currentChunk = '';
        
        for (const line of lines) {
            if (currentChunk.length + line.length > chunkSize) {
                if (currentChunk) chunks.push(currentChunk.trim());
                currentChunk = line;
            } else {
                currentChunk += '\n' + line;
            }
        }
        if (currentChunk) chunks.push(currentChunk.trim());
        
        return chunks;
    }
    
    formatAbstract(key, abstract, domain, fullContent) {
        return `# Abstract: ${key}\n\n${abstract}\n\n---\n*Domain: ${domain} | Type: Long-term Memory*`;
    }
    
    formatOutline(key, outline, domain, fullContent) {
        return `# Outline: ${key}\n\n${outline}\n\n---\n*Domain: ${domain} | Type: File Index*`;
    }
    
    formatChunk(key, index, chunk, domain, fullContent) {
        return `# Chunk ${index}: ${key}\n\n${chunk}\n\n---\n*Domain: ${domain} | Chunk: ${index}*`;
    }
    
    updateIndices(results) {
        for (const domain of ['user_context', 'project_memory', 'skills_index', 'long_term']) {
            const domainFiles = results.filter(r => r.domain === domain);
            
            if (domainFiles.length > 0) {
                const indexPath = path.join(this.basePath, 'L0_Domains', domain, 'index.md');
                
                let index = `# ${domain.charAt(0).toUpperCase() + domain.slice(1).replace('_', ' ')} Index\n\n`;
                index += `*Generated: ${new Date().toISOString()}*\n\n`;
                index += `## Files\n\n`;
                
                for (const f of domainFiles) {
                    index += `- **${f.key}**: ${f.chunks} chunks (${f.size} bytes)\n`;
                }
                
                fs.writeFileSync(indexPath, index);
            }
        }
    }
    
    generateSummary(results) {
        const summary = {
            timestamp: new Date().toISOString(),
            totalFiles: results.length,
            totalChunks: results.reduce((sum, r) => sum + r.chunks, 0),
            byDomain: {}
        };
        
        for (const r of results) {
            if (!summary.byDomain[r.domain]) {
                summary.byDomain[r.domain] = { files: 0, chunks: 0 };
            }
            summary.byDomain[r.domain].files++;
            summary.byDomain[r.domain].chunks += r.chunks;
        }
        
        const summaryPath = path.join(this.basePath, 'REORGANIZATION_SUMMARY.json');
        fs.writeFileSync(summaryPath, JSON.stringify(summary, null, 2));
        
        console.log('\n' + '='*60);
        console.log('  Reorganization Complete');
        console.log('='*60);
        console.log('');
        console.log(`📊 Summary:`);
        console.log(`   Total files: ${summary.totalFiles}`);
        console.log(`   Total chunks: ${summary.totalChunks}`);
        console.log('');
        console.log('📁 By Domain:');
        for (const [domain, data] of Object.entries(summary.byDomain)) {
            console.log(`   ${domain}: ${data.files} files, ${data.chunks} chunks`);
        }
        console.log('');
        console.log(`✅ Summary saved: ${summaryPath}`);
    }
}

async function main() {
    const reorganizer = new MemoryReorganizer();
    const results = await reorganizer.reorganize();
}

main().catch(console.error);
