# CS599 Project

## 项目简介

本项目用于课程《企业级应用软件设计与开发》期末大作业，选题方向为 Agentic AI 原生开发。项目基于 AutoSpider 思路构建一个面向网页信息采集任务的 AI Agent 系统，通过自然语言描述采集目标，由 Agent 完成任务澄清、页面规划、浏览器导航、URL 收集、字段抽取和结果落盘。

## 方向

方向一：Agentic AI 原生开发

## 技术栈

- AI IDE：Trae CN / Codex
- LLM：OpenAI 兼容 API
- Agent 框架：LangGraph / LangChain
- 浏览器自动化：Playwright
- 数据存储：SQLite
- 工程管理：Git / GitHub

## 目录结构

```text
cs599-project/
├── docs/
│   ├── CS599_大作业报告.pdf
│   └── architecture.md
├── src/
│   └── autospider-project/        # AutoSpider 项目代码与运行脚本
│       ├── src/autospider/        # 核心 Agent 实现
│       ├── tests/                 # 测试用例
│       ├── start_bangumi_demo.cmd # Bangumi 小规模演示脚本
│       └── start_autospider.cmd   # 交互式启动脚本
├── README.md
├── .gitignore
└── LICENSE
```

## 环境搭建

项目代码位于 `src/autospider-project/`。本地已验证的演示入口：

```cmd
cd /d D:\codex\code\cs599-project\src\autospider-project
start_bangumi_demo.cmd
```

后续补充完整环境搭建步骤，包括 Python 版本、虚拟环境、依赖安装、API Key 环境变量配置、Playwright 浏览器安装和本地运行命令。

## 项目状态

- [x] Proposal
- [x] MVP
- [ ] Final
