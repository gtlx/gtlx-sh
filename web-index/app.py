#!/usr/bin/env python3
"""
gtlx-sh Web 索引 — 列出所有脚本、看说明、可执行。
后端: FastAPI。
用法: web-index/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 8123
"""
from __future__ import annotations

import re
import shlex
import subprocess
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

GTLX_SH = Path.home() / "项目/code/gtlx-sh"

app = FastAPI(title="gtlx-sh 脚本索引", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FLAGS = ("#!/usr/bin/env bash", "#!/bin/bash")


def is_script(f: Path) -> bool:
    """是否为可执行脚本(排除 .venv/.git 及文档)。"""
    parts = f.parts
    if any(p in (".git", ".venv", "venv", "node_modules", "__pycache__") for p in parts):
        return False
    if f.name.startswith(".") or f.name.endswith((".pyc", ".so")):
        return False
    ext = f.suffix
    if ext in (".md", ".txt", ".png", ".pyc", ".bak"):
        return False
    # 脚本特征: shebang 或可执行位
    try:
        head = f.open(encoding="utf-8", errors="ignore").read(120)
    except OSError:
        return False
    return any(head.startswith(s) for s in FLAGS) or f.stat().st_mode & 0o111 != 0


def parse_doc(f: Path) -> dict:
    """解析脚本头部: 标题行 + 用途说明 + 用法示例(前若干)"""
    try:
        lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return {"name": f.name, "title": "", "desc": "", "usage": []}

    # 去掉前导 shebang 和版权头
    i = 0
    while i < len(lines) and (lines[i].startswith("#!") or lines[i].startswith("# Copyright")
                              or lines[i].startswith("# SPDX") or lines[i].strip() == "#"):
        i += 1
    head = lines[i:]

    title = ""
    desc_lines = []
    usage = []
    for ln in head:
        s = ln.strip()
        if s.startswith("##") or s.startswith("#") or s.startswith("==="):
            t = s.lstrip("#=- \t")
            if not title and t:
                title = t.split("—")[0].split("-")[0].strip() or t
            else:
                desc_lines.append(t)
        elif s.startswith("用法:") or s.startswith("用法") or "usage" in s.lower():
            usage.append(s)
        elif s.startswith(("ocr", "ocrshot", "syscheck", "coc", "appimage", "gitpush",
                           "restic", "server-backup", "systemctl-analysis")) and len(s) < 60:
            usage.append(s)
        elif not s:
            break  # 遇到空行，头部说明结束
    return {
        "name": f.name,
        "title": title or f.name,
        "desc": "\n".join(desc_lines[:6]),
        "usage": usage[:6],
    }


@app.get("/api/scripts")
def list_scripts():
    """列出 gtlx-sh 下所有脚本(按目录分组)"""
    groups: dict[str, list] = {}
    groups["根目录"] = []
    for d in sorted([p for p in GTLX_SH.iterdir() if p.is_dir() and not p.name.startswith(".")]):
        groups[d.name] = []
    for f in GTLX_SH.rglob("*"):
        if f.is_file() and is_script(f):
            rel = f.relative_to(GTLX_SH)
            parent = str(rel.parent) if rel.parent != Path(".") else "根目录"
            groups.setdefault(parent, []).append(parse_doc(f))
    # 去空分组
    return {"path": str(GTLX_SH), "groups": {k: v for k, v in groups.items() if v}}


class RunReq(BaseModel):
    path: str  # 相对 gtlx-sh 的路径


@app.post("/api/run")
def run_script(req: RunReq):
    """运行脚本(仅限 gtlx-sh 内路径, 防目录穿越)"""
    full = (GTLX_SH / req.path).resolve()
    if not str(full).startswith(str(GTLX_SH)):
        raise HTTPException(400, "路径越界")
    if not full.is_file() or not is_script(full):
        raise HTTPException(404, "非脚本")
    cmd = [str(full)]
    # 超时 60s, 返回合并输出
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=60,
                           cwd=str(GTLX_SH))
        return {"exit": p.returncode, "stdout": p.stdout[-2000:], "stderr": p.stderr[-1000:]}
    except subprocess.TimeoutExpired:
        return {"exit": -1, "stdout": "(超时60s)", "stderr": ""}


@app.get("/")
def index():
    return FileResponse(Path(__file__).parent / "index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8123)