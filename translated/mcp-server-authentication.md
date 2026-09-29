# 构建远程 MCP 服务器 ‹ Cloudflare Agents 文档

# 构建远程 MCP 服务器

本指南将展示如何使用 Streamable HTTP 传输（当前 MCP 规范标准）在 Cloudflare 上部署你自己的远程 MCP 服务器。你有两种选择：

- 不带身份验证 —— 任何人都可以连接并使用该服务器（无需登录）。
- 带身份验证和授权 —— 用户在使用工具前需先登录，并且你可以根据用户的权限控制智能体可以调用哪些工具。

## 选择方案

Agents SDK 提供了多种创建 MCP 服务器的方式。请选择适合你用例的方案：

| 方案 | 有状态？ | 是否需要 Durable Objects？ | 适用场景 |
| --- | --- | --- | --- |
| `createMcpHandler()` | 否 | 否 | 无状态工具，设置最简单 |
| `McpAgent` | 是 | 是 | 有状态工具、会话级状态、用户输入请求（elicitation） |
| 原生 `WebStandardStreamableHTTPServerTransport` | 否 | 否 | 完全可控，不依赖 SDK |

- `createMcpHandler()` 是让无状态 MCP 服务器运行起来的最快方式。当你的工具不需要会话级状态时，请使用它。
- `McpAgent` 会为每个会话提供一个 Durable Object，内置状态管理、用户输入请求支持，并同时支持 SSE 和 Streamable HTTP 两种传输。
- 如果你想直接使用 `@modelcontextprotocol/sdk`，而不借助 Agents SDK 的辅助功能，原生传输方式可让你完全掌控。

## 部署你的第一个 MCP 服务器

你可以先部署一个不带身份验证的公开 MCP 服务器，之后再添加用户身份验证和范围化授权。如果你已确定服务器需要身份验证，可以直接跳到下一节。

### 通过仪表板

下面的按钮将引导你完成将示例 MCP 服务器部署到你的 Cloudflare 账户所需的全部步骤：

部署完成后，该服务器将在你的 workers.dev 子域上线（例如 remote-mcp-server-authless.your-account.workers.dev/mcp）。你可以立即使用 AI Playground（一个远程 MCP 客户端）、MCP Inspector 或其他 MCP 客户端连接它。

系统将在你的 GitHub 或 GitLab 账户上为你的 MCP 服务器创建一个新的 git 仓库，并已配置为：每次向该仓库的主分支推送更改或合并拉取请求（PR）时，自动部署到 Cloudflare。你可以克隆该仓库、在本地开发，并开始用自己的工具自定义 MCP 服务器。

### 通过 CLI

你可以使用 Wrangler CLI 在本地机器上创建一个新的 MCP 服务器，并将其部署到 Cloudflare。

- 打开终端并运行以下命令：

```sh
npm create cloudflare@latest -- remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
```

```sh
yarn create cloudflare remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
```

```sh
pnpm create cloudflare@latest remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
```

在设置过程中，选择以下选项：
- 对于「Do you want to add an AGENTS.md file to help AI coding tools understand Cloudflare APIs?」（是否添加 AGENTS.md 文件以帮助 AI 编程工具理解 Cloudflare API？），选择 No。
- 对于「Do you want to use git for version control?」（是否使用 git 进行版本控制？），选择 No。
- 对于「Do you want to deploy your application?」（是否部署你的应用？），选择 No（我们会先测试服务器，再部署）。

现在，你的 MCP 服务器已设置完毕，依赖也已安装。

- 进入项目文件夹：

终端窗口

```sh
cd remote-mcp-server-authless
```

- 在新项目的目录中，运行以下命令启动开发服务器：

终端窗口

```sh
npm start
```

```
Starting local server...
[ wrangler:info ] Ready on http://localhost:8788
```

请查看命令输出以确认本地端口。在此示例中，MCP 服务器运行在 8788 端口，MCP 端点 URL 为 http://localhost:8788/mcp。

- 要在本地测试服务器：请在新终端中运行 MCP Inspector。MCP Inspector 是一个交互式 MCP 客户端，让你可以通过网页浏览器连接 MCP 服务器并调用工具。

终端窗口

```sh
npx @modelcontextprotocol/inspector@latest
```

```
MCP Inspector is up and running at: http://localhost:5173/?MCP_PROXY_AUTH_TOKEN=46ab..cd3
Opening browser...
```

MCP Inspector 将在你的网页浏览器中启动。你也可以手动启动它：打开浏览器并访问 http://localhost:<PORT>。请查看命令输出，确认 MCP Inspector 运行的本地端口。在此示例中，MCP Inspector 运行在 5173 端口。

在 MCP Inspector 中，输入你的 MCP 服务器 URL（http://localhost:8788/mcp），然后选择 Connect。选择 List Tools 即可显示你的 MCP 服务器公开的工具。

- 现在，你可以将 MCP 服务器部署到 Cloudflare。请在项目目录中运行：

终端窗口

```sh
npx wrangler@latest deploy
```

如果你已将某个 git 仓库连接到承载 MCP 服务器的 Worker，也可以通过向该仓库的主分支推送更改或合并拉取请求来部署 MCP 服务器。MCP 服务器将部署到你的 *.workers.dev 子域：https://remote-mcp-server-authless.your-account.workers.dev/mcp。

- 要测试远程 MCP 服务器，请将已部署 MCP 服务器的 URL（https://remote-mcp-server-authless.your-account.workers.dev/mcp）输入到运行于 http://localhost:5173 的 MCP Inspector 中。

现在，你已经有了一个 MCP 客户端可以连接的远程 MCP 服务器。

## 通过本地代理从 MCP 客户端连接

远程 MCP 服务器运行起来后，你可以使用 `mcp-remote` 本地代理将 Claude Desktop 或其他 MCP 客户端连接到它 —— 即使你的 MCP 客户端不支持远程传输或客户端侧授权。这样，你就可以用真实的 MCP 客户端测试与远程 MCP 服务器交互的实际效果。

例如，从 Claude Desktop 连接：

- 更新你的 Claude Desktop 配置，使其指向你的 MCP 服务器 URL：

```json
{
  "mcpServers": {
    "math": {
      "command": "npx",
      "args": ["mcp-remote", "https://remote-mcp-server-authless.your-account.workers.dev/mcp"]
    }
  }
}
```

- 重启 Claude Desktop 以加载 MCP 服务器。完成后，Claude 就能调用你的远程 MCP 服务器。
- 要测试，可以请 Claude 使用你的某个工具。例如：你能用 `math` 工具计算 23 加 19 吗？Claude 应当会调用该工具，并显示远程 MCP 服务器生成的结果。

要了解如何与其他 MCP 客户端一起使用远程 MCP 服务器，请参阅「测试远程 MCP 服务器」。

## 添加身份验证

你之前部署的公开 MCP 服务器示例允许任何客户端在无需登录的情况下连接并调用工具。要为你的 MCP 服务器添加用户身份验证，可以集成 Cloudflare Access 或第三方服务作为 OAuth 提供方。你的 MCP 服务器会处理安全登录流程，并颁发访问令牌，MCP 客户端可使用这些令牌进行已认证的工具调用。用户通过 OAuth 提供方登录，并通过范围化权限授予其 AI 智能体与你的 MCP 服务器所公开工具交互的权限。

### Cloudflare Access OAuth

你可以将 MCP 服务器配置为要求用户通过 Cloudflare Access 进行身份验证。Cloudflare Access 充当身份聚合器，负责验证用户邮箱、来自你现有身份提供方（如 GitHub 或 Google）的信号，以及 IP 地址或设备证书等其他属性。当用户连接到 MCP 服务器时，系统会提示他们登录已配置的身份提供方，只有通过你的 Access 策略的用户才会被授予访问权限。

如需分步部署指南，请参阅「使用 Access for SaaS 保护 MCP 服务器」。

### 第三方 OAuth

你可以将 MCP 服务器与任何支持 OAuth 2.0 规范的 OAuth 提供方对接，包括 GitHub、Google、Slack、Stytch、Auth0、WorkOS 等。

以下示例演示了如何使用 GitHub 作为 OAuth 提供方。

#### 步骤 1：创建新的 MCP 服务器

运行以下命令，创建一个带 GitHub OAuth 的新 MCP 服务器：

```sh
npm create cloudflare@latest -- my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
```

```sh
yarn create cloudflare my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
```

```sh
pnpm create cloudflare@latest my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
```

现在，你的 MCP 服务器已设置完毕，依赖也已安装。进入该项目文件夹：

终端窗口

```sh
cd my-mcp-server-github-auth
```

你会发现，在这个示例 MCP 服务器中，如果你打开 `src/index.ts`，主要区别在于 `defaultHandler` 被设置为 `GitHubHandler`：

TypeScript

```ts
import GitHubHandler from "./github-handler";
export default new OAuthProvider({ apiRoute: "/mcp", apiHandler: MyMCP.serve("/mcp"), defaultHandler: GitHubHandler, authorizeEndpoint: "/authorize", tokenEndpoint: "/token", clientRegistrationEndpoint: "/register",});
```

这可以确保你的用户被重定向到 GitHub 进行身份验证。不过，要让这一切真正生效，你还需要按照下面的步骤创建 OAuth 客户端应用。

#### 步骤 2：创建 OAuth App

你需要创建两个 GitHub OAuth App —— 一个用于本地开发，一个用于生产环境 —— 才能将 GitHub 用作 MCP 服务器的身份验证提供方。

#### 步骤 2.1：为本地开发创建新的 OAuth App

- 前往 github.com/settings/developers，按以下设置创建一个新的 OAuth App：
  - 应用名称（Application name）：My MCP Server (local)
  - 主页 URL（Homepage URL）：http://localhost:8788
  - 授权回调 URL（Authorization callback URL）：http://localhost:8788/callback
- 对于刚创建的 OAuth App，将它的客户端 ID 添加为 `GITHUB_CLIENT_ID`，并生成一个客户端密钥，将其作为 `GITHUB_CLIENT_SECRET` 写入项目根目录的 `.env` 文件中；这些值将用于本地开发中的密钥设置。

终端窗口

```sh
touch .env
echo 'GITHUB_CLIENT_ID="your-client-id"' >> .env
echo 'GITHUB_CLIENT_SECRET="your-client-secret"' >> .env
cat .env
```

- 运行以下命令启动开发服务器：

终端窗口

```sh
npm start
```

现在，你的 MCP 服务器运行在 http://localhost:8788/mcp 上。

- 在新终端中运行 MCP Inspector。MCP Inspector 是一个交互式 MCP 客户端，让你可以通过网页浏览器连接 MCP 服务器并调用工具。

终端窗口

```sh
npx @modelcontextprotocol/inspector@latest
```

- 在网页浏览器中打开 MCP Inspector：

终端窗口

```sh
open http://localhost:5173
```

- 在 Inspector 中输入你的 MCP 服务器 URL：http://localhost:8788/mcp
- 在右侧的主面板中，点击 OAuth Settings 按钮，然后点击 Quick OAuth Flow。你应当会被重定向到 GitHub 登录或授权页面。授权 MCP 客户端（即 Inspector）访问你的 GitHub 账户后，你将被重定向回 Inspector。
- 在侧边栏中点击 Connect，你应该会看到「List Tools」按钮，点击它会列出你的 MCP 服务器公开的工具。

#### 步骤 2.2：为生产环境创建新的 OAuth App

你需要重复步骤 2.1，为生产环境再创建一个新的 OAuth App。

- 前往 github.com/settings/developers，按以下设置创建一个新的 OAuth App：
  - 应用名称（Application name）：My MCP Server (production)
  - 主页 URL（Homepage URL）：填写已部署 MCP 服务器的 workers.dev URL（例如：worker-name.account-name.workers.dev）
  - 授权回调 URL（Authorization callback URL）：填写已部署 MCP 服务器的 workers.dev URL 的 /callback 路径（例如：worker-name.account-name.workers.dev/callback）

- 对于刚创建的 OAuth App，使用 Wrangler CLI 添加客户端 ID 和客户端密钥：

终端窗口

```sh
npx wrangler secret put GITHUB_CLIENT_ID
```

终端窗口

```sh
npx wrangler secret put GITHUB_CLIENT_SECRET
```

```sh
npx wrangler secret put COOKIE_ENCRYPTION_KEY # add any random string here e.g. openssl rand -hex 32
```

- 设置 KV 命名空间
  a. 创建 KV 命名空间：

终端窗口

```sh
npx wrangler kv namespace create "OAUTH_KV"
```

  b. 使用生成的 KV ID 更新 `wrangler.jsonc` 文件：

```json
{
  "kvNamespaces": [
    {
      "binding": "OAUTH_KV",
      "id": "<YOUR_KV_NAMESPACE_ID>"
    }
  ]
}
```

- 将 MCP 服务器部署到你的 Cloudflare workers.dev 域：

终端窗口

```sh
npm run deploy
```

- 使用 AI Playground、MCP Inspector 或其他 MCP 客户端连接运行于 worker-name.account-name.workers.dev/mcp 的服务器，并使用 GitHub 完成身份验证。

## 后续步骤

MCP 工具 — 为你的 MCP 服务器添加工具。
授权 — 自定义身份验证和授权。