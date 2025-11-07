import csv
import os

# 原始文件路径
original_file_path = r"product_prices_stock.csv"
# 临时文件路径
temp_file_path = r"product_prices_stock_temp.csv"

def ensure_utf8_csv(file_path, temp_file_path):
    try:
        # 尝试以 UTF-8 编码读取文件
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)
        print("文件已经是 UTF-8 编码，无需转换。")
    except UnicodeDecodeError:
        # 如果读取失败，尝试以其他编码读取（如 GBK）
        try:
            with open(file_path, 'r', encoding='gbk') as file:
                reader = csv.reader(file)
                rows = list(reader)
            print("文件以 GBK 编码读取成功，将转换为 UTF-8 编码。")
        except UnicodeDecodeError:
            print("无法识别文件编码，请检查文件内容。")
            return

    # 将内容以 UTF-8 编码写入临时文件
    with open(temp_file_path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    print(f"文件已以 UTF-8 编码保存到 {temp_file_path}")

    # 替换原文件
    os.replace(temp_file_path, file_path)
    print(f"原文件已替换为 UTF-8 编码的文件：{file_path}")

# 调用函数
ensure_utf8_csv(original_file_path, temp_file_path)