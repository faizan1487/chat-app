from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Set the PATH environment variable to include the directory containing chromedriver
os.environ["PATH"] += os.pathsep + '/usr/local/bin/'

# Open the webpage
driver = webdriver.Chrome()

# Open the webpage
driver.get("https://portal.alnafi.com/courses/take/CCST/pdfs/43565913-opc-ua-successstory-smartmetering-regioit-v1")

try:
    # Loop to continuously click on the "Complete and Continue" button until all videos are completed
    while True:
        try:
            # Wait for the "Complete and Continue" button to be clickable
            complete_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "_content__container_142a8m")))
            
            # Click the "Complete and Continue" button
            complete_button.click()
            
            # Wait for the next video to start playing
            time.sleep(5)  # Adjust the sleep time if necessary
            
        except Exception as e:
            print("All videos completed!")
            break  # Break the loop when all videos are completed

finally:
    # Close the browser window
    driver.quit()


# https://portal.alnafi.com/courses/take/CCST/pdfs/43565913-opc-ua-successstory-smartmetering-regioit-v1
# /usr/local/bin/chromedriver
# _content__container_142a8m