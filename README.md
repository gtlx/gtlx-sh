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
