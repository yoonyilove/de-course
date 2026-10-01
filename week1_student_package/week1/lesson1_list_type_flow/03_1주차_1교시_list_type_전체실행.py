"""1주차 1교시 전체 실행본: list와 type."""

import os


print(os.getcwd())

company_name = "하모니 결혼정보"
print(company_name)
print(type(company_name))

members = []
members.append({"id": "M001", "name": "김철수", "income": 8000, "age": 31})
members.extend([
    {"id": "M002", "name": "이영희", "income": 6500, "age": 34},
    {"id": "M003", "name": "박민수", "income": 8000, "age": 29},
])
print("현재 회원 수:", len(members))
print(type(members))

first_member = members[0]["name"]
latest_member = members[-1]["name"]
early_members = members[:2]
print("1호 가입자:", first_member)
print("최신 가입자:", latest_member)
print("초기 가입자 2명:", [member["name"] for member in early_members])

members.sort(key=lambda member: member["income"], reverse=True)
for member in members:
    print(
        f"ID: {member['id']} | 이름: {member['name']} | "
        f"연봉: {member['income']}"
    )

adult_users = [member for member in members if member["age"] >= 30]
formatted_names = [f"{member['name']}님" for member in members]
print("30대 이상 회원 수:", len(adult_users))
print(formatted_names)

incoming_member = {
    "id": "M004",
    "name": "최하늘",
    "income": "7200",
    "age": 32,
}
income = incoming_member["income"]
print("변환 전:", income, type(income))
if isinstance(income, str):
    incoming_member["income"] = int(income)
print("변환 후:", incoming_member["income"], type(incoming_member["income"]))

missing_income = None
print(missing_income, type(missing_income))

incoming_member["status"] = "상담대기"
print("추가 전 상태:", incoming_member["status"])
incoming_member["status"] = "상담완료"
members.append(incoming_member)
print("전체 회원 수:", len(members))
print("추가 회원 상태:", members[-1]["status"])
