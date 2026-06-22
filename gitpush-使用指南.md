# Git 自动提交推送工具 使用指南

> 脚本位置：`gitpush.sh`  
> 配置文件：默认 `~/.gitpush.conf`（可自定义路径）

---

 ## 🚀 快速上手

 > ⚠️ **Android 用户注意**：由于 Android 的 sdcard 文件系统不支持 `chmod +x`，所有命令都必须用 `bash` 调用，例如 `bash gitpush.sh`，不能用 `./gitpush.sh`。

 ### 第一步：设置你的默认配置（只需一次）
 ```bash
 bash gitpush.sh --set-folder /storage/emulated/0/GTLX/Ai/TwitterClientApp
 bash gitpush.sh --set-remote git@github.com:你的用户名/仓库名.git
 bash gitpush.sh --set-user "你的Git名字"
 bash gitpush.sh --set-email "你的Git邮箱"
 ```

 ### 第二步：日常提交
 ```bash
 # 直接提交默认文件夹
 bash gitpush.sh "修了个bug"

 # 或者不写提交信息，自动用时间戳
 bash gitpush.sh
 ```

---

 ## 📖 完整命令列表

 | 命令 | 说明 |
 |------|------|
 | `bash gitpush.sh` | 提交默认文件夹（不写信息则用时间戳） |
 | `bash gitpush.sh "信息"` | 提交默认文件夹并写备注 |
 | `bash gitpush.sh /路径` | 提交指定路径（信息用时间戳） |
 | `bash gitpush.sh /路径 "信息"` | 提交指定路径并写备注 |
 | `bash gitpush.sh --show` | 查看当前默认配置 |
 | `bash gitpush.sh --help` | 显示帮助 |

 ---

 ## ⚙️ 配置管理

 | 命令 | 说明 |
 |------|------|
 | `bash gitpush.sh --set-folder <路径>` | 修改默认文件夹 |
 | `bash gitpush.sh --set-remote <url>` | 修改默认远程仓库地址 |
 | `bash gitpush.sh --set-user <用户名>` | 修改默认提交用户名 |
 | `bash gitpush.sh --set-email <邮箱>` | 修改默认提交邮箱 |
 | `bash gitpush.sh --set-conf <路径>` | 永久修改默认配置文件路径 |

---

## 📂 配置文件路径控制（新功能）

 永久更改配置文件位置
 默认配置保存在 `~/.gitpush.conf`。如果你想把配置文件放到脚本同目录，方便备份和迁移：

 ```bash
 # 永久改为脚本同目录的 gitpush.conf
 bash gitpush.sh --set-conf ./gitpush.conf
 ```

 之后所有 `--set-*` 修改都会写进你指定的配置文件。

 ### 临时使用另一个配置文件
 不改变默认路径，只是本次读取另一个配置：

 ```bash
 # 本次用项目专属配置，不影响默认设定
 bash gitpush.sh --conf /path/to/project.conf
 ```

 ### 检查当前使用的配置文件
 ```bash
 bash gitpush.sh --show
 # 会显示「配置文件   : /当前/使用的/路径」
 ```

---

 ## 🔧 高级：临时覆盖配置

 有时你只想对本次提交换一个远程仓库或用户名，不改变默认配置：

 ```bash
 bash gitpush.sh --remote git@github.com:临时仓库.git "用了临时仓库"
 bash gitpush.sh --user "临时名字" --email "临时@邮箱"
 ```

 临时参数优先级高于默认配置，用完即弃，不会存到配置文件。

---

## ⬇️ 拉取远程更新

从 v2.3 开始，脚本支持 `--pull` 拉取模式，并会在分支冲突时弹菜单让你选择处理策略。

### 命令

```bash
bash gitpush.sh --pull                    # 拉取默认仓库的当前分支
bash gitpush.sh --pull <文件夹>           # 拉取指定文件夹所在仓库
bash gitpush.sh --pull <文件夹> <分支名>  # 拉取指定仓库的指定分支
```

### 冲突处理：merge vs rebase

当本地和远程分支产生分叉时，脚本会弹出菜单让你选：

- **[1] merge（合并）**：把远程内容和本地内容合在一起，保留双方的分叉历史，会产生一个额外的"合并提交"。结果是两条线汇合，留有合并记录。
- **[2] rebase（变基）**：把你的本地提交"拆下来"，接到远程最新提交的后面，历史变成一条直线。结果是看起来你是在远程更新之后才提交的，分叉痕迹被抹平。

> ⚠️ **都是"远程→本地"的拉取操作**，不是推送方向。两者区别在于拼接历史的方式，merge 留分叉痕迹，rebase 让历史更线性整洁。

### 流程说明

1. 先 `git fetch` 获取远程最新信息
2. 如果远程没有新东西 → 提示「已是最新」
3. 如果本地落后且可快进 → 直接拉取
4. 如果分支分叉 → 弹出菜单让你选 merge / rebase / 放弃
5. push 被拒绝时 → 自动问「要先拉取吗？」→ 走上述流程 → 拉完自动重推

---

## 📦 批量处理（新功能）

从 v2.3 开始，脚本支持 `--batch` 模式，一次处理多个项目。

### 命令

```bash
bash gitpush.sh --batch <配置文件>
```

### 批量配置文件格式

每行一个任务，用竖线 `|` 分隔字段：

```
文件夹路径|远程URL|分支|提交信息
```

- 空行和 `#` 开头的行会被忽略
- **只有文件夹路径是必填的**，其他三个字段都可以留空

**字段留空时的回退规则：**

| 留空字段 | 回退值 |
|----------|--------|
| 远程URL | 配置文件里的 `DEFAULT_REMOTE` |
| 分支 | 当前仓库所在分支（取不到就用 `main`） |
| 提交信息 | 自动生成时间戳（格式 `Auto commit YYYY-MM-DD HH:MM:SS`） |

所以最简单的写法只需要一行一个路径：
```
项目A文件夹
项目B文件夹|||
项目C文件夹||dev|
项目D文件夹|git@gitee.com:me/other.git||修复了个bug
```

### ♻️ 和单发用同一个配置文件

**不需要单独创建批量配置文件！** 批量任务可以直接写在你日常提交用的配置文件（如脚本旁的 `gitpush.conf`）里，和全局变量混着写互不干扰：

```bash
# ===== 全局默认值（单发也生效）=====
DEFAULT_FOLDER="/storage/emulated/0/GTLX/Ai/TwitterClientApp"
DEFAULT_REMOTE="git@github.com:me/main.git"
DEFAULT_USER="张三"
DEFAULT_EMAIL="zhang@example.com"

# ===== 批量任务（以下是会被 --batch 执行的）=====
projectA|||
projectB|git@gitee.com:me/backup.git||
projectC||dev|feat: 新功能开发
```

- 没有 `|` 的行（如 `DEFAULT_*` 变量定义）不会被当成任务
- `bash gitpush.sh "日常提交"` → 走单发逻辑，提交 `DEFAULT_FOLDER`
- `bash gitpush.sh --batch` → 走批量逻辑，执行下面那三个任务
- 一举两得，不用切配置文件 ✨

### 配置示例（独立批量文件也支持）

```bash
# 项目A：推送到 GitHub（全字段指定）
/storage/emulated/0/GTLX/Ai/TwitterClientApp|git@github.com:me/twitter.git|main|修复登录bug

# 项目B：只填文件夹和分支，远程用默认
/storage/emulated/0/GTLX/Ai/TwitterExporter||master|

# 项目C：只填文件夹，全回退（远程/分支/信息全自动）
/storage/emulated/0/GTLX/Ai/gitpush|||
```

### 注意事项

- 每行独立处理，一个项目失败不影响后续项目
- 每个项目都会走完整的冲突检测交互流程（pull 分叉弹菜单、push 被拒自动拉取重推）
- 进度和结果会逐行打印，方便排查
- **不指定配置文件时**，`--batch` 自动用当前生效的配置文件（优先脚本旁 `gitpush.conf`，否则 `~/.gitpush.conf`）

---

## 🤖 自动初始化仓库

如果目标文件夹还不是 Git 仓库，脚本会自动帮你初始化：

1. 执行 `git init`
2. 用你配置的远程地址执行 `git remote add origin`
3. 用你配置的用户名/邮箱执行 `git config user.name / user.email`
4. 第一次提交后自动创建 `main` 分支并推送

这样哪怕是一个全新文件夹，第一次运行也能直接推送到远程仓库。

---

 ## 📋 常见场景示例

 ```bash
 # 场景1：第一次用，初始化一切
 bash gitpush.sh --set-folder /home/me/project
 bash gitpush.sh --set-remote git@github.com:me/project.git
 bash gitpush.sh --set-user "张三" --set-email "zhang@example.com"
 bash gitpush.sh "首次提交"

 # 场景2：日常提交
 bash gitpush.sh "修复登录页闪退"

 # 场景3：看看当前配置了啥（含配置文件路径）
 bash gitpush.sh --show

 # 场景4：临时交个别的文件夹
 bash gitpush.sh /tmp/another-project "临时改了点东西"

 # 场景5：只想初始化仓库，不推远程
 # （不设 remote 配置就行，脚本会跳过 push）

 # 场景6：多个项目用不同配置文件
 bash gitpush.sh --conf ./projectA.conf
 bash gitpush.sh --conf ./projectB.conf

 # 场景7：把配置文件跟脚本放在一起
 bash gitpush.sh --set-conf ./gitpush.conf
 bash gitpush.sh --set-folder /path/to/project
 # 以后所有配置都写进当前目录的 gitpush.conf
 ```

---

## 📄 配置文件格式

配置文件的完整格式如下（可手改）：

```bash
DEFAULT_FOLDER="/你的/默认/文件夹"
DEFAULT_REMOTE="git@github.com:用户名/仓库.git"
DEFAULT_USER="你的名字"
DEFAULT_EMAIL="you@email.com"
```

---

## ⚠️ 前提条件

- 系统已安装 `git`
- 远程仓库已创建好（GitHub/Gitee 等）
- 如果用 SSH 地址，已配好 SSH Key

---

> 💡 提示：脚本可以放在系统 PATH 里的任何地方（如 `/usr/local/bin`），\
> 这样在任意目录下都能直接调用 `gitpush.sh`，不用敲完整路径。