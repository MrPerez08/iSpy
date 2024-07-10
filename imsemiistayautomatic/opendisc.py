from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time

# Replace with your server invite link
server_invite= "https://discord.gg/EdqRe89B"
email = "itybitygremlin@gmail.com"  # Replace with your email
password = "MrYoshiJoshiSells"  # Replace with your password
pedo = ""

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
    #Enter 2captcha hcaptcha bypass
    #WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, 'checkbox'))).click()

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