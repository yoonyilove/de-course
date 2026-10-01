"""1주차 2교시 전체 실행본: 조건·반복·함수."""

members = [
    {
        "member_id": "M001", "name": "김철수", "age": 38,
        "is_profile_active": True,
        "weekly_logins_raw": ["2", "3", "2", "1"]
    },
    {
        "member_id": "M002", "name": "이영희", "age": 34,
        "is_profile_active": False,
        "weekly_logins_raw": ["1", "0", "1", "0"]
    },
    {
        "member_id": "M003", "name": "박민수", "age": 36,
        "is_profile_active": True,
        "weekly_logins_raw": ["1", "2", "4", "3"]
    },
    {
        "member_id": "M004", "name": "최하늘", "age": 31,
        "is_profile_active": False,
        "weekly_logins_raw": ["1", "0", "0", "1"]
    },
]

print("준비된 회원 수:", len(members))
print("첫 회원:", members[0]["name"], members[0]["weekly_logins_raw"])


def activity_level(login_counts, high_boundary=10, medium_boundary=5):
    """문자열 로그인 횟수를 합산하고 (합계, 등급)을 반환한다."""
    total = sum(int(x) for x in login_counts)
    if total >= high_boundary:
        level = "활발"
    elif total >= medium_boundary:
        level = "보통"
    else:
        level = "낮음"
    return total, level

def consultation_priority(member):
    """활성 프로필이며 로그인 합계가 5 이상이면 상담우선을 반환한다."""
    total, _ = activity_level(member["weekly_logins_raw"])
    if member["is_profile_active"] and total >= 5:
        return "상담우선"
    return "일반"

reports = []
for member in members:
    total, level = activity_level(member["weekly_logins_raw"])
    reports.append({
        "member_id": member["member_id"],
        "name": member["name"],
        "login_total": total,
        "activity_level": level,
        "consultation_priority": consultation_priority(member),
    })

print("\n활동 수준 분류 보고서")
for index in range(len(reports)):
    report = reports[index]
    print(
        str(index + 1) + "번 " + report["name"] + "님: "
        + report["activity_level"] + " / " + report["consultation_priority"]
    )

assert [r["login_total"] for r in reports] == [8, 2, 10, 2]
assert [r["activity_level"] for r in reports] == ["보통", "낮음", "활발", "낮음"]
assert [r["consultation_priority"] for r in reports] == ["상담우선", "일반", "상담우선", "일반"]
print("\n검증 완료: 예상 합계·등급·상담우선 결과가 모두 일치합니다.")
