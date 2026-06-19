# gtlx-sh

个人常用脚本集合。

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
