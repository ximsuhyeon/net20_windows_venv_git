from pathlib import Path
from urllib.parse import urlparse

IN_FILE = "sites.txt"
OUT_FILE = "cleaned_sites.txt"


def normalize(url: str):
    url = url.strip()
    if not url:
        return None
    if "://" not in url:
        url = "https://" + url

    p = urlparse(url)
    if not p.netloc:
        return None

    return p._replace(
        scheme=p.scheme.lower(),
        netloc=p.netloc.lower(),
        path=p.path if p.path else "/",
        params="",
        query="",
        fragment=""
    ).geturl()


def load_sites():
    p = Path(IN_FILE)
    if not p.exists():
        return []

    urls = []
    seen = set()
    for line in p.read_text(encoding="utf-8").splitlines():
        u = normalize(line)
        if u and u not in seen:
            seen.add(u)
            urls.append(u)
    return urls


def save_sites(urls):
    content = "\n".join(urls) + ("\n" if urls else "")
    Path(IN_FILE).write_text(content, encoding="utf-8")
    Path(OUT_FILE).write_text(content, encoding="utf-8")


def show_list(urls):
    print("\n[현재 사이트 목록]")
    if not urls:
        print("(비어있음)")
    else:
        for i, u in enumerate(urls, start=1):
            print(f"{i}) {u}")


def main():
    urls = load_sites()

    while True:
        show_list(urls)
        print("\n메뉴 선택")
        print("1. 추가")
        print("2. 삭제")
        print("3. 종료")

        choice = input("선택 >> ").strip()

        # 1️⃣ 추가
        if choice == "1":
            raw = input("추가할 URL 입력: ").strip()
            u = normalize(raw)
            if not u:
                print("URL 형식 오류")
            elif u in urls:
                print("이미 존재하는 URL")
            else:
                urls.append(u)
                print("추가 완료")

        # 2️⃣ 삭제
        elif choice == "2":
            if not urls:
                print("삭제할 항목이 없습니다")
                continue

            num = input("삭제할 번호 입력: ").strip()
            if not num.isdigit():
                print("숫자만 입력하세요")
                continue

            idx = int(num) - 1
            if idx < 0 or idx >= len(urls):
                print("번호 범위 오류")
            else:
                removed = urls.pop(idx)
                print(f"삭제 완료: {removed}")

        # 3️⃣ 종료
        elif choice == "3":
            save_sites(urls)
            print("저장 후 종료합니다")
            break

        else:
            print("잘못된 선택입니다 (1~3)")


if __name__ == "__main__":
    main()