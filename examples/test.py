print("=== 나눗셈 프로그램 시작 ===")

try:
    num = int(input("숫자를 하나 입력하세요: "))
    print("✔ 입력값을 숫자로 변환 성공")

    result = 10 / num
    print("✔ 나눗셈 계산 성공")

except ValueError:
    print("❌ 숫자가 아닌 값을 입력했습니다 (ValueError)")

except ZeroDivisionError:
    print("❌ 0으로 나눌 수 없습니다 (ZeroDivisionError)")

else:
    print("✅ 최종 결과:", result)

finally:
    print("=== 프로그램 종료 ===")