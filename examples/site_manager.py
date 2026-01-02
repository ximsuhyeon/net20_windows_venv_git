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

def main():
    urls = load_sites()
    print(f"로딩 완료: {len(urls)}개")
    print("명령: add <url> | del <번호|url> | list | end")

    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            save_sites(urls)
            print(f"\n저장 완료: {IN_FILE}, {OUT_FILE} (총 {len(urls)}개)")
            break

        if not line:
            continue

        if line == "list":
            cmd_list(urls)
            continue

        if line.startswith("add "):
            u = normalize(line[4:])
            if not u:
                print("추가 실패: URL 형식이 이상함")
                continue
            if u in urls:
                print("이미 존재:", u)
                continue
            urls.append(u)
            print("추가됨:", u)
            continue

        if line.startswith("del "):
            arg = line[4:].strip()
            if arg.isdigit():
                idx = int(arg) - 1
                if 0 <= idx < len(urls):
                    print("삭제됨:", urls.pop(idx))
                else:
                    print("삭제 실패: 범위 밖 번호")
            else:
                u = normalize(arg)
                if u and u in urls:
                    urls.remove(u)
                    print("삭제됨:", u)
                else:
                    pr
