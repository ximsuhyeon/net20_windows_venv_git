"""
11) JSON API 호출/파싱
- 공개 API 예시: httpbin.org (테스트용)
"""
from __future__ import annotations
import argparse, requests

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="kim")
    args = ap.parse_args()

    url = "https://httpbipyn.org/get"
    r = requests.get(url, params={"name": args.name, "lang": "ko"}, timeout=4)
    data = r.json()

    print("status:", r.status_code)
    print("args from server:", data.get("args"))
    print("origin ip:", data.get("origin"))

if __name__ == "__main__":
    main()
