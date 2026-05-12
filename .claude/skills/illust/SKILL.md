# Skill: illust — Wiki 配图生成

## 触发指令

- `/illust <wiki页面路径>` — 为指定页面生成配图
- `/illust` — 扫描所有 wiki/ 页面，为没有图片的页面批量生图

ingest 技能处理完一个文件后，**自动调用本技能**为新生成的 wiki 页面配图。

---

## 执行流程

### 单页面模式 `/illust <路径>`

1. 读取目标 `.md` 文件内容
2. 提炼核心概念，生成一段**英文图片描述 prompt**（见 Prompt 规范）
3. 调用 `generate.py` 生图，图片保存到 `assets/illust/`
4. 在页面的 `## 关联连接` 区域**之前**插入图片引用：
   ```
   ![[assets/illust/文件名.png]]
   ```
5. 在 `wiki/log.md` 追加记录

### 批量模式 `/illust`

- 遍历 `wiki/` 下所有 `.md` 文件
- 跳过已包含 `![[assets/illust/` 的页面
- 其余页面依次执行单页面流程

### ingest 自动触发

ingest 处理完每个文件、创建/更新 wiki 页面后，立即对该页面执行单页面流程。

---

## Prompt 生成规范

根据页面 `type` 字段选择不同风格：

| type | 图片风格指令 |
|------|-------------|
| `concept` | `clean technical diagram, minimalist, dark background, glowing lines, no text` |
| `entity` | `professional portrait illustration, flat design, neutral background` |
| `source` | `book cover style, abstract representation of the topic, modern design` |
| `synthesis` | `mind map visualization, interconnected nodes, dark theme` |
| `comparison` | `side by side comparison diagram, clean infographic style` |

**Prompt 模板：**
```
{核心概念的英文描述}, {风格指令}, high quality, 4k
```

示例：
- `Transformer attention mechanism with multiple heads processing tokens in parallel, clean technical diagram, minimalist, dark background, glowing lines, no text, high quality, 4k`

---

## 调用 generate.py

```bash
uv run .claude/skills/illust/generate.py \
  --prompt "<生成的prompt>" \
  --output "assets/illust/<slug>.png" \
  --provider openai   # 或 google
```

默认 provider 优先级：读取 `ILLUST_PROVIDER` 环境变量，默认 `openai`。

---

## 文件命名规则

图片文件名 = wiki 页面文件名（去掉 `.md`）+ `.png`

示例：
- `wiki/concepts/Transformer架构.md` → `assets/illust/Transformer架构.png`

---

## log.md 记录格式

```
- [YYYY-MM-DD] [illust] <页面路径> → assets/illust/<文件名>.png (provider: openai)
```

---

## 错误处理

- API 调用失败：在页面插入 `> [!todo] 待补充：配图生成失败，请手动运行 /illust <路径>` 并继续
- 网络超时：重试一次，仍失败则同上
- 已有图片：询问用户是否覆盖，默认跳过
