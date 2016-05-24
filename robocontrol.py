import pyautogui, sys, pyHook, pythoncom
import configparser

#detect screen size
screenWidth, screenHeight = pyautogui.size()

#prepare ini parser
parser = configparser.ConfigParser()
parser.read('robocontrol.ini')

# set all global variables
speed = 2
hookOn = False

#dicts and lists
helpDict = {}
helpDict['Movement'] = {}
helpDict['Speed Keys'] = {}
helpDict['Commands'] = {}
keyPairs = {}
speedKeys = {}
speeds = ['Slow','Medium','Fast']
xCoords = {}
yCoords = {}
debouncedKeyList = []
speedKeyList = []
commandKeyList = []

def MakeList(section,list):
	parse = parser[section]
	for keys in parse:
		list.append(parse[keys])

def MakeSpeedDict (section,dict):
	parse = parser[section]
	for keys in parse:
		dict.update({parse[keys]:keys})	

def MakeCoords(section1,section2,section3,dict):
	parse1 = parser[section1]
	parse2 = parser[section2]
	parse3 = parser[section3]
	for keys in parse1:
		dict.update({parse1[keys]:parse2[keys]})
	for keys in parse3:
		dict.update({parse3[keys]:parse2[keys]})
	for items in speeds:
		dict.update({items:parse2[items]})

def MakePairs(list,dict):	
	count = 0
	for items in list:
		dict.update({list[count]:False})
		count = count + 1
	
def MakeHelpDict(dict):
	for keys in parser['operations']:
		dict['Movement'].update({parser['operations'][keys]:keys})
	for keys in parser['speedkeys']:
		dict['Speed Keys'].update({parser['speedkeys'][keys]:keys})
	for keys in parser['commandkeys']:
		dict['Commands'].update({parser['commandkeys'][keys]:keys})
	
MakeList('operations',debouncedKeyList)
MakeList('speedkeys',speedKeyList)
MakeList('commandkeys',commandKeyList)
MakeSpeedDict('speedkeys',speedKeys)		
MakeCoords('operations','xCoords','commandkeys',xCoords)
MakeCoords('operations','yCoords','commandkeys',yCoords)
keyList = debouncedKeyList + speedKeyList + commandKeyList
MakePairs(debouncedKeyList,keyPairs)
MakeHelpDict(helpDict)

#Welcome display
print('Robocontrol Script v1.06')
print('Controls can be modified in robocontrol.ini') 
print()
print('Press Esc to quit')
print('Press Scroll Lock to enable key control')
print('Control is Off')
print()


def OnKeyDownEvent(event):
	global hookOn
	if event.KeyID == 27: #Escape to quit
		sys.exit()
	elif event.KeyID == 145: #Scroll lock to enable/disable key control
		ChangeHook()
	elif hookOn == True: #If control is enabled, Then...
		if event.KeyID == 19: #Display key list
			ButtonList()
		elif event.Key in keyList:
			if event.Key in debouncedKeyList and keyPairs[event.Key] == False:
				pyautogui.mouseDown(x = xCoords[event.Key], y = yCoords[event.Key])
				keyPairs[event.Key] = True
			elif event.Key in commandKeyList:
				pyautogui.click(xCoords[event.Key],yCoords[event.Key])
			elif event.Key in speedKeyList:
				ModifySpeed(event)
			
# return True to pass the event to other handlers, i.e. OS
	if hookOn == True:
		return (event.Key not in keyList)
	else:
		return True
		
def OnKeyUpEvent(event):
#only watching up events for debounced buttons	
	if event.Key in debouncedKeyList:
		pyautogui.mouseUp()
		keyPairs[event.Key] = False
		
# return True to pass the event to other handlers
	return (event.Key not in keyList)

def ChangeHook():
	global hookOn
	if hookOn == False:
		hookOn = True
		print('Control is On')
		print('Press Pause/Break to see available commands')
		print('Press Scroll Lock to disable key control')
		print()
	else:
		hookOn = False
		print('Control is Off')
		print('Press Scroll Lock to enable key control')
		print()
	return()

def ButtonList():
	for x in helpDict:
		print()
		print(x)
		for y in helpDict[x]:
			print(y,helpDict[x][y],sep=" = ")
	return()

def ModifySpeed(event):
	global speed
	if speedKeys[event.Key] == 'increase':
		if speed == 2:
			pyautogui.click(xCoords["Fast"],yCoords["Fast"])
			speed += 1
		elif speed == 1:
			pyautogui.click(xCoords["Medium"],yCoords["Medium"])
			speed += 1
	elif speedKeys[event.Key] == 'decrease':	
		if speed == 3:
			pyautogui.click(xCoords["Medium"],yCoords["Medium"])
			speed -= 1
		elif speed == 2:
			pyautogui.click(xCoords["Slow"],yCoords["Slow"])
			speed -= 1
	return (event)	
		
# create a hook manager
hm = pyHook.HookManager()
# watch for all keyboard events
hm.KeyDown = OnKeyDownEvent
hm.KeyUp = OnKeyUpEvent
# set the hook
hm.HookKeyboard()
# wait forever
pythoncom.PumpMessages()


