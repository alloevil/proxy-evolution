# proxy-evolution

一句话介绍：补充本项目的定位。

## 常用命令

未探测到构建/测试命令——补一行真实可跑的命令再上岗。

## 边界

### never

- 不读取、不提交 `.env`

### ask-first

- 新增运行时依赖
- 修改 CI 配置
- 对任何分支 force push

<!-- 这是起点：agent 犯一次错就补一条边界，定期跑 agentsmd-lint。 -->
