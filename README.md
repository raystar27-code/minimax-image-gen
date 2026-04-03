# MiniMax 图像生成工具 (MiniMax Image Gen Skill)

这是一个为 **OpenClaw** 开发的、高度封装的 MiniMax 图像生成技能插件。它能够通过自然语言指令生成高质量图片，并支持多比例、批量生成及风格化控制。

## 🌟 特点
- **全功能支持**：集成 MiniMax `image-01` (高质) 与 `image-01-live` (极速) 模型。
- **灵活配置**：支持 4:3, 16:9, 1:1 等多种比例，支持批量出图 (`n` 参数)。
- **高度封装**：技能代码、文档、依赖均位于 `skills/minimax-image-gen/` 目录下，易于部署。
- **OpenClaw 友好**：内置标准格式的 `SKILL.md`，可供智能体快速学习。

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r skills/minimax-image-gen/requirements.txt
```

### 2. 配置秘钥
在该目录下创建 `.env` 文件：
```bash
cp skills/minimax-image-gen/.env.example skills/minimax-image-gen/.env
# 然后填入你的 MINIMAX_API_KEY
```

### 3. 在 OpenClaw 中使用
将此仓库克隆至 OpenClaw 的技能工作区，或直接让 OpenClaw 读取该项目并执行练习。

---
## 📄 常用命令示例
```bash
# 生成一张江南水乡图
python3 skills/minimax-image-gen/minimax_gen.py --prompt "江南水乡"

# 生成一张 16:9 的赛博朋克风格图
python3 skills/minimax-image-gen/minimax_gen.py --prompt "赛博朋克" --aspect_ratio 16:9
```
