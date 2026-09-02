#!/bin/bash
# server-backup.sh — 服务器数据备份到本机(两段式)
# 段1(服务器端): rsync 镜像 /root/gtlx/{Home,docker} -> /root/backup-mirror/
#   由 systemd 托管, 独立于会话, Hermes/电脑关闭不影响:
#     ssh yuyun 'systemd-run --collect --unit=backup-gtlx-mirror bash -c "rsync -a --exclude=.stversions --exclude=\"sync-conflict*\" --exclude=.syncthing.*.tmp /root/gtlx/Home /root/gtlx/docker /root/backup-mirror/; echo MIRROR-DONE > /tmp/backup-mirror.done"'
# 段2(本机): 本脚本拉取镜像到本机
# 用法: server-backup.sh --start   # 触发服务器端镜像(systemd-run 后台)
#       server-backup.sh           # 镜像完成后拉取到本机(默认 /home/gtlx/备份/服务器)
#       server-backup.sh /自定义目录
set -euo pipefail

SERVER="${SERVER:-yuyun}"
DEST="${1:-/home/gtlx/备份/服务器}"

if [ "${1:-}" = "--start" ]; then
  echo "==> 触发服务器端镜像(systemd 后台, 排除 .hermes)..."
  ssh "$SERVER" 'systemd-run --collect --unit=backup-gtlx-mirror /usr/local/bin/backup-gtlx-mirror.sh'
  echo "==> 已触发, 完成后本机执行: server-backup.sh 拉取"
  exit 0
fi

echo "==> 检查服务器镜像状态..."
if ! ssh "$SERVER" 'test -f /tmp/backup-mirror.done'; then
  echo "⚠ 服务器镜像未完成(或未触发)"
  echo "  先触发: server-backup.sh --start"
  echo "  或查看: ssh yuyun systemctl status backup-gtlx-mirror"
  exit 1
fi

mkdir -p "$DEST"
echo "==> 拉取: $SERVER:/root/backup-mirror/ -> $DEST/"
rsync -av --progress "$SERVER:/root/backup-mirror/" "$DEST/"
echo "==> 完成:"
du -sh "$DEST"
