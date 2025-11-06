# 智能零售商品识别系统

智能零售商品识别系统/
├── 📁 核心代码/
│   ├── app.py                          # Flask 后端主程序
│   ├── 1_解析商品名.py                 # 商品信息解析脚本
│   ├── 2_修改格式.py                   # 文件格式转换脚本
│   └── 📁 yolov5_master/               # YOLOv5 完整源码
│       ├── models/                     # 模型定义
│       ├── utils/                      # 工具模块
│       ├── data/                       # 数据配置
│       └── ... (其他YOLOv5文件)
├── 📁 静态资源/
│   ├── best.pt                         # YOLOv5 训练好的模型权重
│   ├── data.yaml                       # 数据集配置和类别信息
│   └── 📁 temp/                        # 测试图片目录
├── 📁 数据文件/
│   ├── product_prices_stock.csv        # 商品价格库存数据
│   └── user_accounts.csv               # 用户账号数据（原 Register&Login.csv）
├── 📁 前端页面/
│   └── 📁 templates/
│       ├── index.html                  # 主入口页面
│       ├── welcome.html                # 欢迎页面
│       ├── register_login.html         # 注册登录页面
│       ├── settlement.html             # 商品结算页面
│       └── price_management.html       # 价格管理页面
└── README.md                           # 项目说明文档

涵盖商品识别、动态结算及库存管理等核心业务场景
