import webbrowser as wb
import pyautogui as pag
from screeninfo import get_monitors
import time

#monitor 1 dimensions/resolution
monitorWidth,monitorHeight = get_monitors()[0].width, get_monitors()[0].height
pedo = "neal_j07"

#Opens Discord on the browser
chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
wb.register('chrome', None, wb.BackgroundBrowser(chrome_path))
wb.get('chrome').open_new_tab("https://discord.com/channels/@me")
time.sleep(2)

pag.click(20,170) #Instantly Moves cursor to add a server
#time.sleep(.5)
#pag.click(monitorWidth/2,monitorHeight*3/4)
#time.sleep(.5)
#pag.typewrite("https://discord.gg/gDqMfCPxCs")
#pag.click(monitorWidth*6/10,monitorHeight*7/10)

time.sleep(.5)
pag.moveTo(monitorWidth * 9/10,monitorHeight/10)
time.sleep(.5)
pag.click(monitorWidth * 9/10,monitorHeight/10)