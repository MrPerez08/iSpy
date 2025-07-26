import os
from twocaptcha import TwoCaptcha
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def solvehCaptcha():
    api_key = os.getenv('APIKEY_2CAPTCHA', 'afc6affd6485ce9fe825ca3613a7835a')

    solver = TwoCaptcha(api_key)

    try:
        result = solver.hcaptcha(
            sitekey='41b778e7-8f20-45cc-a804-1f1ebb45c579',
            url='https://2captcha.com/demo/hcaptcha',
        )

    except Exception as e:
        print(e)
        return False

    else:
        return result

browser = webdriver.Chrome()
browser.get('https://2captcha.com/demo/hcaptcha')

WebDriverWait(browser,10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR,'#root > div._layout_zgi06_1._basicLayout_18ddp_2 > main > div > div > div._content_18ddp_17 > section > div > form > div._captchaWidgetContainer_1f3oo_22 > div > div > iframe')
))

result = solvehCaptcha()
print(result)