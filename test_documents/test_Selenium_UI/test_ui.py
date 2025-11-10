from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

driver = webdriver.Chrome() # 初始化Chrome浏览器驱动
driver.implicitly_wait(5)  # 隐式等待，增强健壮性，设置隐式等待时间为5秒

try:
    # 测试登录
    driver.get("http://localhost:5000/Register&Login.html")
    driver.find_element(By.ID, "username").send_keys("test_user")
    driver.find_element(By.ID, "password").send_keys("test123")
    driver.find_element(By.XPATH, "//button[text()='登录']").click()
    
    # 验证登录是否成功
    assert "Price_management.html" in driver.current_url, "登录失败"
    print("登录测试通过")

    # 测试结算功能
    driver.get("http://localhost:5000/Settlement.html")
    upload = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    upload.send_keys("test_product.jpg")  # 测试专用图片
    driver.find_element(By.XPATH, "//button[text()='确定']").click()
    
    # 验证商品是否添加到购物车
    shopping_list = driver.find_element(By.ID, "shopping-list")
    assert "可口可乐" in shopping_list.text, "商品识别失败"
    print("商品结算测试通过")

except NoSuchElementException as e:
    print(f"元素未找到: {e}")
except AssertionError as e:
    print(f"测试失败: {e}")
finally:
    driver.quit()