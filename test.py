import webbrowser
import pyautogui

#Opens Discord on the browser
chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
url = "https://discord.com/channels/@me/1237525797213044818"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
webbrowser.get('chrome').open_new_tab(url)

pyautogui.moveTo(100,100) #Instantly Moves cursor to user search