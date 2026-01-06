import requests

url = "https://httpbin.org/get"
params = {"name": "xim", "lang": "ko"}
r = requests.get(url, params=params, timeout=4)

print("status:", r.status_code)
print(r.url)           # 실제 요청 URL 확인
print(r.json()["args"]) # 서버가 받은 파라미터
