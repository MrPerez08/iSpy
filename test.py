import webbrowser as wb
import pyautogui as pag
import time

#Opens Discord on the browser
chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
url = "https://discord.com/channels/@me/1237525797213044818"
url2 = "https://discord.com/channels/1256622278733729902/1256622278733729905"
wb.register('chrome', None, wb.BackgroundBrowser(chrome_path))
wb.get('chrome').open_new_tab(url2)
time.sleep(2)
pag.locateOnScreen("")

#pag.click(1700,110) #Instantly Moves cursor to user search
#pag.typewrite("Neal")
#pag.press('enter') 