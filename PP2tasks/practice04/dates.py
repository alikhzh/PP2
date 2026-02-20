import datetime
#1
now = datetime.datetime.now()
print(now)
#2
from datetime import date

d1 = date(2026, 1, 1)
d2 = date(2025, 1, 1)

print((d1 - d2).days)
#3
today = datetime.datetime.now()
print(today.strftime("%Y-%m-%d"))
