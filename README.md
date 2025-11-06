# 智能零售商品识别系统

项目概述：智能零售商品识别系统项目涵盖商品识别、动态结算及库存管理等核心业务场景。

智能零售商品识别系统/
├── README.md                           # 项目说明文档
│
├── 📁 templates/
│   ├── index.html                  # 主入口页面
│   ├── welcome.html                # 欢迎页面
│   ├── register_login.html         # 注册登录页面
│   ├── settlement.html             # 商品结算页面
│   └── price_management.html       # 价格管理页面
│
├── 📁 test_documents/
│   ├── 📁 test_cases
│   │   ├── Test_Cases_InventoryManagement_v1.0.xlsx
│   │   ├── Test_Cases_ProductIdentification_v1.0.xlsx
│   │   ├── Test_Cases_Settlement_v1.0.xlsx
│   │   └── Test_Cases_System_v1.0.xlsx
│   ├── 📁 test_data
│   │   ├── test_photo1.jpg
│   │   └── test_photo2.jpg
│   ├── 📁 test_plans
│   │   └── Test_Plan.md
│   ├── 📁 test_reports
│   │   └── Test_Report_System_v1.0_20240630.md
│   └── 📁 test_Selenium_UI
│       └── test_ui.py
│
│── 📁 yolov5_master/               # YOLOv5 完整源码
│
├── 1_解析商品名.py                 # 商品信息解析脚本
├── 2_修改格式.py                   # 文件格式转换脚本
├── app.py                          # Flask 后端主程序
├── best.pt                         # YOLOv5 训练好的模型权重       
├── data.yaml                       # 数据集配置和类别信息
├── product_prices_stock.csv        # 商品价格库存数据
└── Register_Login.csv               # 用户账号数据
