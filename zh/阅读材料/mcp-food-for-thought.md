---
source: https://www.reillywood.com/blog/apis-dont-make-good-mcp-tools/
license: 个人博客，未明示再发布授权
tier: B
handling: 中文精读笔记（非逐段译文）
week: 2
---

# 精读笔记：API 并不是好的 MCP 工具

> 原文：APIs don't make good MCP tools（作者 Reilly Wood）
> ⚠️ 本笔记为**提炼与讲解**，非逐段译文。原文版权归作者所有，请通过上方链接阅读原文。

## 一句话结论

把既有 Web API 自动转换成 MCP 工具「能跑，但跑不好」——因为 API 是为**确定性程序**
设计的，而智能体的约束（上下文预算、工具数量上限、token 效率）与之根本不匹配。

## 四个核心论点

### 1. 智能体应付不了大量工具

- VS Code 有 **128 个工具的硬上限**；而实际上许多模型在远低于此数量时工具调用精度
  就已明显下滑。
- 每个工具及其描述都要**占用宝贵的上下文窗口**。
- 多数 Web API 设计时并未考虑这些约束。一个产品领域里有几十个 API 对代码调用
  没问题，但一一映射成 MCP 工具后效果往往很差。
- **从零设计的 MCP 工具通常比单个 Web API 灵活得多**——一个工具可以完成多个 API 的工作。

### 2. API 会迅速撑爆上下文窗口

- 设想某 API 一次返回 100 条记录，每条 50 个字段。即使查询只需要少数字段，
  **所有字段最终都会进入上下文窗口**。
- API 通常按**记录数**分页，但记录大小差异巨大：一条可能含 10 万 token 的大文本字段，
  另一条可能只有 10。直接塞进上下文是**赌博**——有时成功，有时炸掉。
- **JSON 是 token 效率极差的格式。** 原文给的对比：

```json
[{"firstName":"Alice","lastName":"Johnson","age":28},
 {"firstName":"Bob","lastName":"Smith","age":35}]
```

```csv
firstName,lastName,age
Alice,Johnson,28
Bob,Smith,35
```

> **CSV 每条记录的 token 数只有 JSON 的一半。** 一般而言 CSV、TSV 或 YAML（嵌套数据）
> 比 JSON 更适合作为工具返回格式。

作者也承认这些问题**并非无解**——完全可以自动加字段投影参数、自动截断/摘要大结果、
自动把 JSON 转成 CSV。但**他见过的大多数服务器一件都没做**。

### 3. API 没有发挥智能体的独特能力

API 返回结构化数据供程序消费——这固然是智能体想要的，但**智能体还能处理更自由形式的
指令**。例如：

- 一个 `ask_question` 工具可以对文档做 RAG 查询，返回**纯文本**来支撑下一次工具调用，
  完全跳过结构化数据。
- 一个 `search_cities` 工具可以返回城市列表**并附上下一步建议**：

```csv
city_name,population,country,region
Tokyo,37194000,Japan,Asia
Delhi,32941000,India,Asia
Shanghai,28517000,China,Asia

Suggestion: To get more specific information (weather, attractions, demographics),
try calling get_city_details with the city_name parameter.
```

这种**分层与工具链式调用**在 MCP 服务器中非常有效，而自动转换 API 的做法会把它完全抹掉。

### 4. 如果智能体需要调 API，它其实可以自己调

Claude Code 这类智能体如今**写 + 执行代码**（包括调用 Web API 的脚本）的能力相当强。
有人因此主张「根本不需要 MCP」。作者**不同意这个结论**，但认同一个方向性判断：
智能体的沙箱能力在快速改进，如果智能体直接调 API 既**容易又安全**，
那不妨就这么做，去掉中间层。

> 作者的态度是「顺势而为」而非教条——这是工程判断，不是立场之争。

## 结论原文要点

智能体与 API 的典型消费者**根本不同**。从既有 API 自动生成 MCP 工具是可行的，
但**不太可能效果好**。当工具是**针对智能体独特的能力与限制设计**时，智能体才表现最好。

## 与本课程的关系

| 关联点 | 说明 |
|---|---|
| Week 2（MCP） | 本文解释了为什么「MCP 服务器 = API 包装」是常见误设计 |
| Week 3（上下文管理） | token 效率与字段投影是上下文工程的一部分 |
| Week 6（安全） | 「智能体可直接调 API」一旦缺乏沙箱，就是提示词注入的直接入口（见 `copilot-prompt-injection-rce`） |

## 可迁移到实践的三条

1. **给工具加字段投影参数**，别让智能体被动吞下全部字段。
2. **默认返回 CSV/TSV/YAML 而非 JSON**，token 直接省一半。
3. **返回时附带「下一步建议」**，把工具链路由显式告诉智能体，而不是让它自己猜。
