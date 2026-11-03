#!/usr/bin/env python3
"""Собрать совместимый пакет для Codex 0.161 из общего пакета TGParse."""

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "plugins" / "tgparse"
TARGET = ROOT / "plugins" / "tgparse-codex"


def package_files():
    manifest = json.loads((SOURCE / "plugin.json").read_text())
    overlay = manifest["extensions"]["com.openai"]
    legacy = {key: value for key, value in manifest.items()
              if key not in ("$schema", "extensions")}
    legacy.update(skills="./skills/", mcpServers="./.mcp.json",
                  interface=overlay["interface"])
    files = {Path(".codex-plugin/plugin.json"):
             (json.dumps(legacy, ensure_ascii=False, indent=2) + "\n").encode()}
    for path in SOURCE.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(SOURCE)
        if relative.parts[0] in ("plugin.json", "mcp.json", ".claude-plugin"):
            continue
        files[relative] = path.read_bytes()
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="Проверить синхронизацию, не изменяя файлы")
    args = parser.parse_args()
    expected = package_files()
    actual = {path.relative_to(TARGET): path.read_bytes()
              for path in TARGET.rglob("*") if path.is_file()}
    if args.check:
        if actual != expected:
            parser.exit(1, "Совместимый пакет устарел: запустите scripts/build_codex_compat.py\n")
        print("Совместимый пакет синхронизирован")
        return
    # Удаляем только устаревшие файлы внутри выделенной папки сборки.
    for relative in actual.keys() - expected.keys():
        (TARGET / relative).unlink()
    for relative, content in expected.items():
        path = TARGET / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    print("Совместимый пакет собран: plugins/tgparse-codex")


if __name__ == "__main__":
    main()
