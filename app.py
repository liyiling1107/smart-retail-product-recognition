import os
import sys
import torch
import numpy as np
import cv2
import csv
from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__, template_folder='templates')

# YOLOv5 模型路径
YOLOV5_PATH = os.path.join(os.path.dirname(__file__), 'yolov5_master')
sys.path.append(YOLOV5_PATH)

from yolov5_master.models.common import DetectMultiBackend
from yolov5_master.utils.general import non_max_suppression
from yolov5_master.utils.augmentations import letterbox


# 添加 scale_coords 函数
def scale_coords(img1_shape, coords, img0_shape, ratio_pad=None):
    if ratio_pad is None:
        gain = min(img1_shape[0] / img0_shape[0], img1_shape[1] / img0_shape[1])
        pad = ((img1_shape[1] - img0_shape[1] * gain) / 2,
               (img1_shape[0] - img0_shape[0] * gain) / 2)
    else:
        gain = ratio_pad[0][0]
        pad = ratio_pad[1]
    coords[:, [0, 2]] -= pad[0]
    coords[:, [1, 3]] -= pad[1]
    coords[:, :4] /= gain
    coords[:, :4] = coords[:, :4].clamp(min=0)
    return coords


# 模型和CSV路径
YOLOV5_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'best.pt')
PRODUCT_CSV_PATH = os.path.join(os.path.dirname(__file__), 'product_prices_stock.csv')
REGISTER_CSV_PATH = os.path.join(os.path.dirname(__file__), 'Register&Login.csv')


# 加载模型
def load_yolov5_model(model_path):
    try:
        model = DetectMultiBackend(weights=model_path, device='cpu', dnn=False, data=None, fp16=False, fuse=True)
        model.conf = 0.25
        return model
    except Exception as e:
        print(f"模型加载失败: {e}")
        return None


# 从CSV查找价格
def get_price_from_csv(label):
    try:
        with open(PRODUCT_CSV_PATH, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                if row['class_name'] == label:
                    return float(row['price'])
    except Exception as e:
        print(f"读取CSV失败: {e}")
    return None


# YOLO识别
def predict_image_yolov5(model, image_path):
    im0 = cv2.imread(image_path)
    img = letterbox(im0, 640, stride=32, auto=True)[0]
    img = img.transpose((2, 0, 1))[::-1]
    img = np.ascontiguousarray(img)

    img = torch.from_numpy(img).to(model.device).float() / 255.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    pred = model(img, augment=False, visualize=False)
    pred = non_max_suppression(pred, conf_thres=0.25, iou_thres=0.45)

    predictions = []
    for det in pred:
        if len(det):
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
            for *xyxy, conf, cls in det:
                label = model.names[int(cls)]
                price = get_price_from_csv(label)
                predictions.append({
                    'label': label,
                    'confidence': float(conf),
                    'price': price
                })

    return predictions


# 首页路由
@app.route('/')
def index():
    return render_template('index.html')


# 欢迎页面路由
@app.route('/Welcome.html')
def welcome():
    return render_template('Welcome.html')


# 商品结算页面路由
@app.route('/Settlement.html')
def settlement():
    return render_template('Settlement.html')


# 店员注册登录页面路由
@app.route('/Register&Login.html')
def register_login():
    return render_template('Register&Login.html')


# 价格管理页面路由
@app.route('/Price_management.html')
def price_management():
    return render_template('Price_management.html')


# 登录路由
@app.route('/login', methods=['POST'])
def login():
    data = request.form
    username = data.get('username')
    password = data.get('password')

    try:
        with open(REGISTER_CSV_PATH, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                if 'username' in row and 'password' in row:
                    if row['username'] == username and row['password'] == password:
                        return jsonify({'message': '登录成功'})  # 返回 JSON 响应
    except FileNotFoundError:
        return jsonify({'message': '登录失败，用户信息文件不存在'})
    except Exception as e:
        print(f"读取CSV文件失败: {e}")
        return jsonify({'message': '登录失败，系统错误'})

    return jsonify({'message': '登录失败，用户名或密码错误'})


# 注册路由
@app.route('/register', methods=['POST'])
def register():
    data = request.form
    username = data.get('username')
    password = data.get('password')

    # 检查用户名是否已存在
    try:
        with open(REGISTER_CSV_PATH, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                if row['username'] == username:
                    return jsonify({'message': '注册失败，用户名已存在'})
    except FileNotFoundError:
        # 如果文件不存在，创建文件
        pass

    # 将用户名和密码保存到 Register&Login.csv 文件中
    try:
        with open(REGISTER_CSV_PATH, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([username, password])
        return jsonify({'message': '注册成功'})
    except Exception as e:
        print(f"写入CSV文件失败: {e}")
        return jsonify({'message': '注册失败，系统错误'})


# 搜索商品路由
@app.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('search_term')
    results = {}

    try:
        with open(PRODUCT_CSV_PATH, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                if search_term.lower() in row['class_name'].lower():
                    results[row['class_name']] = {
                        'stock': row['stock'],
                        'price': row['price']
                    }
    except Exception as e:
        print(f"读取CSV文件失败: {e}")

    return jsonify(results)


# 图像预测路由
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': '未上传图片'}), 400
    image_file = request.files['image']
    if not os.path.exists('temp'):
        os.makedirs('temp')
    image_path = os.path.join('temp', image_file.filename)

    # 使用 with 语句确保文件被正确关闭
    with open(image_path, 'wb') as f:
        image_file.save(f)

    model = load_yolov5_model(YOLOV5_MODEL_PATH)
    if model is None:
        return jsonify({'error': '模型加载失败'}), 500

    predictions = predict_image_yolov5(model, image_path)
    try:
        os.remove(image_path)
    except Exception as e:
        print(f"删除文件失败: {e}")
    return jsonify({'predictions': predictions})


# 更新库存路由
@app.route('/update_stock', methods=['POST'])
def update_stock():
    data = request.json  # 获取前端发送的购物清单数据
    try:
        with open(PRODUCT_CSV_PATH, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=',')
            products = list(reader)  # 读取所有商品信息

        updated_products = []
        for product in products:
            for item in data:
                if product['class_name'] == item['label']:
                    product['stock'] = int(product['stock']) - 1  # 减少库存
                    break
            updated_products.append(product)

        # 将更新后的商品信息写回 CSV 文件
        with open(PRODUCT_CSV_PATH, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=['class_name', 'price', 'stock'])
            writer.writeheader()
            writer.writerows(updated_products)

        return jsonify({'message': '库存更新成功'})
    except Exception as e:
        print(f"更新库存失败: {e}")
        return jsonify({'message': '库存更新失败，系统错误'})

if __name__ == '__main__':
    app.run(debug=True)