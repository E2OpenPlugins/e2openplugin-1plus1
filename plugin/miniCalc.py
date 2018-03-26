# -*- coding: UTF-8 -*-

# Change the / operator to mean true division.
# (The default in python 2.x is floor division)
from __future__ import division

# for localized messages
from . import _

def compute(expression):
	"""
	Evaluate expression and return result as a string
	Valid characters:    0-9. +-*/^ ()
	Sample expression:   0.2/7 + 0.5 * 3.14159^(-2)
	"""
	
	# sanitize input
	allowed_chars=" 0123456789.+-*/^()"
	i=0
	while i < len(expression):
	    if (not(expression[i] in allowed_chars)):
	        expression=""   # illegal char found, discard input
	        break
	    i += 1

	try:
		# ^ means raise to a power (ie. **)
		r = str(eval(expression.replace('^', '**')))
	except:
		r = ''
	return(r)


###########################################################################
from Screens.Screen import Screen
from Components.Label import Label
from Components.ActionMap import ActionMap
from Components.Input import Input
from Screens.InputBox import InputBox
from Screens.MessageBox import MessageBox
from Plugins.Plugin import PluginDescriptor

class miniCalcScreen(Screen):
	def __init__(self, session, args = 0):
		self.session = session
		Screen.__init__(self, session)

		self["myActionMap"] = ActionMap(["SetupActions"],
		{
			#"ok": self.myInput,
			"cancel": self.cancel
		}, -1)
		self.onShown.append(self.myInput)

	def myInput(self):
		self.session.open(VirtualKeyBoard,
			title=_("[ 1+1 ]      Enter an arithmetic expression"),
			text=" " * 100)
		self.close(None)

	def cancel(self):
		#print "[1+1] cancel"
		self.close(None)


###############################################################
# This part is based on Screens/VirtualKeyBoard.py
from Components.Language import language
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from enigma import eListboxPythonMultiContent, gFont, RT_HALIGN_CENTER, RT_VALIGN_CENTER
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN
from Tools.LoadPixmap import LoadPixmap

class VirtualKeyBoardList(MenuList):
	def __init__(self, list, enableWrapAround=False):
		MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
		self.l.setFont(0, gFont("Regular", 28))
		self.l.setItemHeight(45)

def VirtualKeyBoardEntryComponent(keys, selectedKey):
	key_backspace = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/vkey_backspace.png"))
	key_bg = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/vkey_bg.png"))
	key_clr = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/vkey_clr.png"))
	key_esc = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/vkey_esc.png"))
	key_ok = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/vkey_ok.png"))
	key_sel = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/vkey_sel.png"))
	key_space = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/vkey_space.png"))
	res = [ (keys) ]
	
	#x = 0
	x = 180
	count = 0
	for key in keys:
		width = None
		if key == "EXIT":
			width = key_esc.size().width()
			res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_esc))
		elif key == "BACKSPACE":
			width = key_backspace.size().width()
			res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_backspace))
		elif key == "CLEAR":
			width = key_clr.size().width()
			res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_clr))
		elif key == "SPACE":
			width = key_space.size().width()
			res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_space))
		elif key == "OK":
			width = key_ok.size().width()
			res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_ok))
		#elif key == "<-":
		#	res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(45, 45), png=key_left))
		#elif key == "->":
		#	res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(45, 45), png=key_right))
		
		else:
			width = key_bg.size().width()
			res.extend((
				MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_bg),
				MultiContentEntryText(pos=(x, 0), size=(width, 45), font=0, text=key.encode("utf-8"), flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER)
			))
		
		if selectedKey == count:
			width = key_sel.size().width()
			res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_sel))

		if width is not None:
			x += width
		else:
			x += 45
		count += 1
	

	#res.append(MultiContentEntryText(pos=( 80, 40), size=(100, 45), font=0, text=(_("Bald figures")).encode("utf-8"), flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER))
	return res


class VirtualKeyBoard(Screen):
	def locate_key(self, key):
		r=0
		for l in self.keys_list:
			for k in l:
				if (k == key): 
					return(r)
				r += 1

	def __init__(self, session, title="", text=""):
		Screen.__init__(self, session)
		self.keys_list = []
		self.lang = language.getLanguage()
		self.keys_list = [
			[u"BACKSPACE", u"(", u")",u"CLEAR"],
			[u"1", u"2", u"3", u"/"],
			[u"4", u"5", u"6", u"*"],
			[u"7", u"8", u"9", u"-"],
			[u"^",u"0", u".", u"+"]]
			
		
		self.text = text.decode("utf-8")
		
		self["header"] = Label(title)
		self["text"] = Label(text)
		self["list"] = VirtualKeyBoardList([])

		self.rows = len(self.keys_list);
		self.keysPerRow = len(self.keys_list[0]);
		self.max_key = (self.keysPerRow * self.rows) - 1	 # 0-based counting

		self["actions"] = ActionMap(["OkCancelActions", "WizardActions", "ColorActions","NumberActions"],
			{
				"0": self.key0,
				"1": self.key1,
				"2": self.key2,
				"3": self.key3,
				"4": self.key4,
				"5": self.key5,
				"6": self.key6,
				"7": self.key7,
				"8": self.key8,
				"9": self.key9,
				"ok": self.okClicked,
				"cancel": self.exit,
				"left": self.left,
				"right": self.right,
				"up": self.up,
				"down": self.down,
				"red": self.backClicked,
				"green": self.ok
			}, -2)
		

		self.onLayoutFinish.append(self.buildVirtualKeyBoard)

	

	def buildVirtualKeyBoard(self, selectedKey=0, keysPerRow=0):
		list = []
		
		self.k_list = self.keys_list
		for keys in self.k_list:
			if selectedKey < keysPerRow and selectedKey > -1:
				list.append(VirtualKeyBoardEntryComponent(keys, selectedKey))
			else:
				list.append(VirtualKeyBoardEntryComponent(keys, -1))
			selectedKey -= keysPerRow
		
		self["list"].setList(list)


	def key0to9(self,key):
		self.text += key
		self["text"].setText(self.text.encode("utf-8"))
		self["header"].setText(compute(self.text))
		self.selectedKey = self.locate_key(key)
		self.showActiveKey()


	def key0(self):
		self.key0to9(u"0")
	def key1(self):
		self.key0to9(u"1")
	def key2(self):
		self.key0to9(u"2")
	def key3(self):
		self.key0to9(u"3")
	def key4(self):
		self.key0to9(u"4")
	def key5(self):
		self.key0to9(u"5")
	def key6(self):
		self.key0to9(u"6")
	def key7(self):
		self.key0to9(u"7")
	def key8(self):
		self.key0to9(u"8")
	def key9(self):
		self.key0to9(u"9")


	def backClicked(self):
		self.text = self.text[:-1]
		self["text"].setText(self.text.encode("utf-8"))
		self["header"].setText(compute(self.text))
			
	def okClicked(self):
		list = self.keys_list
		
		selectedKey = self.selectedKey

		text = None

		for x in list:
			if selectedKey < self.keysPerRow:
				if selectedKey < len(x):
					text = x[selectedKey]
				break
			else:
				selectedKey -= self.keysPerRow

		if text is None:
			return

		if text == "EXIT":
			self.close(None)
		
		elif text == "BACKSPACE":
			self.text = self.text[:-1]
			self["text"].setText(self.text.encode("utf-8"))
			self["header"].setText(compute(self.text))
		
		elif text == "CLEAR":
			self.text = ""
			self["text"].setText(self.text.encode("utf-8"))
			self["header"].setText(compute(self.text))
		
		elif text == "SPACE":
			self.text += " "
			self["text"].setText(self.text.encode("utf-8"))
		
		elif text == "OK":
			self.close(self.text.encode("utf-8"))
		
		else:
			self.text += text
			self["text"].setText(self.text.encode("utf-8"))
			self["header"].setText(compute(self.text))

	def ok(self):
		self.close(self.text.encode("utf-8"))

	def exit(self):
		self.close(None)

	def left(self):
		self.selectedKey -= 1
		
		s = True
		for i in range(1, self.rows):
			if (s and (self.selectedKey == ((i-1) * self.keysPerRow)-1 )):
				s = False
				self.selectedKey += self.keysPerRow
		
		self.showActiveKey()

	def right(self):
		self.selectedKey += 1
		
		s = True
		for i in range(1, self.rows):
			if (s and (self.selectedKey == i * self.keysPerRow)):
				s = False
				self.selectedKey = (i-1) * self.keysPerRow
		
		self.showActiveKey()

	def up(self):
		self.selectedKey -= self.keysPerRow
		
		if (self.selectedKey < 0):
			self.selectedKey += (self.keysPerRow * self.rows)
		self.showActiveKey()

	def down(self):
		self.selectedKey += self.keysPerRow
		
		if (self.selectedKey > self.max_key):
			self.selectedKey -= (self.keysPerRow * self.rows)
		self.showActiveKey()

	def showActiveKey(self):
		self.buildVirtualKeyBoard(self.selectedKey, self.keysPerRow)


