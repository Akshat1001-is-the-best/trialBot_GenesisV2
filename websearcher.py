from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
from tts import tts
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Add random delays between actions
def human_delay(min_sec=1, max_sec=3):
    time.sleep(random.uniform(min_sec, max_sec))

def google_Search(text):
    chrome_options = Options()
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(options=chrome_options)


    driver.get("https://search.aol.com/")
    #human_delay()


    search_box = driver.find_element(By.NAME, "q")
    #human_delay(0.5, 1.5)
    # Type like a human (with delays between keystrokes)
    search_term = text
    for char in search_term:
        search_box.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))

    tts("here is what I found")
    
    #human_delay()
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)

    print('search over')
"""
# Move mouse randomly to simulate human behavior
actions = ActionChains(driver)
actions.move_to_element(search_box).perform()
human_delay()

# Scroll the page randomly
driver.execute_script("window.scrollBy(0, %d)" % random.randint(50, 200))
human_delay()
"""