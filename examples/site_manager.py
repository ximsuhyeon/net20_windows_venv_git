from pathlib import Path
from urllib.parse import urlparse

IN_FILE = "sites.txt"
OUT_FILE = "cleaned_sites.txt"


def normalize(line: str):
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
    return p._replace(
        scheme=scheme,
        netloc=netloc,
        path=path,
        params="",
        query="",
        fragment=""
    ).geturl()


def load_sites():
    p = Path.cwd() / IN_FILE
    if not p.exists():
        return []
    lines = p.read_text(encoding="utf-8").splitlines()
    urls = []
    seen = set()
    for raw in lines:
        u = normalize(raw)
        if u and u not in seen:
            seen.add(u)
            urls.append(u)
    return urls


def save_sites(urls):
    (Path.cwd() / IN_FILE).write_text(
        "\n".join(urls) + ("\n" if urls else ""),
        encoding="utf-8",
        newline="\n"
    )
    (Path.cwd() / OUT_FILE).write_text(
        "\n".join(urls) + ("\n" if urls else ""),
        encoding="utf-8",
        newline="\n"
    )


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
            for i, u in enumerate(urls, start=1):
                print(f"{i:02d}. {u}")
            continue

        if line.startswith("add "):
            u = normalize(line[4:])
            if not u:
                print("추가 실패: URL 형식 오류")
            elif u in urls:
                print("이미 존재:", u)
            else:
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
                    print("삭제 실패: 번호 범위 오류")
            else:
                u = normalize(arg)
                if u in urls:
                    urls.remove(u)
                    print("삭제됨:", u)
                else:
                    print("삭제 실패: 목록에 없음")
            continue

        if line == "end":
            save_sites(urls)
            print(f"저장 완료: {IN_FILE}, {OUT_FILE} (총 {len(urls)}개)")
            break

        print("알 수 없는 명령. 사용: add/del/list/end")


if __name__ == "__main__":
    main()