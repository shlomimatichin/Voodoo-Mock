from Tkinter import *
import thread
import time
from pytestsimplecui import PyTestSimpleCui

class Desc:
	def __init__( self , root , text , allWidth ):
		self.allWidth = allWidth;
		self.frame = Frame( root , bd=2 , relief='sunken' , width=allWidth/30 )
		self.frame.pack( side='left' , fill='x' , expand=1 , padx=1 , pady=1 )
		self.label = Label( self.frame , text=text , font='{courier -9}' , width=allWidth/30 )
		self.label.pack()

	def setText( self , text ):
		self.label.configure( text=text , width=self.allWidth/30 )

class Time:
	def __init__( self , root , text ):
		self.frame = Frame( root , bd=2 , relief='sunken' , width=60 )
		self.frame.pack( side='left' , padx=1 , pady=1 )
		self.label = Label( self.frame , text=text , font='{courier -9}')
		self.label.pack()

	def setText( self , text ):
		self.label.configure( text=text )

class PyTestSimpleGui( PyTestSimpleCui ):
	def __init__( self ):
		PyTestSimpleCui.__init__( self )
		self.color = 'green'
		self.root = Tk()
		self.root.title("pytestgui")
		self.width = self.root.winfo_screenwidth() - 300
		self.barFrame = Frame( self.root , bd=2 , relief='sunken' )
		self.barFrame.pack( fill='x' , expand=1 , side='top' , padx=1 , pady=1 )
		self.canvas=Canvas(self.barFrame, width=self.width, height=20)
		self.canvas.pack()
		self.scale=self.canvas.create_rectangle(0, 0, 0, 20,
				fill=self.color, outline=self.color )
		self.descFrame = Frame( self.root )
		self.descFrame.pack( fill='x' , expand=1 , side='bottom' )
		self.test = Desc( self.descFrame , 'test_Normal' , self.width )
		self.testTime = Time( self.descFrame , '0:00' )
		self.testSuite = Desc( self.descFrame , 'Test_Good' , self.width )
		self.testSuiteTime = Time( self.descFrame , '0:00' )
		self.total = Desc( self.descFrame , '100 of 100' , self.width )
		self.testTotalTime = Time( self.descFrame , '0:00' )
		self.count = 0
		self.quit = False
		self.testDescription = ""
		self.suiteDescription = ""
		self.testsCount = 999
		self.updateRequested = False
		thread.start_new_thread( self.root.mainloop , () )
		time.sleep( 0.01 )
		self.centerWindow()

	def centerWindow( self ):
		w = self.root.winfo_width()
		h = self.root.winfo_height()
		ws = self.root.winfo_screenwidth()
		hs = self.root.winfo_screenheight()
		x = (ws/2) - (w/2)
		y = (hs/2)*0.9 - (h/2) 
		self.root.geometry('+%d+%d' % (x, y))

	def askForUpdate( self ):
		if not self.updateRequested:
			self.updateRequested = True
			self.root.after( 0 , self.update )

	def update( self ):
		if self.quit:
			self.root.destroy()
			return
		self.canvas.itemconfigure( self.scale , fill=self.color, outline=self.color )
		width = self.width * self.count / self.testsCount
		self.canvas.coords( self.scale , 0 , 0 , width , 20 )
		self.test.setText( self.testDescription )
		self.total.setText( "%d of %d (%d%%)" % ( self.count , self.testsCount , 100 * self.count / self.testsCount ) )
		self.root.wm_title( self.testDescription )
		self.canvas.update_idletasks()
		self.testSuite.setText( self.suiteDescription )
		self.updateRequested = False

	def leaveWorld( self , description ):
		self.quit = True
		self.askForUpdate()
		time.sleep( 0.2 )
		return PyTestSimpleCui.leaveWorld( self , description )

	def enterWorld( self, description ):
		self.testsCount = self._countTests()
		self.askForUpdate()
		return PyTestSimpleCui.enterWorld( self , description )
    
	def failTest( self, fullPath, lineNum, message ):
		self.color = 'red'
		self.askForUpdate()
		return PyTestSimpleCui.failTest( self , fullPath , lineNum , message )

	def enterTest( self, description ):
		self.count += 1
		self.testDescription = description;
		self.askForUpdate()
		return PyTestSimpleCui.enterTest( self , description )

	def enterSuite( self , description ):
		self.suiteDescription = description
		self.askForUpdate()
		return PyTestSimpleCui.enterSuite( self , description )
        
__all__ = [ "PyTestSimpleGui" ]
