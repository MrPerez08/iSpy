import webbrowser as wb
import pyautogui as pag
from screeninfo import get_monitors
import time
import platform

chrome_path =""
match platform.system():
    case 'Windows': chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    case 'Darwin': chrome_path = "~/Library/Application Support/Google/Chrome"

#monitor 1 dimensions/resolution
monitorWidth,monitorHeight = get_monitors()[0].width, get_monitors()[0].height
pedo = "neal_j07"  #<-- INSERT pedo discord usertag

#Opens Discord on the browser
chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
wb.register('chrome', None, wb.BackgroundBrowser(chrome_path))
wb.get('chrome').open_new_tab("https://discord.com/channels/@me")
time.sleep(2)

#THE FOLLOWING IS IF ACC HASNT JOINED SERVER YET
pag.click(20,170) #Instantly Moves cursor to add a server
#time.sleep(.5)
#pag.click(monitorWidth/2,monitorHeight*3/4)
#time.sleep(.5)
#pag.typewrite("https://discord.gg/gDqMfCPxCs")
#pag.click(monitorWidth*6/10,monitorHeight*7/10)

#IF IT AINT BROKE DONT FIX IT
 
time.sleep(.5)
pag.moveTo(monitorWidth * 9/10,monitorHeight/10)
time.sleep(.5)
pag.click(monitorWidth /2,monitorHeight/10)
pag.leftClick(monitorWidth * 9/10,monitorHeight/10)
pag.click(monitorWidth * 9/10,monitorHeight/6)
pag.typewrite(pedo)
pag.press("enter")
pag.click(monitorWidth * 9/10,monitorHeight/6)
pag.leftClick(monitorWidth * 9/10,monitorHeight/4)


pag.moveTo(monitorWidth/5.5,monitorHeight/2)
pag.scroll(15)
#while(True):
    #time.sleep(.5)
    #pag.scroll(32)







