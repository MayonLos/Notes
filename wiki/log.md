# Wiki 操作日志

> Append-only。每条以 `## [YYYY-MM-DD] type | title` 开头，支持 grep：
> `grep "^## \[" wiki/log.md | tail -5`

- [2026-05-12] [illust] wiki/concepts/Laplace变换.md → assets/illust/Laplace变换.png (provider: google, model: imagen-4.0-generate-001)

## [2026-05-12] ingest | 锁存器与触发器.pdf
- **变更**: 新增 [[摘要-锁存器与触发器]]；大幅扩充 [[锁存器和触发器]]（维持-阻塞原理/波形图/一次采用现象/异步置复位/触发器互转）；更新 [[index.md]]
- **冲突**: "一次翻转限制"与"一次采用现象"术语差异，已在页面中统一解释两者关系，无静默覆盖

---

## [2026-05-07] ingest | 全量资料重摄入（4 源 + 25 wiki 导出）
- **变更**:
  - 新增资料摘要：[[摘要-agent-skills-spec]]、[[摘要-deepseek-api]]、[[摘要-thorough-pytorch]]、[[摘要-数字电路课堂笔记]]
  - 新增实体：[[agentskills-io]]、[[DeepSeek]]、[[DataWhale]]
  - 新增概念（AI/工具链）：[[AgentSkills]]、[[渐进式加载]]、[[API兼容性策略]]、[[PyTorch]]
  - 新增概念（数字电路）：[[计数制与编码]]、[[逻辑代数]]、[[逻辑函数化简]]、[[逻辑门电路]]、[[组合逻辑电路]]、[[锁存器和触发器]]、[[原码反码补码]]
  - 新增概念（C++）：[[基础语法]]、[[面向对象]]、[[标准模板库]]、[[内存管理]]
  - 新增概念（控制理论/数学）：[[算子]]、[[Laplace变换]]、[[物理建模]]、[[方框图]]
  - 新增对比：[[TTL-vs-CMOS]]
  - 新增综合：[[算子本质]]
  - 更新：[[index.md]]、[[synthesis.md]]
- **新增洞察**：AgentSkills `description` 字段的双重职责冲突（功能说明 vs 激活条件），导致 false positive 触发与沉没成本效应，已记录于 [[AgentSkills]]
- **路径修正**：数字电路课堂笔记图片实际路径为 `raw/04-notes/2026-05-05-数字电路课堂笔记/IMG_*.jpg`，旧摘要中路径有误，已在新摘要页中修正
- **冲突**: 无
- **归档**: 3 篇文章（raw/01-articles/）+ 25 个旧 wiki 导出（raw/05-wiki-export/）已归档

## [2026-05-06] init | 知识库全量重构

- **变更**: 清空 wiki/，重建框架文件；旧内容迁移至 raw/05-wiki-export/；archive 解冻至 raw/
- **冲突**: 无
