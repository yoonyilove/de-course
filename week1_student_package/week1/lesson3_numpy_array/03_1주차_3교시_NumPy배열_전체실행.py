"""1주차 3교시 전체 실행본: NumPy 배열."""

import numpy as np
member_names = ["김철수", "이영희", "박민수", "최하늘"]
login_matrix = np.array([[2,3,2,1],[1,0,1,0],[1,2,4,3],[1,0,0,1]])
print(login_matrix.shape, login_matrix.ndim, login_matrix.dtype)
print(login_matrix[2, :], login_matrix[:, 2])
print(login_matrix[0:2, 2:4])
print(login_matrix.mean(axis=0), login_matrix.mean(axis=1))
totals = login_matrix.sum(axis=1)
print(np.where(totals >= 10, "우선", np.where(totals >= 5, "관찰", "낮음")))
last_two = login_matrix[:, 2:4]
recent = np.where(last_two.sum(axis=1) >= 5, "최근활발", "일반")
print(list(zip(member_names, recent)))
assert recent.tolist() == ["일반","일반","최근활발","일반"]
