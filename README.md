# AutoSpider: A Pure-Vision Browser Agent for Web Data Collection

基于 LangGraph 和 Playwright 的纯视觉浏览器智能体，用户用自然语言描述采集目标后，系统自动完成网页导航、URL 收集、字段抽取和结构化结果输出。

## 方向

方向一：Agentic AI 原生开发

## 技术栈

- AI IDE：Trae CN / Codex
- LLM：OpenAI 兼容 API
- Agent 框架：LangGraph + LangChain
- 浏览器自动化：Playwright
- CLI：Typer + Rich
- 数据存储：SQLite + JSON / JSONL 文件
- 状态与队列：Memory 模式；保留 Redis 适配能力
- 工程管理：Git / GitHub

## 目录结构

```text
cs599-project/
├── docs/
│   ├── architecture.md              # 系统架构说明
│   └── CS599_大作业报告.pdf          # 最终报告，后续补充
├── src/
│   └── autospider-project/
│       ├── src/autospider/
│       │   ├── interface/cli/       # CLI 入口
│       │   ├── composition/         # LangGraph 编排与流水线
│       │   ├── contexts/
│       │   │   ├── chat/            # 任务澄清与需求结构化
│       │   │   ├── planning/        # 任务规划与子任务拆分
│       │   │   ├── collection/      # 页面导航、URL 收集、字段抽取
│       │   │   └── experience/      # Skill / XPath 经验沉淀
│       │   └── platform/            # LLM、浏览器、日志、持久化等基础设施
│       ├── tests/                   # 单元测试、契约测试、Benchmark 测试
│       ├── start_bangumi_demo.cmd   # Bangumi 演示脚本
│       ├── start_autospider.cmd     # 交互式启动脚本
│       ├── pyproject.toml
│       └── README.md                # AutoSpider 子项目说明
├── README.md
├── .gitignore
└── LICENSE
```

## 环境搭建

以下命令以 Windows CMD 为例。推荐使用 Python 3.11。

### 1. 进入项目目录

```cmd
git clone https://github.com/lingbolan/cs599-project.git
cd cs599-project\src\autospider-project
```

### 2. 创建虚拟环境

```cmd
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
```

如果系统没有注册 `py -3.11`，也可以将第一行替换为本机 Python 3.11 的 `python.exe` 路径。

### 3. 安装依赖

```cmd
.\.venv\Scripts\pip.exe install -e ".[dev,redis,db]"
.\.venv\Scripts\pip.exe install lxml
```

### 4. 安装 Playwright 浏览器

```cmd
set PLAYWRIGHT_BROWSERS_PATH=%cd%\.pw-browsers
.\.venv\Scripts\playwright.exe install chromium
```

### 5. 配置 API Key

复制环境变量模板：

```cmd
copy .env.example .env
```

编辑 `.env`，配置 OpenAI 兼容 API：

```env
BAILIAN_API_KEY=your-api-key-here
BAILIAN_API_BASE=https://your-api-provider.example/v1
BAILIAN_MODEL=your-model-name
```

不要把 `.env` 提交到 GitHub。仓库 `.gitignore` 已忽略 `.env`、运行输出、虚拟环境和浏览器缓存。

## 启动方式

### Bangumi 演示任务

```cmd
cd cs599-project\src\autospider-project
start_bangumi_demo.cmd
```

脚本会以 memory 模式启动，默认任务为：

```text
Collect 5 anime entries from Bangumi calendar page https://bangumi.tv/calendar.
Fields: Chinese title, Japanese title, weekday.
```

如果终端出现确认问题：

```text
请选择下一步 [1=开始执行, 2=补充需求并重新生成, 3=手动修改字段后执行, 4=取消]
```

输入：

```text
1
```

如果出现历史任务选择：

```text
1. 复用历史任务
2. 创建新任务
```

建议输入：

```text
2
```

### 交互式任务

```cmd
cd cs599-project\src\autospider-project
start_autospider.cmd
```

示例输入：

```text
从 Bangumi 每日放送页 https://bangumi.tv/calendar 采集 5 条动画，字段包括中文标题、日文标题、放送星期。
```

## 结果输出

运行结果保存在 `src/autospider-project/output/`：

```text
output/
├── merged_results.jsonl                         # 最终合并结果
├── task_plan.json                               # 任务规划结果
├── plan_knowledge.md                            # 规划阶段生成的知识文档
├── runtime.log                                  # 运行日志
└── subtask_leaf_001/
    ├── collected_urls.json                      # 收集到的详情页 URL 和点击记录
    ├── pipeline_extracted_items.jsonl           # 子任务字段抽取结果
    └── pipeline_summary.json                    # 成功数、失败数、成功率等摘要
```

查看最终结果：

```cmd
type output\merged_results.jsonl
```

如果中文乱码，使用 PowerShell：

```powershell
Get-Content .\output\merged_results.jsonl -Encoding utf8
```

## 工作流

```text
User Request
    ↓
Task Clarification
    ↓
Planning
    ↓
Browser Navigation
    ↓
URL Collection
    ↓
Detail Page Extraction
    ↓
Result Aggregation
    ↓
Output Artifacts
```

- **Task Clarification**：将用户的自然语言需求转换为结构化采集任务。
- **Planning**：分析目标页面，生成采集计划和子任务。
- **Browser Navigation**：通过 Playwright 打开页面，并由视觉 LLM 判断下一步操作。
- **URL Collection**：从列表页收集详情页链接。
- **Detail Page Extraction**：访问详情页并抽取结构化字段。
- **Result Aggregation**：合并子任务结果，输出 JSONL 和摘要文件。

## 核心特性

- 纯视觉浏览器智能体：基于截图和 Set-of-Mark 标注理解网页。
- 多步骤 Agent 流程：任务澄清、规划、导航、采集、抽取、聚合分阶段执行。
- LangGraph 状态管理：使用图结构组织多轮中断、恢复和执行状态。
- 工具调用能力：通过 Playwright 控制浏览器完成真实页面访问。
- Memory 本地运行模式：在无 Redis 服务时也可以完成小规模 Demo。
- 可观测输出：保留运行日志、任务计划、采集 URL、抽取结果和成功率摘要。

## 本地改造

为适配课程演示和本地部署，本项目在原 AutoSpider 基础上进行了以下调整：

- 增加 memory checkpoint 后端，降低本地部署门槛。
- 增加 memory URL channel，使小规模 Demo 不依赖 Redis。
- 增加 OpenAI 兼容 API 请求头适配，兼容第三方 API 供应商。
- 增加 Windows 启动脚本，统一设置 UTF-8、Playwright 浏览器路径和本地运行参数。
- 增加 Bangumi 小规模演示脚本，控制运行时间并输出可展示结果。

## 项目状态

- [x] Proposal
- [x] MVP
- [ ] Final

当前项目主体、运行脚本和 Demo 已完成。后续主要补充课程报告、Specs 文档、测试评估截图和最终 PDF。

## 许可证

[MIT License](LICENSE)
