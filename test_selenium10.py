from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# مسیر ChromeDriver
chromedriver_path = "E:/1-python/8-telegram-bot/1-telegram-scraper/chromedriver.exe"

# تنظیمات کروم
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/133.0.0.0 Safari/537.36")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# تنظیم Service
service = Service(executable_path=chromedriver_path)

# باز کردن مرورگر
driver = webdriver.Chrome(service=service, options=chrome_options)
print("کروم باز شد!")

# رفتن به تلگرام وب و لاگین
driver.get("https://web.telegram.org/k/")
print("تلگرام وب باز شد! لطفاً لاگین کن.")
time.sleep(30)  # 30 ثانیه برای لاگین دستی

# رفتن به کانال
driver.get("https://web.telegram.org/k/#@ZXgasket")
print("رفتیم به کانال @ZXgasket!")
time.sleep(10)  # صبر برای لود کامل

# پیدا کردن بخش اسکرول
bubbles_inner = driver.find_element(By.CSS_SELECTOR, ".bubbles-inner")

# تست اسکرول به بالا با جاوااسکریپت
print("تست اسکرول به بالا با جاوااسکریپت...")
for _ in range(5):  # 5 بار تلاش می‌کنه
    driver.execute_script("arguments[0].scrollTop = 0;", bubbles_inner)
    current_scroll = driver.execute_script("return arguments[0].scrollTop;", bubbles_inner)
    print(f"مقدار scrollTop بعد از اسکرول: {current_scroll}")
    time.sleep(1)
    if current_scroll == 0:
        print("اسکرول به بالا با جاوااسکریپت موفق بود!")
        break
else:
    print("اسکرول به بالا با جاوااسکریپت کار نکرد!")

# تست اسکرول به بالا با شبیه‌سازی کلید
print("تست اسکرول به بالا با کلید Page Up...")
for _ in range(10):  # 10 بار Page Up می‌زنه
    bubbles_inner.send_keys(Keys.PAGE_UP)
    current_scroll = driver.execute_script("return arguments[0].scrollTop;", bubbles_inner)
    print(f"مقدار scrollTop بعد از Page Up: {current_scroll}")
    time.sleep(0.5)
    if current_scroll == 0:
        print("اسکرول به بالا با کلید موفق بود!")
        break
else:
    print("اسکرول به بالا با کلید هم کار نکرد!")

# چک کردن تعداد پست‌ها بعد از اسکرول
posts = driver.find_elements(By.CSS_SELECTOR, ".bubble.channel-post")
print(f"تعداد پست‌های لود شده: {len(posts)}")

# نگه داشتن مرورگر برای مشاهده
print("مرورگر باز می‌مونه، خودت چک کن!")
time.sleep(60)
driver.quit()