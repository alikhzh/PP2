import json
import os

# Получаем путь к текущему файлу
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "sample-data.json")

# Открываем JSON файл
with open(file_path, "r") as file:
    data = json.load(file)

# Заголовок таблицы
print("Interface Status")
print("=" * 80)
print(f"{'DN':50} {'Description':20} {'Speed':8} {'MTU':6}")
print("-" * 80)

# Перебираем интерфейсы и выводим строки
for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]

    dn = attributes.get("dn", "")
    descr = attributes.get("descr", "")
    speed = attributes.get("speed", "")
    mtu = attributes.get("mtu", "")

    print(f"{dn:50} {descr:20} {speed:8} {mtu:6}")
