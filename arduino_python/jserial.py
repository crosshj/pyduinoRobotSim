#! /usr/bin/env python
"""
uses wxpython 

	get --- http://wxpython.org/download.php  
	    --- http://downloads.sourceforge.net/wxpython/wxPython2.8-win32-unicode-2.8.12.1-py27.exe


"""


import wx
import serial


def scan():
	"""scan for available ports. return a list of tuples (num, name)"""
	global ports
	ports = []
	for i in range(256):
		try:
			s = serial.Serial(i)
			ports.append( (i, s.portstr))
			s.close()   # explicit close 'cause of delayed GC in java
		except serial.SerialException:
			pass


class MyDialog(wx.Dialog):

	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size=(250, 125))
		self.port_list=[]
		for n,s in ports:
			self.port_list.append(s)
		print self.port_list
		self.selected = self.port_list[0]
		wx.Button(self, 1, 'Okay', (80, 60))
		wx.ComboBox(self, -1, pos=(50, 25), size=(150, -1), choices=self.port_list, style=wx.CB_READONLY,value=self.port_list[0])
		
	
		self.Bind(wx.EVT_BUTTON, self.OnClose, id=1)
		self.Bind(wx.EVT_COMBOBOX, self.OnSelect)
	
		self.Centre()
	
	def OnClose(self, event):
		self.Close()
	def OnSelect(self, event):
			self.selected = self.port_list[event.Selection]
	def GetValue(self):
		return self.selected
	
def Select_Port():
	scan()
	if len(ports) == 0:
		return "None"
		print "No ports found"
	elif len(ports) == 1:  
		port_list=[]
		for n,s in ports:
			port_list.append(s)
		return port_list[0]
	else:
		app = wx.PySimpleApp()
		dlg = MyDialog(None, -1, 'Select port to use:')
		retval = dlg.ShowModal()
		selected = dlg.GetValue()
		dlg.Destroy()
		app.MainLoop() 
		return selected


def init(PORT, RATE):

	try:
		ser = serial.Serial(
		                port=PORT,
		                baudrate=RATE,
		                bytesize=serial.EIGHTBITS,
		                parity=serial.PARITY_NONE,
		                stopbits=serial.STOPBITS_ONE,
		                timeout=0,
		                xonxoff=0,
		                rtscts=0,
		                interCharTimeout=None
		            )
		return ser
	except:
		print "Could not init com port"
		return False
	













if __name__=='__main__':
	Select_Port()
	
