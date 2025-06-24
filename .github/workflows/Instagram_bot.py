from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

USERNAME = 'selenium.bot.demo1'     # Replace with your dummy username
PASSWORD = 'Selenium@12345'         # Replace with your dummy password
TARGET_USER = 'cbitosc'             # The Instagram profile to search

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def login():
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)

    driver.find_element(By.NAME, "username").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD + Keys.ENTER)
    time.sleep(7)

    try:
        # Dismiss "Save Info" popup
        not_now = driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
        not_now.click()
        time.sleep(3)
    except:
        print("No 'Save Info' popup.")

def search_and_follow():
    driver.get(f"https://www.instagram.com/{TARGET_USER}/")
    time.sleep(5)

    try:
        follow_btn = driver.find_element(By.XPATH, "//button[text()='Follow']")
        follow_btn.click()
        print("✅ Followed the user.")
        time.sleep(3)
    except:
        print("🔁 Already following or button not found.")

def extract_data():
    time.sleep(2)

    try:
        bio_element = driver.find_element(By.XPATH, "//div[contains(@class,'-vDIg')]")
        bio = bio_element.text.strip()
    except:
        bio = "No bio found."

    try:
        stats = driver.find_elements(By.XPATH, "//ul[contains(@class,'x78zum5')]/li")
        posts = stats[0].text.split("\n")[0] if len(stats) > 0 else "N/A"
        followers = stats[1].text.split("\n")[0] if len(stats) > 1 else "N/A"
        following = stats[2].text.split("\n")[0] if len(stats) > 2 else "N/A"
    except:
        posts = followers = following = "N/A"

    with open("profile_info.txt", "w", encoding="utf-8") as file:
        file.write(f"Username: {TARGET_USER}\n")
        file.write(f"Bio: {bio}\n")
        file.write(f"Posts: {posts}\n")
        file.write(f"Followers: {followers}\n")
        file.write(f"Following: {following}\n")

    print("✅ profile_info.txt generated successfully.")

if __name__ == "__main__":
    login()
    search_and_follow()
    extract_data()
    driver.quit()
