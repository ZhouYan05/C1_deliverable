---
source: https://developers.cloudflare.com/agents/guides/remote-mcp-server/
license: Cloudflare 官方文档，专有内容
tier: B
handling: 中文精读笔记（非逐段译文）
week: 2
---

# 精读笔记：构建远程 MCP 服务器（含认证与授权）

> 原文：Build a Remote MCP server · Cloudflare Agents docs
> ⚠️ 本笔记为**提炼与讲解**，非逐段译文。内容基于 Cloudflare Agents SDK，
>    但**认证授权的通用原则适用于任何 MCP 服务器**。
> 📌 抓取乱码说明：源文件中部分全角符号被转成 `Â·`、`â` 等乱码，已按语义还原。

## 一句话结论

远程 MCP 服务器有**两条路线**——**无认证公开**（任何人可连）vs
**带认证 + 作用域授权**（用户登录后，按权限控制智能体能调哪些工具）。
**Week 2 作业要求自定义 MCP 服务器，这篇是直接可用的实操手册。**

## 传输层

当前 MCP 规范标准为 **Streamable HTTP 传输**。

## 三种实现方式对比

Agents SDK 提供多种创建 MCP 服务器的方式：

| 方式 | 有状态？ | 需要 Durable Objects？ | 适用场景 |
|---|---|---|---|
| `createMcpHandler()` | 否 | 否 | **无状态工具**，最简配置 |
| `McpAgent` | 是 | 是 | 有状态工具、按会话状态、**请求 elicitation** |
| 原生 `WebStandardStreamableHTTPServerTransport` | 否 | 否 | **完全控制**，不依赖 SDK 封装 |

- `createMcpHandler()`：跑起无状态 MCP 服务器的最快方式
- `McpAgent`：每个会话一个 Durable Object，内置状态管理、elicitation 支持，
  同时支持 SSE 与 Streamable HTTP
- 原生传输：想直接用 `@modelcontextprotocol/sdk` 而不引入 Agents SDK 助手时使用

> **选型建议**：作业场景用 `createMcpHandler()` 即可；需要会话内记忆（多轮任务）
> 时才升级到 `McpAgent`。

## 部署：先无认证，后加认证

原文建议的路径：**先部署一个无认证的公开 MCP 服务器验证连通性，再补上认证与授权。**

**Dashboard 方式**：一键部署，服务器将上线于你的 `*.workers.dev` 子域
（如 `remote-mcp-server-authless.your-account.workers.dev/mcp`），并自动在你的
GitHub / GitLab 建立仓库，配置为**每次推送或合并 PR 到 main 分支时自动部署**。

**CLI 方式**：

```bash
# npm
npm create cloudflare@latest -- remote-mcp-server-authless \
  --template=cloudflare/ai/demos/remote-mcp-authless

# yarn
yarn create cloudflare remote-mcp-server-authless \
  --template=cloudflare/ai/demos/remote-mcp-authless

# pnpm
pnpm create cloudflare@latest remote-mcp-server-authless \
  --template=cloudflare/ai/demos/remote-mcp-authless
```

安装选项：**不加 AGENTS.md**、**不用 git**、**先不部署**（先本地测试）。

```bash
cd remote-mcp-server-authless
npm start          # 启动开发服务器，注意输出中的本地端口（本例 8788）
```

**测试**：

```bash
npx @modelcontextprotocol/inspector@latest
```

MCP Inspector 是**交互式 MCP 客户端**，可在浏览器中连接你的服务器并调用工具
（本例运行在 5173 端口）。在 Inspector 中填入 MCP 端点 URL
（`http://localhost:8788/mcp`）→ Connect → List Tools。

**部署**：

```bash
npx wrangler@latest deploy
```

## 通过本地代理连接远程服务器

如果你的 MCP 客户端**不支持远程传输或客户端侧授权**，可以用 `mcp-remote` 本地代理。
以 Claude Desktop 为例，修改其配置：

```json
{
  "mcpServers": {
    "math": {
      "command": "npx",
      "args": ["mcp-remote",
        "https://remote-mcp-server-authless.your-account.workers.dev/mcp"]
    }
  }
}
```

重启 Claude Desktop 即可。测试示例：

> 「能否用 math 工具把 23 和 19 相加？」

## 加入认证与授权

### 核心机制

> MCP 服务器处理安全的登录流程并**签发访问令牌（access token）**，MCP 客户端用该令牌
> 发起**经过认证的工具调用**。用户通过 OAuth 提供方登录，并**以作用域权限（scoped
> permissions）**授予其 AI 智能体与本服务器工具交互的权限。

**关键点**：认证（你是谁）→ 授权（你能调哪些工具）是**两件事**，后者靠 scope 表达。

### Cloudflare Access 作为 OAuth 提供方

Cloudflare Access 充当**身份聚合器**，校验：

- 用户邮箱
- 来自既有身份提供方（GitHub、Google）的信号
- **IP 地址或设备证书**等其他属性

用户连接时被引导到已配置的身份提供方登录，**只有通过 Access 策略才被授予访问权**。

### 第三方 OAuth（以 GitHub 为例）

任何支持 **OAuth 2.0** 规范的提供方都可用：GitHub、Google、Slack、Stytch、Auth0、
WorkOS 等。

**步骤 1：创建带 GitHub OAuth 的 MCP 服务器**

```bash
npm create cloudflare@latest -- my-mcp-server-github-auth \
  --template=cloudflare/ai/demos/remote-mcp-github-oauth
cd my-mcp-server-github-auth
```

关键差异在 `src/index.ts`——把 `defaultHandler` 设为 `GitHubHandler`：

```typescript
import GitHubHandler from "./github-handler";

export default new OAuthProvider({
  apiRoute: "/mcp",
  apiHandler: MyMCP.serve("/mcp"),
  defaultHandler: GitHubHandler,
  authorizeEndpoint: "/authorize",
  tokenEndpoint: "/token",
  clientRegistrationEndpoint: "/register",
});
```

**步骤 2：创建 OAuth App（本地开发 + 生产各一个）**

在 `github.com/settings/developers` 创建：

| 字段 | 本地开发 | 生产 |
|---|---|---|
| Application name | My MCP Server (local) | My MCP Server (production) |
| Homepage URL | `http://localhost:8788` | 你部署后的 `workers.dev` 域名 |
| Authorization callback URL | `http://localhost:8788/callback` | `.../callback` |

**本地开发**——把凭据写入项目根目录 `.env`：

```bash
touch .env
echo 'GITHUB_CLIENT_ID="your-client-id"' >> .env
echo 'GITHUB_CLIENT_SECRET="your-client-secret"' >> .env
```

**生产环境**——用 Wrangler 设置密钥（不要硬编码）：

```bash
npx wrangler secret put GITHUB_CLIENT_ID
npx wrangler secret put GITHUB_CLIENT_SECRET
npx wrangler secret put COOKIE_ENCRYPTION_KEY   # 如：openssl rand -hex 32
```

**配置 KV 命名空间**：

```bash
npx wrangler kv namespace create "OAUTH_KV"
```

然后在 `wrangler.jsonc` 中写入：

```json
{
  "kvNamespaces": [
    { "binding": "OAUTH_KV", "id": "<YOUR_KV_NAMESPACE_ID>" }
  ]
}
```

最后 `npm run deploy`，用 AI Playground / MCP Inspector 连接并用 GitHub 认证。

> 在 Inspector 中测试 OAuth：右侧主面板 → **OAuth Settings** 按钮 → **Quick OAuth Flow**
> → 跳转 GitHub 授权 → 跳回 → 侧栏点 Connect → 出现 List Tools。

## 与本课程的关系

- **Week 2 作业「构建自定义 MCP 服务器」的直接参考**。
- 与 `mcp-introduction`（协议概览）配套：那篇讲**是什么**，这篇讲**怎么部署与保护**。
- 与 `copilot-prompt-injection-rce` 形成鲜明对照：**无认证的公开 MCP 服务器
  等于把工具调用权开放给任何人**——若再叠加提示词注入，风险急剧放大。
- 与 `mcp-food-for-thought` 对照：那篇主张 API 自动转换效果差，这篇展示
  **手工设计的服务器**应有的完备度（认证、授权、作用域）。

## 可迁移到实践的四条

1. **先无认证跑通，再加认证**——把连通性问题与权限问题分开调试。
2. **认证 ≠ 授权**：用 scope 精确控制智能体可调用的工具集合。
3. **凭据绝不进代码库**：本地用 `.env`，生产用 `wrangler secret put`。
4. **客户端不支持远程传输时用 `mcp-remote` 代理**，避免为兼容旧客户端而降低服务端安全。
