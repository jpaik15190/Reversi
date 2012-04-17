import wxversion
import wx, wx.html
import sys

aboutText = """<p>Reversi!</p>""" 

class HtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, id, size=(600,400)):
        wx.html.HtmlWindow.__init__(self,parent, id, size=size)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

    def OnLinkClicked(self, link):
        wx.LaunchDefaultBrowser(link.GetHref())
        
class AboutBox(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "About Reversi",
            style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|
                wx.TAB_TRAVERSAL)
        hwin = HtmlWindow(self, -1, size=(200,200))
        vers = {}
        vers["python"] = sys.version.split()[0]
        vers["wxpy"] = wx.VERSION_STRING
        hwin.SetPage(aboutText % vers)
        btn = hwin.FindWindowById(wx.ID_OK)
        irep = hwin.GetInternalRepresentation()
        hwin.SetSize((irep.GetWidth()+25, irep.GetHeight()+10))
        self.SetClientSize(hwin.GetSize())
        self.CentreOnParent(wx.BOTH)
        self.SetFocus()

class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, pos=(0,0), size=(1000,850))
        self.Bind(wx.EVT_CLOSE, self.OnClose)
  
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        
        m_exit = menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")
        self.Bind(wx.EVT_MENU, self.OnClose, m_exit)
        
        menuBar.Append(menu, "&File")
        menu = wx.Menu()
        m_about = menu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, m_about)
        
        menuBar.Append(menu, "&Help")
        self.SetMenuBar(menuBar)
        
        self.statusbar = self.CreateStatusBar()

        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        
        #m_text = wx.StaticText(panel, -1, "Hello World!")
        #m_text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        #m_text.SetSize(m_text.GetBestSize())
        #box.Add(m_text, 0, wx.ALL, 10)
        
        #m_close = wx.Button(panel, wx.ID_CLOSE, "Close")
        #m_close.Bind(wx.EVT_BUTTON, self.OnClose)
        #box.Add(m_close, 0, wx.ALL, 10)
        
        self.button1 =wx.Button(self, label="Button 1", pos=(0, 0), size=(100,100))   
        self.button2 =wx.Button(self, label="Button 2", pos=(100, 0), size=(100,100))
        self.button3 =wx.Button(self, label="Button 3", pos=(200, 0), size=(100,100))      
        self.button4 =wx.Button(self, label="Button 4", pos=(300, 0), size=(100,100))
        self.button5 =wx.Button(self, label="Button 5", pos=(400, 0), size=(100,100))      
        self.button6 =wx.Button(self, label="Button 6", pos=(500, 0), size=(100,100))
        self.button7 =wx.Button(self, label="Button 7", pos=(600, 0), size=(100,100))    
        self.button8 =wx.Button(self, label="Button 8", pos=(700, 0), size=(100,100))
        
        self.button9 =wx.Button(self, label="Button 9", pos=(0, 100), size=(100,100))    
        self.button10 =wx.Button(self, label="Button 10", pos=(100, 100), size=(100,100))
        self.button11 =wx.Button(self, label="Button 11", pos=(200, 100), size=(100,100))      
        self.button12 =wx.Button(self, label="Button 12", pos=(300, 100), size=(100,100))
        self.button13 =wx.Button(self, label="Button 13", pos=(400, 100), size=(100,100))     
        self.button14 =wx.Button(self, label="Button 14", pos=(500, 100), size=(100,100))
        self.button15 =wx.Button(self, label="Button 15", pos=(600, 100), size=(100,100))       
        self.button16 =wx.Button(self, label="Button 16", pos=(700, 100), size=(100,100))
        
        self.button17 =wx.Button(self, label="Button 17", pos=(0, 200), size=(100,100))       
        self.button18 =wx.Button(self, label="Button 18", pos=(100, 200), size=(100,100))
        self.button19 =wx.Button(self, label="Button 19", pos=(200, 200), size=(100,100))     
        self.button20 =wx.Button(self, label="Button 20", pos=(300, 200), size=(100,100))
        self.button21 =wx.Button(self, label="Button 21", pos=(400, 200), size=(100,100))    
        self.button22 =wx.Button(self, label="Button 22", pos=(500, 200), size=(100,100))
        self.button23 =wx.Button(self, label="Button 23", pos=(600, 200), size=(100,100))     
        self.button24 =wx.Button(self, label="Button 24", pos=(700, 200), size=(100,100))
        
        self.button25 =wx.Button(self, label="Button 25", pos=(0, 300), size=(100,100))    
        self.button26 =wx.Button(self, label="Button 26", pos=(100, 300), size=(100,100))
        self.button27 =wx.Button(self, label="Button 27", pos=(200, 300), size=(100,100))       
        self.button28 =wx.Button(self, label="Button 28", pos=(300, 300), size=(100,100))
        self.button29 =wx.Button(self, label="Button 29", pos=(400, 300), size=(100,100))      
        self.button30 =wx.Button(self, label="Button 30", pos=(500, 300), size=(100,100))
        self.button31 =wx.Button(self, label="Button 31", pos=(600, 300), size=(100,100))       
        self.button32 =wx.Button(self, label="Button 32", pos=(700, 300), size=(100,100))
        
        self.button33 =wx.Button(self, label="Button 33", pos=(0, 400), size=(100,100))     
        self.button34 =wx.Button(self, label="Button 34", pos=(100, 400), size=(100,100))
        self.button35 =wx.Button(self, label="Button 35", pos=(200, 400), size=(100,100))  
        self.button36 =wx.Button(self, label="Button 36", pos=(300, 400), size=(100,100))
        self.button37 =wx.Button(self, label="Button 37", pos=(400, 400), size=(100,100))      
        self.button38 =wx.Button(self, label="Button 38", pos=(500, 400), size=(100,100))
        self.button39 =wx.Button(self, label="Button 39", pos=(600, 400), size=(100,100))     
        self.button40 =wx.Button(self, label="Button 40", pos=(700, 400), size=(100,100))
        
        self.button41 =wx.Button(self, label="Button 41", pos=(0, 500), size=(100,100))   
        self.button42 =wx.Button(self, label="Button 42", pos=(100, 500), size=(100,100))
        self.button43 =wx.Button(self, label="Button 43", pos=(200, 500), size=(100,100))      
        self.button44 =wx.Button(self, label="Button 44", pos=(300, 500), size=(100,100))
        self.button45 =wx.Button(self, label="Button 45", pos=(400, 500), size=(100,100))     
        self.button46 =wx.Button(self, label="Button 46", pos=(500, 500), size=(100,100))
        self.button47 =wx.Button(self, label="Button 47", pos=(600, 500), size=(100,100))      
        self.button48 =wx.Button(self, label="Button 48", pos=(700, 500), size=(100,100))
        
        self.button49 =wx.Button(self, label="Button 49", pos=(0, 600), size=(100,100))      
        self.button50 =wx.Button(self, label="Button 50", pos=(100, 600), size=(100,100))
        self.button51 =wx.Button(self, label="Button 51", pos=(200, 600), size=(100,100))      
        self.button52 =wx.Button(self, label="Button 52", pos=(300, 600), size=(100,100))
        self.button53 =wx.Button(self, label="Button 53", pos=(400, 600), size=(100,100))      
        self.button54 =wx.Button(self, label="Button 54", pos=(500, 600), size=(100,100))
        self.button55 =wx.Button(self, label="Button 55", pos=(600, 600), size=(100,100))     
        self.button56 =wx.Button(self, label="Button 56", pos=(700, 600), size=(100,100))
        
        self.button57 =wx.Button(self, label="Button 57", pos=(0, 700), size=(100,100))    
        self.button58 =wx.Button(self, label="Button 58", pos=(100, 700), size=(100,100))
        self.button59 =wx.Button(self, label="Button 59", pos=(200, 700), size=(100,100))    
        self.button60 =wx.Button(self, label="Button 60", pos=(300, 700), size=(100,100))
        self.button61 =wx.Button(self, label="Button 61", pos=(400, 700), size=(100,100))      
        self.button62 =wx.Button(self, label="Button 62", pos=(500, 700), size=(100,100))
        self.button63 =wx.Button(self, label="Button 63", pos=(600, 700), size=(100,100))   
        self.button64 =wx.Button(self, label="Button 64", pos=(700, 700), size=(100,100))
        
        
        self.button1.SetBackgroundColour("Green")
        self.button2.SetBackgroundColour("Green")
        self.button3.SetBackgroundColour("Green")    
        self.button4.SetBackgroundColour("Green")
        self.button5.SetBackgroundColour("Green")
        self.button6.SetBackgroundColour("Green")
        self.button7.SetBackgroundColour("Green")  
        self.button8.SetBackgroundColour("Green")
        
        self.button9.SetBackgroundColour("Green")  
        self.button10.SetBackgroundColour("Green")
        self.button11.SetBackgroundColour("Green")    
        self.button12.SetBackgroundColour("Green")
        self.button13.SetBackgroundColour("Green")     
        self.button14.SetBackgroundColour("Green")
        self.button15.SetBackgroundColour("Green")      
        self.button16.SetBackgroundColour("Green")
        
        self.button17.SetBackgroundColour("Green")     
        self.button18.SetBackgroundColour("Green")
        self.button19.SetBackgroundColour("Green")     
        self.button20.SetBackgroundColour("Green")
        self.button21.SetBackgroundColour("Green")  
        self.button22.SetBackgroundColour("Green")
        self.button23.SetBackgroundColour("Green")  
        self.button24.SetBackgroundColour("Green")
        
        self.button25.SetBackgroundColour("Green") 
        self.button26.SetBackgroundColour("Green")
        self.button27.SetBackgroundColour("Green")      
        self.button28.SetBackgroundColour("Green")
        self.button29.SetBackgroundColour("Green")  
        self.button30.SetBackgroundColour("Green")
        self.button31.SetBackgroundColour("Green") 
        self.button32.SetBackgroundColour("Green")
        
        self.button33.SetBackgroundColour("Green")   
        self.button34.SetBackgroundColour("Green")
        self.button35.SetBackgroundColour("Green") 
        self.button36.SetBackgroundColour("Green")
        self.button37.SetBackgroundColour("Green")     
        self.button38.SetBackgroundColour("Green")
        self.button39.SetBackgroundColour("Green")    
        self.button40.SetBackgroundColour("Green")
        
        self.button41.SetBackgroundColour("Green") 
        self.button42.SetBackgroundColour("Green")
        self.button43.SetBackgroundColour("Green")   
        self.button44.SetBackgroundColour("Green")
        self.button45.SetBackgroundColour("Green")    
        self.button46.SetBackgroundColour("Green")
        self.button47.SetBackgroundColour("Green")   
        self.button48.SetBackgroundColour("Green")
        
        self.button49.SetBackgroundColour("Green")  
        self.button50.SetBackgroundColour("Green")
        self.button51.SetBackgroundColour("Green")      
        self.button52.SetBackgroundColour("Green")
        self.button53.SetBackgroundColour("Green")     
        self.button54.SetBackgroundColour("Green")
        self.button55.SetBackgroundColour("Green")   
        self.button56.SetBackgroundColour("Green")
        
        self.button57.SetBackgroundColour("Green")  
        self.button58.SetBackgroundColour("Green")
        self.button59.SetBackgroundColour("Green") 
        self.button60.SetBackgroundColour("Green")
        self.button61.SetBackgroundColour("Green")   
        self.button62.SetBackgroundColour("Green")
        self.button63.SetBackgroundColour("Green") 
        self.button64.SetBackgroundColour("Green")
        
        self.Bind(wx.EVT_BUTTON, self.OnToggleItem, self.button1)
        
        panel.SetSizer(box)
        panel.Layout()

    def OnClose(self, event):
        dlg = wx.MessageDialog(self, 
            "Do you really want to stop playing Reversi?",
            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()

    def OnAbout(self, event):
        dlg = AboutBox()
        dlg.ShowModal()
        dlg.Destroy()  
        
    def OnToggleItem(self, event):
        # tricky logic to toggle colour
        colour =  (self.enabled and "Black" or "White")
        self.btn.SetLabel(colour)
        self.enabled = not self.enabled
        self.btn.SetBackgroundColour(colour)
        self.btn.ClearBackground()
        
   

app = wx.App(redirect=True)   # Error messages go to popup window
top = Frame("Reversi!")
top.Show()
app.MainLoop()