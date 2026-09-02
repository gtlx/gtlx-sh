#!/usr/bin/env bash
#
# Copyright (C) 2026 gtlx
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# web-index — 启动 gtlx-sh 脚本索引服务
# 用法: web-index/start.sh [端口(默认8123)]
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${1:-8123}"

# 首次运行: 创建 venv + 装依赖
if [ ! -x "$DIR/.venv/bin/uvicorn" ]; then
  echo "→ 首次运行, 创建 venv 并安装依赖..."
  python3 -m venv "$DIR/.venv"
  "$DIR/.venv/bin/pip" install --quiet -r "$DIR/requirements.txt"
  chmod +x "$DIR/.venv/bin/uvicorn"
fi

echo "→ gtlx-sh 脚本索引: http://127.0.0.1:$PORT"
# 起服务后自动打开浏览器(后台,不阻塞服务)
( sleep 0.5; xdg-open "http://127.0.0.1:$PORT" >/dev/null 2>&1 ) &
cd "$DIR"
exec "$DIR/.venv/bin/uvicorn" app:app --host 127.0.0.1 --port "$PORT"