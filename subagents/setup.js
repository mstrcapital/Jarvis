#!/usr/bin/env node
/**
 * Sub-Agent System Setup Script
 */

const fs = require('fs');
const path = require('path');

class SubAgentSetup {
    constructor() {
        this.basePath = '/root/.openclaw/workspace/subagents';
        this.configPath = path.join(this.basePath, 'config');
    }
    
    setup() {
        console.log('\n' + '='.repeat(60));
        console.log('  OpenClaw Sub-Agent System Setup');
        console.log('='.repeat(60));
        
        // Create directories
        fs.mkdirSync(this.configPath, { recursive: true });
        
        // Create 1M context config
        console.log('\n📦 Creating 1M context config...');
        const contextConfig = `# OpenClaw Configuration - 1M Context Enabled
models:
  anthropic:
    params:
      context1m: true
agents:
  default:
    params:
      context1m: true
subagents:
  enabled: true
  max_subagents: 8
`;
        fs.writeFileSync(path.join(this.basePath, '1m_context_config.yaml'), contextConfig);
        console.log('   ✅ 1m_context_config.yaml');
        
        // Create 8 agent configs
        console.log('\n📦 Creating 8 AI employee configs...');
        const agents = [
            { name: 'xiao_o', cn: '小O', role: '私人管家', memory: '512MB', schedule: '08:00, 22:00' },
            { name: 'xiao_hai', cn: '小海', role: '出海研究', memory: '512MB', schedule: '09:00, every 4h' },
            { name: 'xiao_c', cn: '小C', role: '内容运营', memory: '512MB', schedule: '10:00, 14:00, 18:00' },
            { name: 'xiao_long', cn: '小龙', role: '社区管理', memory: '256MB', schedule: '24h' },
            { name: 'xiao_tuan', cn: '小团', role: '团队管理', memory: '256MB', schedule: '08:30, hourly' },
            { name: 'xiao_fruit', cn: '小果', role: 'iOS开发', memory: '512MB', schedule: '09:30, as_needed' },
            { name: 'xiao_fa', cn: '小法', role: '法律顾问', memory: '256MB', schedule: '08:00, weekly' },
            { name: 'xiao_hei', cn: '小黑', role: '黑科技情报', memory: '512MB', schedule: '09:00, 15:00' }
        ];
        
        for (const agent of agents) {
            const config = `subagent:
  id: "${agent.name}"
  name: "${agent.cn}"
  role: "${agent.role}"
memory:
  limit: "${agent.memory}"
  isolation: true
schedule:
  - "${agent.schedule}"
capabilities:
  - task_coordination
  - progress_tracking
`;
            fs.writeFileSync(path.join(this.configPath, `${agent.name}.yaml`), config);
            console.log(`   ✅ ${agent.name}.yaml (${agent.cn} - ${agent.role})`);
        }
        
        // Create startup script
        console.log('\n📦 Creating startup script...');
        const startupScript = `#!/bin/bash
echo "🚀 启动8个AI员工系统"
echo "======================================"
echo "📦 启动小O (管家)..."
openclaw subagents start xiao_o --daemon
sleep 3
for agent in xiao_hai xiao_c xiao_long xiao_tuan xiao_fruit xiao_fa xiao_hei; do
    echo "📦 启动${agent}..."
    openclaw subagents start $agent --daemon
    sleep 2
done
echo ""
echo "✅ 8个AI员工已启动!"
echo "📊 内存占用: ~3GB"
`;
        fs.writeFileSync(path.join(this.basePath, 'start_all.sh'), startupScript);
        fs.chmodSync(path.join(this.basePath, 'start_all.sh'), '755');
        console.log('   ✅ start_all.sh');
        
        // Create monitor script
        console.log('\n📦 Creating monitor script...');
        const monitorScript = `#!/bin/bash
echo "📊 OpenClaw Sub-Agent Monitor"
echo "======================================"
echo ""
echo "📦 子Agent状态:"
openclaw subagents status
echo ""
echo "💾 资源占用:"
openclaw subagents resources
echo ""
echo "🏥 健康检查:"
openclaw subagents health
`;
        fs.writeFileSync(path.join(this.basePath, 'monitor.sh'), monitorScript);
        fs.chmodSync(path.join(this.basePath, 'monitor.sh'), '755');
        console.log('   ✅ monitor.sh');
        
        // Create report
        const report = {
            generatedAt: new Date().toISOString(),
            agents: agents.map(a => ({ name: a.name, cn: a.cn, role: a.role, memory: a.memory })),
            totalMemory: '3GB',
            totalAgents: 8
        };
        fs.writeFileSync(path.join(this.basePath, 'setup_report.json'), JSON.stringify(report, null, 2));
        
        console.log('\n' + '='.repeat(60));
        console.log('  ✅ Setup Complete!');
        console.log('='.repeat(60));
        console.log(`\n📁 Files created in: ${this.basePath}`);
        console.log(`📊 Total agents: 8`);
        console.log(`💾 Total memory: 3GB`);
    }
}

new SubAgentSetup().setup();
