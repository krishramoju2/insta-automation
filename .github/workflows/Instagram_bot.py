from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# 🔐 Dummy credentials
USERNAME = "selenium.bot.demo1"
PASSWORD = "Selenium@12345"
TARGET_USER = "cbitosc"

# ✅ Headless Chrome config for Codespaces
options = Options()
options.binary_location = "/usr/bin/chromium-browser"
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def login():
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)
    driver.find_element(By.NAME, "username").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD + Keys.ENTER)
    time.sleep(7)

def follow_and_scrape():
    driver.get(f"https://www.instagram.com/{TARGET_USER}/")
    time.sleep(5)

    try:
        follow = driver.find_element(By.XPATH, "//button[text()='Follow']")
        follow.click()
    except:
        print("Already following or button not found.")

    try:
        bio = driver.find_element(By.XPATH, "//div[contains(@class,'-vDIg')]").text
    except:
        bio = "No bio found."

    stats = driver.find_elements(By.XPATH, "//ul[contains(@class,'x78zum5')]/li")
    posts = stats[0].text.split("\n")[0] if len(stats) > 0 else "N/A"
    followers = stats[1].text.split("\n")[0] if len(stats) > 1 else "N/A"
    following = stats[2].text.split("\n")[0] if len(stats) > 2 else "N/A"

    with open("profile_info.txt", "w") as f:
        f.write(f"Bio: {bio}\n")
        f.write(f"Posts: {posts}\nFollowers: {followers}\nFollowing: {following}\n")

    print("✅ profile_info.txt saved!")

def main():
    try:
        login()
        follow_and_scrape()
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
