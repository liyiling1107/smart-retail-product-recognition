import yaml
import csv
import random

# 路径设置
yaml_path = r"data.yaml"
csv_path = r"product_prices_stock.csv"

# 读取 YAML 文件
with open(yaml_path, 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

# 获取类别名称列表
names = data.get('names', [])

# 写入 CSV 文件
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['class_name', 'price', 'stock'])  # 表头
    for name in names:
        price = random.randint(1, 50)                # 随机价格：1~50
        stock = random.choice(range(10, 101, 10))    # 随机库存：10~100（步长为10）
        writer.writerow([name, price, stock])

print(f"已成功写入 {len(names)} 个类别到 CSV 文件：{csv_path}")


