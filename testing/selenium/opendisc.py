from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from twocaptcha import TwoCaptcha


# Replace with your server invite link
server_invite= "https://discord.gg/awGmqSr5"
pedo = "mrmadmonkey"

#bot account information
email = "itybitygremlin@gmail.com"  
password = "MrYoshiJoshiSells"  

# Set up options for Chrome
options = Options()
options.add_argument("--start-maximized")  # Start maximized
options.add_argument("--disable-infobars")  # Disable infobars
options.add_argument("--disable-extensions")  # Disable extensions
options.add_argument("--disable-infobars")



# Initialize WebDriver using ChromeDriverManager to handle the path
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.get("https://discord.com/login")  # Open Discord login page


# Sign In
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)  # Enter the password
    driver.find_element(By.XPATH, '//button[contains(., "Log In")]').click()  # Click the login button
    WebDriverWait(driver, 30).until(EC.url_contains("channels"))  # Wait for a successful login
except Exception as e:
    print(f"An error occurred while logging in: {e}")
    driver.quit()
    exit()

# Join Discord Server
try:
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME,'circleIcon_db6521'))).click()
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(., "Join a Server")]'))).click()
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'inputInner_e8a9c7'))).send_keys(server_invite)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(., "Join Server")]'))).click()

    #a9b5fb07-92ff-493f-86fe-352a2803b3df

    WebDriverWait(driver,10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#app-mount > div.appAsidePanelWrapper_bd26cc > div.notAppAsidePanel_bd26cc > div:nth-child(5) > div.layer_c9e2da > div > div > div > div.content_d10a58 > div.captchaContainer_d10a58 > div > iframe')
    ))

    api_key = os.getenv('APIKEY_2CAPTCHA', 'afc6affd6485ce9fe825ca3613a7835a')
    solver = TwoCaptcha(api_key)
    try:
        result = solver.hcaptcha(
            sitekey='a9b5fb07-92ff-493f-86fe-352a2803b3df',
            url=driver.current_url,
        )
    except Exception as e:
        print(f"Error occurred: {e}")
    else:
        print('HUURAAH', result)


    #//*[@id="app-mount"]/div[2]/div[1]/div[5]/div[2]/div/div/div/div[1]/div[4]/div/iframe
    ##app-mount > div.appAsidePanelWrapper_bd26cc > div.notAppAsidePanel_bd26cc > div:nth-child(5) > div.layer_c9e2da > div > div > div > div.content_d10a58 > div.captchaContainer_d10a58 > div > iframe

    #Enter 2captcha hcaptcha bypass
    #WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, 'checkbox'))).click()

    #WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'wrapper_f90abb'))).click()
    #WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'input_f4e139'))).send_keys()
    #time.sleep(1)
    #WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, 'uid_16'))).send_keys(pedo)
    


     
    print("Successfully navigated to the server!")
except Exception as e:
    print(f"An error occurred while joining the server: {e}")

#Code a way to message within the server and say something like the following:
#"hi "


try:
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(., pedo)]'))).click()
    print("Successfully joined chat")
except Exception as e:
    print(f"An error occured when contacting accused: {e}")


time.sleep(10)
driver.quit()