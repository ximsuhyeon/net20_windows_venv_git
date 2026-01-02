from __future__ import annotations
from pathlib import Path
from urllib.parse import urlparse

IN_FILE = "sites.txt"
OUT_FILE = "cleaned_sites.txt"

def normalize(line: str) -> str | None:
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if "://" not in line:
        line = "https://" + line
    p = urlparse(line)
    if not p.netloc:
        return None
    scheme = (p.scheme or "https").lower()
    netloc = p.netloc.lower()
    path = p.path if p.path else "/"
    return p._replace(scheme=scheme, netloc=netloc, path=path, params="", query="", fragment="").geturl()

def load_sites() -> list[str]:
    p = Path.cwd() / IN_FILE
    if not p.exists():
        return []
    lines = p.read_text(encoding="utf-8").splitlines()
    urls, seen = [], set()
    for raw in lines:
        u = normalize(raw)
        if not u or u in seen:
            continue
        seen.add(u)
        urls.append(u)
    return urls

def save_sites(urls: list[str]) -> None:
    (Path.cwd() / IN_FILE).write_text("\n".join(urls) + ("\n" if urls else ""), encoding="utf-8", newline="\n")
    (Path.cwd() / OUT_FILE).write_text("\n".join(urls) + ("\n" if urls else ""), encoding="utf-8", newline="\n")

def cmd_list(urls: list[str]) -> None:
    if not urls:
        print("(비어있음)")
        return
    for i, u in enumerate(urls, start=1):
        print(f"{i:02d}. {u}")

def main() -> None:
    urls = load_sites()
    print(f"로딩 완료: {len(urls)}개")
    print("명령: add <url> | del <번호|url> | list | end")

    while True:
    try:
        line = input("> ").strip()
    except (EOFError, KeyboardInterrupt):
        # Ctrl+C 또는 입력 종료 시에도 저장하고 종료
        save_sites(urls)
        print(f"\n저장 완료: {IN_FILE}, {OUT_FILE} (총 {len(urls)}개)")
        break

    if not line:
        continue

    if line == "list":
        cmd_list(urls)
        continue

    if line.startswith("add "):
        cmd_add(urls, line[4:])
        continue

    if line.startswith("del "):
        cmd_del(urls, line[4:])
        continue

    if line == "end":
        save_sites(urls)
        print(f"저장 완료: {IN_FILE}, {OUT_FILE} (총 {len(urls)}개)")
        break

    print("알 수 없는 명령. 사용: add/del/list/end")

