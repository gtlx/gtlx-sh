# gtlx-sh

个人常用脚本集合。按**文件夹分类**，每个脚本独立文件，Git 版本管理，AGPL-3.0 许可。

```
gtlx-sh/
  appimage, gitpush                     ← 根目录: 单脚本工具
  detection/                            ← 检测类: coc, pkg-audit, systemctl-analysis, syscheck
  ocr/                                  ← 截图识别: ocr, ocrshot
  backup/                               ← 备份类: restic-backup, server-backup.sh
  ...
```

`~/.local/bin/` 中的命令是**软链接**，指向本目录脚本真身。改脚本请改这里（git 管理、可回退），不要改 `~/.local/bin` 里的软链。

---

## ocr/ — 截图识别（OCR）

Wayland 截图即文字识别，串 grim + slurp + satty + rapidocr。

### ocr — 图片文字识别 CLI
```bash
ocr                     # 识别 ~/Pictures/ScreenShot/ 最新截图
ocr 图片.png            # 识别指定文件
ocr --clipboard         # 识别剪贴板图片
ocr --clipboard-txt     # 读剪贴板文本
```

### ocrshot — 截图即识别（区域/整屏 → 标注 → OCR → 复制）
```bash
ocrshot            # 框选区域 → satty 标注 → OCR → 复制
ocrshot --full     # 整屏截图 → 同流程
```
- niri 快捷键：`Ctrl+Alt+A`(区域) / `Ctrl+Alt+Shift+A`(整屏)
- 配置：`~/.config/ocrshot/config`，`SHOT_DIR` 设保存目录（默认 `~/Pictures/ScreenShot/ocr`，**别用 `~`**）

---

## appimage — AppImage 桌面集成

自动提取 AppImage 中的图标和 `.desktop` 文件，添加到应用程序菜单。

### 用法

```bash
appimage -i <AppImage文件路径>
```

### 示例

```bash
appimage -i ~/软件/some-app-x86_64.AppImage
```

脚本会自动：
1. 提取 AppImage
2. 找到图标和 `.desktop` 文件
3. 图标 → `~/.local/share/icons/`
4. `.desktop` → `~/.local/share/applications/`（自动修正 `Exec`、`Icon` 路径）

---

## coc — ~/.config 配置残留检查

扫描 `~/.config` 目录，找出已卸载软件留下的配置残留。

### 用法

```bash
coc                      # 扫描模式，列出可疑残留
coc --clean              # 扫描后交互式清理
coc --verbose            # 显示全部条目（包括正常的）
coc --json               # 输出 JSON 格式
coc --help               # 显示帮助
```

### 检测方式

- 映射表：配置目录名 ↔ 包名/命令名
- 包管理器：`pacman` / `dpkg` 查包是否安装
- AppImage：扫描 `~/软件/`、`~/Applications/` 等目录
- `.desktop`：检查 `/usr/share/applications`
- 特征识别：KDE `.rc` 文件、系统自动生成文件等

---

## systemctl-analysis — Systemd 服务分析

全面分析 systemd 服务的运行状态，生成可视化报告。

### 用法

```bash
systemctl-analysis                      # 终端输出（带颜色）
systemctl-analysis --output 报告.md      # 输出到 Markdown 文件
systemctl-analysis --json               # JSON 格式（需安装 jq）
systemctl-analysis --help               # 显示帮助
```

### 功能

| 功能 | 说明 |
|------|------|
| 运行中/失败/not-found/masked 统计 | 一键汇总 |
| 已启用服务列表 | 开机自启一览 |
| 定时器状态 | 下次执行时间 |
| 启动耗时分析 | systemd-analyze 数据 |
| 残留软链接检测 | 自动扫描 `.wants/` 目录坏链 |
| not-found 分类 | 🔴 **可清理**（坏链残留）vs 🟡 **无害**（系统包引用）|
| 清理建议 | 直接给出可执行的 `sudo rm` 命令 |

### not-found 分类说明

脚本会自动区分两类 not-found 服务：

- **🔴 可清理**：`multi-user.target.wants/` 中存在残留软链接，指向已卸载的服务文件。脚本会列出对应的坏链路径和删除命令。
- **🟡 无害**：被已安装的系统包（如 `libvirt`、`systemd` 等）通过 `Wants=` 软依赖引用，无法消除也不影响运行。脚本会标明引用来源。

### 示例

```bash
# 终端输出
systemctl-analysis

# 保存报告
systemctl-analysis -o ~/文档/服务报告.md

# 查看 JSON
systemctl-analysis --json | jq .summary
```

---

## gitpush — Git 自动提交推送工具

智能的 Git 自动 commit & push 脚本，支持单发和批量提交、冲突交互处理、远程仓库管理。

### 用法

```bash
gitpush                              # 提交默认文件夹（信息用时间戳）
gitpush /路径/项目                     # 提交指定路径
gitpush /路径/项目 "修复了xxx"         # 提交并写备注
gitpush --set-folder /路径            # 设置默认文件夹
gitpush --set-remote git@...          # 设置默认远程仓库
gitpush --pull                        # 拉取远程更新
gitpush --batch                       # 批量处理多个项目
gitpush --show                        # 查看当前配置
gitpush --help                        # 完整帮助
```

### 功能一览

| 功能 | 说明 |
|------|------|
| 自动 commit & push | 一键提交，信息可选，默认时间戳 |
| 批量处理 | 一个配置文件管理多个项目，逐一提交推送 |
| 冲突交互处理 | pull 分叉时弹菜单选 merge/rebase |
| push 被拒自动重试 | 被拒绝后自动拉取合并再推送 |
| 智能初始化 | 非 Git 仓库自动 `git init` + 配置远程 |
| 多层配置覆盖 | 默认 → 临时 `--remote/--user` → 显式 `--conf` |
| 跨平台 | Linux/Mac/Android（Termux）均可使用 |

### 详细说明

完整的使用指南见 [`gitpush-使用指南.md`](./gitpush-使用指南.md)，包含：

- 配置管理与配置文件路径控制
- 批量任务配置格式与回退规则
- 冲突处理流程详解（merge vs rebase）
- `--pull` 拉取模式说明
- 常见场景示例
- Android Termux 注意事项
