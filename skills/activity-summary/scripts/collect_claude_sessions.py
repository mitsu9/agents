#!/usr/bin/env python3
"""
Claude Code の会話履歴から指定日のセッションを収集し、要約用データを出力する。

Usage:
    python collect_claude_sessions.py [--date YYYY-MM-DD] [--claude-dir ~/.claude]

Output (JSON):
    {
        "date": "2026-03-09",
        "sessions": [
            {
                "session_id": "abc123",
                "project": "work-cockpit",
                "start_time": "2026-03-09T09:00:00Z",
                "end_time": "2026-03-09T10:30:00Z",
                "messages": [
                    {"role": "user", "timestamp": "...", "text": "..."},
                    {"role": "assistant", "timestamp": "...", "text": "..."}
                ]
            }
        ]
    }
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Collect Claude Code sessions for a given date")
    parser.add_argument("--date", default=None, help="Target date (YYYY-MM-DD). Defaults to today.")
    parser.add_argument("--claude-dir", default=os.path.expanduser("~/.claude"), help="Claude config directory")
    return parser.parse_args()


def extract_text_from_content(content):
    """メッセージの content からテキスト部分だけを抽出する。"""
    if isinstance(content, str):
        # system-reminder や command タグを除外
        if content.startswith("<system-reminder>") or content.startswith("<command"):
            return None
        return content
    if isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                text = block["text"]
                # system-reminder や command タグを除外
                if text.startswith("<system-reminder>") or text.startswith("<command"):
                    continue
                texts.append(text)
        return "\n".join(texts) if texts else None
    return None


def parse_session_file(filepath, target_date):
    """セッション JSONL ファイルをパースし、対象日のメッセージを抽出する。"""
    messages = []
    has_target_date = False

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # user/assistant メッセージのみ対象
                msg_type = data.get("type")
                if msg_type not in ("user", "assistant"):
                    continue

                # isMeta はスキップ
                if data.get("isMeta"):
                    continue

                timestamp_str = data.get("timestamp", "")
                if not timestamp_str:
                    continue

                # 日付フィルタ
                try:
                    ts = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                    msg_date = ts.strftime("%Y-%m-%d")
                except (ValueError, AttributeError):
                    continue

                if msg_date != target_date:
                    continue

                has_target_date = True

                # メッセージテキスト抽出
                message = data.get("message", {})
                role = message.get("role", msg_type)
                text = extract_text_from_content(message.get("content", ""))

                if text and len(text.strip()) > 0:
                    # 長すぎるメッセージは切り詰め（ツール結果等）
                    if len(text) > 2000:
                        text = text[:2000] + "... (truncated)"
                    messages.append({
                        "role": role,
                        "timestamp": timestamp_str,
                        "text": text.strip(),
                    })
    except (OSError, PermissionError):
        return None

    if not has_target_date:
        return None

    return messages


def project_name_from_dir(dirname):
    """プロジェクトディレクトリ名からリポジトリ名を推定する。"""
    # 例: -Users-mitsunobu-homma--ghq-github-com-mitsu9-work-cockpit → work-cockpit
    parts = dirname.split("-")
    # 末尾から意味のある部分を取る
    # github-com-org-repo パターンを探す
    full = dirname.replace("-", "/")
    if "github/com/" in full:
        after_github = full.split("github/com/")[-1]
        segments = [s for s in after_github.split("/") if s]
        if len(segments) >= 2:
            return f"{segments[-2]}/{segments[-1]}"
        elif segments:
            return segments[-1]
    # フォールバック: 最後の意味のある部分
    return dirname.rsplit("-", 1)[-1] if dirname else dirname


def collect_sessions(claude_dir, target_date):
    """全プロジェクトから対象日のセッションを収集する。"""
    projects_dir = Path(claude_dir) / "projects"
    if not projects_dir.exists():
        return []

    sessions = []

    for project_dir in projects_dir.iterdir():
        if not project_dir.is_dir():
            continue

        project_name = project_name_from_dir(project_dir.name)

        for session_file in project_dir.glob("*.jsonl"):
            session_id = session_file.stem
            messages = parse_session_file(session_file, target_date)

            if messages is None or len(messages) == 0:
                continue

            # タイムスタンプでソート
            messages.sort(key=lambda m: m["timestamp"])

            sessions.append({
                "session_id": session_id,
                "project": project_name,
                "start_time": messages[0]["timestamp"],
                "end_time": messages[-1]["timestamp"],
                "message_count": len(messages),
                "messages": messages,
            })

    # 開始時刻でソート
    sessions.sort(key=lambda s: s["start_time"])
    return sessions


def main():
    args = parse_args()

    if args.date:
        target_date = args.date
    else:
        target_date = datetime.now().strftime("%Y-%m-%d")

    sessions = collect_sessions(args.claude_dir, target_date)

    output = {
        "date": target_date,
        "session_count": len(sessions),
        "sessions": sessions,
    }

    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
