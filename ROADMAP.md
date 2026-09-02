# gtlx-sh 重构开发规划（v2）

> 目标：把 gtlx-sh 从"平铺脚本目录"重构为「按文件夹分类 + 统一 git 管理 + 网页索引界面」的完整工具库。
> 原则：脚本真身全在 gtlx-sh（git 管理、AGPL），`~/.local/bin` 只留软链；检测脚本去重；**能看说明、能点执行**。

---

## 现状问题

1. **重复**：`coc` / `systemctl-analysis` 在 `gtlx-sh/` 和 `~/.local/bin/health/` 各有一份（曾不同步）
2. **分散**：脚本散在 `gtlx-sh/`、`~/.local/bin/`、`~/.local/bin/health/` 三处
3. **无统一索引**：没有一个能看到"有哪些脚本、干嘛用、怎么调"的地方

## 目标结构

```
gtlx-sh/
  README.md  LICENSE
  detection/          ← 检测类（原 health/ 合并）：coc, pkg-audit, systemctl-analysis, syscheck
  ocr/                ← 截图识别：ocr, ocrshot（已完成 ✅）
  backup/             ← 备份类：restic-backup, server-backup.sh
  write/  whatever/   ← 其他按需
~/.local/bin/         ← 只有软链 → gtlx-sh
```

---

## 一期：目录分类 + 检测脚本去重

**本期后：重复消失，脚本归位，git 统一管理**

- [x] 建立 `detection/`、`backup/` 分类目录
- [x] 把 `~/.local/bin/health/{coc,pkg-audit,systemctl-analysis}` 与 `gtlx-sh/` 里同名脚本**比对 → 取最新/合并 → 归入 `detection/`**
- [x] 处理 `appimage`（gtlx-sh 与 ~/.local/bin 曾 md5 不同，比对合版）
- [x] `syscheck`（~/.local/bin 的体检调度器）保留作入口，改指 `detection/` 脚本
- [x] `backup/` 收编 `restic-backup`、`server-backup.sh`
- [x] `~/.local/bin` 全部换软链 + 清理 .bak
- [x] README 更新目录结构

**验收**：`git grep` 无重复脚本；全部命令经软链可用；`syscheck` 能调 detection/ 模块

---

## 二期：网页索引界面（能看说明 + 能执行）

**本期后：浏览器打开即见所有脚本，点开看用法，可点运行**

- 技术：Python FastAPI（或轻量 Flask）+ 前端单页
- 功能：
  - 按文件夹分组列出脚本
  - 解析脚本头部注释 → 显示用途/用法
  - 「运行」按钮 → 回调后端 `subprocess` 执行（在终端/界面显示输出）
  - 目录配置可编辑（映射 gtlx-sh 路径）
- 安全：运行前确认；sudo 命令明确标示
- 形态：`localhost` 本地访问，可从 niri 或 Hermes 唤起

**验收**：浏览器列出全部脚本、点开看说明、点运行出结果

---

## 三期：打磨（可选）

- [ ] 索引界面美化（Soft UI/Glassmorphism，符合你审美）
- [ ] 脚本执行输出实时流
- [ ] 支持编辑脚本/新增脚本
- [ ] 打成 systemd 服务开机可访问

---

## 技术选型说明（为什么不用 Rust）

这个索引界面的**瓶颈是"组织 + 展示 + 调脚本"，不是性能**。Rust 的性能/内存优势在这里用不上。Python 与 bash 脚本同域（`subprocess` 天然），开发快、一个文件就能起。符合"先问瓶颈再定语言"。Rust 仅在未来要「离线单文件分发给别人」时才值得。

---

## 进度记录

- 2026-09-03：一期前置——`ocr/` 分类完成（ocr/ocrshot 迁入 + 软链 + README）✅
- 2026-09-03：提交 df365b3（ocr 迁入）