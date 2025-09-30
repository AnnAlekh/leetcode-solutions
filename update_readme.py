#!/usr/bin/env python3
import json, re, datetime, os, requests

USER = "dumooroo"  # ← ваш ник
README = "README.md"

# 1. Забираем данные из публичного graphql-эндпоинта LeetCode
query = """
query getUserProfile($username: String!) {
  matchedUser(username: $username) {
    submitStats: submitStatsGlobal {
      acSubmissionNum {
        difficulty
        count
      }
    }
  }
}
"""
resp = requests.post(
    "https://leetcode.com/graphql",
    json={"query": query, "variables": {"username": USER}},
    timeout=30,
)
resp.raise_for_status()
data = resp.json()["data"]["matchedUser"]["submitStats"]["acSubmissionNum"]

stats = {item["difficulty"]: item["count"] for item in data}
total = sum(stats.values())

# 2. Формируем новую табличку
table = f"""| Показатель        | Значение |
|-------------------|----------|
| **Всего решено**  | {total}  |
| **Easy**          | {stats.get("Easy", 0)}   |
| **Medium**        | {stats.get("Medium", 0)} |
| **Hard**          | {stats.get("Hard", 0)}   |"""

# 3. Заменяем блок между маркерами
with open(README, encoding="utf-8") as f:
    content = f.read()

replacer = re.compile(
    r"<!--START_SECTION:leetcode-->.*?<!--END_SECTION:leetcode-->",
    re.DOTALL,
)
new_chunk = f"<!--START_SECTION:leetcode-->\n{table}\n<!--END_SECTION:leetcode-->"
content = replacer.sub(new_chunk, content)

# 4. Проставляем дату апдейта
content = re.sub(r"<last-update>", datetime.datetime.utcnow().strftime("%d %b %Y %H:%M UTC"), content)

with open(README, "w", encoding="utf-8") as f:
    f.write(content)