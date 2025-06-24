from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

USERNAME = 'selenium.bot.demo1'   # Replace with dummy Instagram username
PASSWORD = 'Selenium@12345'   # Replace with dummy Instagram password
TARGET_USER = 'cbitosc'

# Setup Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# Initialize the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def login():
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)

    user_input = driver.find_element(By.NAME, "username")
    pass_input = driver.find_element(By.NAME, "password")
    user_input.send_keys(USERNAME)
    pass_input.send_keys(PASSWORD)
    pass_input.send_keys(Keys.ENTER)
    time.sleep(7)

def search_and_follow():
    driver.get(f"https://www.instagram.com/{TARGET_USER}/")
    time.sleep(5)

    try:
        follow_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Follow')]")
        follow_btn.click()
        time.sleep(3)
    except:
        print("Already following or button not found.")

def extract_data():
    time.sleep(2)
    bio = driver.find_element(By.XPATH, "//div[contains(@class, '_aacl _aaco _aacw _aacx _aad7 _aade')]").text
    stats = driver.find_elements(By.XPATH, "//ul[@class='_ac2a']/li/span/span")
    
    followers = stats[1].get_attribute("title") if len(stats) > 1 else "N/A"
    posts = stats[0].text if len(stats) > 0 else "N/A"
    following = stats[2].text if len(stats) > 2 else "N/A"

    with open("profile_info.txt", "w", encoding='utf-8') as f:
        f.write(f"Username: {TARGET_USER}\n")
        f.write(f"Bio: {bio}\n")
        f.write(f"Posts: {posts}\n")
        f.write(f"Followers: {followers}\n")
        f.write(f"Following: {following}\n")

    print("Data saved to profile_info.txt")

if __name__ == "__main__":
    login()
    search_and_follow()
    extract_data()
    driver.quit()
