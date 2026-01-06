"""
14) 파일 다운로드(스트리밍)
- 큰 파일은 한 번에 read()하지 말고 chunk로 저장
"""
from __future__ import annotations
import argparse, requests
from pathlib import Path


## https://ssl.pstatic.net/melona/libs/1546/1546753/8f91fb73f9e353e962f7_20251212175756607.jpg
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="https://www.example.com/")
    ap.add_argument("--out", default="reports/download.html")
    args = ap.parse_args()

    out = Path(args.out)
    out.parent.mkdir(exist_ok=True, parents=True)

    with requests.get(args.url, stream=True, timeout=5) as r:
        r.raise_for_status()
        with out.open("wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    print("saved:", out.resolve())

if __name__ == "__main__":
    main()
