# xapi MCP 配置指南

## MCP端点

```
https://mcp.xapi.to/mcp?apikey=sk-13f1579ac8ee0810246ea4b0a4239b52bd2de6dcae251a53
```

## 安装mcporter

```bash
npm install -g mcporter
```

## 添加xapi MCP

```bash
mcporter add xapi --url "https://mcp.xapi.to/mcp?apikey=sk-13f1579ac8ee0810246ea4b0a4239b52bd2de6dcae251a53"
```

## 或者手动配置

对于Cursor:
添加到 ~/.cursor/mcp.json:

```json
{
  "mcpServers": {
    "xapi": {
      "url": "https://mcp.xapi.to/mcp?apikey=sk-13f1579ac8ee0810246ea4b0a4239b52bd2de6dcae251a53"
    }
  }
}
```

对于VS Code:
添加到 ~/.vscode/mcp.json:

```json
{
  "mcpServers": {
    "xapi": {
      "url": "https://mcp.xapi.to/mcp?apikey=sk-13f1579ac8ee0810246ea4b0a4239b52bd2de6dcae251a53"
    }
  }
}
```

