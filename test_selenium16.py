from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time

# مسیر ChromeDriver (مطمئن شو مسیر درست باشه)
chromedriver_path = "E:/1-python/8-telegram-bot/1-telegram-scraper/chromedriver.exe"

# تنظیمات کروم
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# باز کردن مرورگر
driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
driver.get("https://web.telegram.org/k/")
print("تلگرام وب باز شد! لطفاً لاگین کن.")
time.sleep(30)  # 30 ثانیه برای لاگین دستی

# رفتن به کانال
driver.get("https://web.telegram.org/k/#@ZXgasket")
print("رفتیم به کانال ZXgasket!")
time.sleep(10)  # منتظر لود شدن کانال

# پیدا کردن المنت پست‌ها
bubbles_inner = driver.find_element_by_class_name('bubbles-inner')

# اسکرول به بالای کانال
driver.execute_script("arguments[0].scrollTop = 0;", bubbles_inner)
print("اسکرول کردیم به بالای کانال!")
time.sleep(5)

# حلقه برای اسکرول و گرفتن پست‌ها
last_height = driver.execute_script("return arguments[0].scrollHeight;", bubbles_inner)
while True:
    # گرفتن پست‌ها
    posts = driver.find_elements_by_class_name('bubble.channel-post')
    for post in posts:
        try:
            caption = post.find_element_by_class_name('translatable-message').text
            date = post.find_element_by_class_name('time-inner').text
            print(f"تاریخ: {date} | کپشن: {caption}")
        except:
            print("یه پست بدون کپشن یا تاریخ پیدا شد.")

    # اسکرول به پایین
    driver.execute_script("arguments[0].scrollBy(0, 1000);", bubbles_inner)
    time.sleep(2)  # منتظر لود شدن پست‌های جدید

    # چک کردن پایان اسکرول
    new_height = driver.execute_script("return arguments[0].scrollHeight;", bubbles_inner)
    if new_height == last_height:
        print("به آخر کانال رسیدیم!")
        break
    last_height = new_height

# بستن مرورگر
driver.quit()