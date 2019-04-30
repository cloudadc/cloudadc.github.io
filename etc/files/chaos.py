#!/usr/bin/env python3
"""
Hello World, but with more meat.
"""

import sys
import wx
import threading
import time
import psutil

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from pymongo.errors import PyMongoError

class HelloFrame(wx.Frame):
    """
    A Frame that says Hello World
    """

    ppid = 0
    button = None
    doWrite = True
    writeSpeed = 1
    slidertxt = None
    wc = 1
    closing = False    

    def __init__(self, *args, **kw):
        
        # Parse our kwargs
        self.parseKWArgs(kw)
        
        # ensure the parent's __init__ is called
        super(HelloFrame, self).__init__(*args, **kw, size=(600,400))
        
        # create a panel in the frame
        pnl = wx.Panel(self)

        self.errlbl = wx.StaticText(pnl, pos=(270,196))
        self.stpid = wx.StaticText(pnl, pos=(10,45))
        self.st = wx.StaticText(pnl, label="Checking Primary...", pos=(10,15))
        font = self.st.GetFont()
        font.PointSize += 3
        self.st.SetFont(font)

        # Connect and start writing data
        try:
            self.client = MongoClient(self.conn_str)
            self.db = self.client.tfw
            self.db.numbers.drop()
            threading.Thread(target=self.writeData).start()
        except PyMongoError as ex:
            wx.MessageBox('Failed to connect %s' % ex)
            self.Close(True)
            return

        # Get server nodes
        nodes = list(self.client.nodes)
        nodes = sorted(nodes, key=lambda node: node[0] + str(node[1]))

        # Can only kill a server if it's all localhost
        self.local_ports = []
        kill_enabled = True
        for node in nodes:
            self.local_ports.append(str(node[1]))
            if node[0] != 'localhost':
                kill_enabled = False

        # create the chaos button
        if kill_enabled:
            chaosButton = wx.Button(pnl, label="Kill Primary", pos=(10,80), size=(250,50))
            self.Bind(wx.EVT_BUTTON, self.OnKill, chaosButton)
            self.button = chaosButton

        threading.Thread(target=self.updateStatus, args = (kill_enabled, )).start()

        toggleButton = wx.Button(pnl, label="Toggle Writes", pos=(270,80), size=(200,50))
        self.Bind(wx.EVT_BUTTON, self.OnToggle, toggleButton)
        
        vert_increment = 18
        current_y = 160

        # Create label
        self.stp = []
        dc = wx.ClientDC(pnl)
        max_text_len = 0
        for node in nodes:
            label = "%s:%s - " % (node[0], node[1])
            max_text_len = max(max_text_len, dc.GetTextExtent(label).GetWidth())
            stl = wx.StaticText(pnl, label=label, pos=(10,current_y))
            current_y += vert_increment

        # add labels for amount read
        current_y = 160
        threads = []
        for index in range(len(nodes)):
            node = nodes[index]
            self.stp.append(wx.StaticText(pnl, pos=(max_text_len + 10,current_y)))
            threads.append(threading.Thread(target=self.readFromServer, args=(index, node[0], node[1])))
            current_y += vert_increment

        # Start all threads at the same time
        for thread in threads:
            thread.start()

        # Add a slider with text 
        current_y += 20
        self.slidertxt = wx.StaticText(pnl, label='Inserting speed:'+str(self.writeSpeed), pos=(40,current_y))
        current_y += 18
        sliderwdg = wx.Slider(pnl, value=1, minValue=1, maxValue=10, pos=(10,current_y), size=(250,25), style=wx.SL_HORIZONTAL) 
        self.Bind(wx.EVT_SLIDER, self.OnSliderScroll, sliderwdg) 
		
        current_y += 32
        self.rb1 = wx.RadioButton(pnl,1, label = '1', pos = (10,current_y), style = wx.RB_GROUP) 
        current_y += 18
        self.rb2 = wx.RadioButton(pnl,2, label = '2', pos = (10,current_y)) 
        current_y += 18
        self.rb3 = wx.RadioButton(pnl,3, label = '3', pos = (10,current_y)) 
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadiogroup)
        self.rb1.SetValue(True)
        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()

    def parseKWArgs(self, kw):
        # pick our args out
        self.conn_str = None
        self.auth_args = None
        self.ssl = 'false'
        if 'conn_str' in kw:
            self.conn_str = kw['conn_str']
            kw.pop('conn_str')

            if self.conn_str:
                # Atlas
                if self.conn_str.find('mongodb.net'):
                    self.ssl = 'true'
                    # Find auth args between // and @
                    auth_args_start = self.conn_str.find('//')
                    auth_args_end = self.conn_str.find('@', auth_args_start)
                    self.auth_args = self.conn_str[auth_args_start + 2 : auth_args_end]

        if not self.conn_str:
            self.conn_str = 'mongodb://localhost:27001,localhost:27002,localhost:27003/?replicaSet=demoRS&retryWrites=true&serverSelectionTimeoutMS=5000'

    def writeData(self):
        i = 1
        while not self.closing:
            if self.doWrite:
                try:
                    self.db.numbers.insert({ "i" : i }, w=int(self.wc))
                    self.errlbl.SetLabel("")
                    i += 1
                except PyMongoError as ex:
                    self.errlbl.SetLabel("No primary available for writes")
                time.sleep(1/(self.writeSpeed))


    def readFromServer(self, index, server, port):
        server_conn_str = ""
        if self.auth_args:
            server_conn_str = 'mongodb://%s@%s:%d/?serverSelectionTimeoutMS=1000&connectTimeoutMS=1000&ssl=%s' % (self.auth_args, server, port, self.ssl)
        else:
            server_conn_str = 'mongodb://%s:%d/?serverSelectionTimeoutMS=1000&connectTimeoutMS=1000&ssl=%s' % (server, port, self.ssl)
        while not self.closing:
            lver = "unknown"
            count = 0
            try:
                lcl = MongoClient(server_conn_str)
                lver = lcl.server_info()['version']
                ldb = lcl.tfw
                count = list(ldb.numbers.aggregate([{ '$group': { '_id': 'null', 'sum': { '$sum': 1 }}}]))[0]['sum']
            except IndexError:
                count = 0
            except ServerSelectionTimeoutError:
                count = "Timeout"
            except PyMongoError as ex:
                count = ex
            except:
                count = ""
            if not self.closing:
                self.stp[index].SetLabel(str(count)+" (version:"+str(lver)+")")
            
            time.sleep(0.25)

    def updateStatus(self, kill_enabled):
        while not self.closing:
            try:
                primary = self.db.client.address
                pport = primary[1]

                if not self.closing:
                    self.st.SetLabel("Primary " + str(primary))

                if kill_enabled:
                    pids = [] 
                    for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
                        if proc.info['name'] == 'mongod' and \
                            any(x in self.local_ports for x in proc.info['cmdline']):
                            if str(pport) in proc.info['cmdline']:
                                self.ppid = proc.info['pid']
                                isPrim = True
                            else:
                                isPrim = False
                            pids.append(("Primary" if isPrim else "Secondary", proc.info['pid']))
                
                    if not self.closing:
                        self.stpid.SetLabel("PIDs: " + str(pids))

            except:
                pass
            time.sleep(0.5);

        

    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()

        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)
        
        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

        # Handle the frame closing
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)


    def OnToggle(self, event):
        if self.doWrite:
            self.doWrite = False
        else:
            self.doWrite = True

            
    def OnKill(self, event):
        """Kill button."""
        p = psutil.Process(self.ppid)
        p.kill()
        #p.terminate()
        #self.button.SetLabel("...done - Starting a new mongod in a moment")


    def OnSliderScroll(self, event):
        """Write speed slider."""
        obj = event.GetEventObject()
        self.writeSpeed = obj.GetValue()
        self.slidertxt.SetLabel('Inserting speed:'+str(self.writeSpeed))

    def OnRadiogroup(self, event):
        """Radion buttongroup pressed."""
        rb = event.GetEventObject()
        self.wc = int(rb.GetLabel()) 
        print(self.wc,'current write concern')
        
    def OnCloseFrame(self, event):
        # Mark window as closing
        self.closing = True
        # Destroy the window
        self.Destroy()

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a wxPython Hello World sample", 
                      "About Hello World 2",
                      wx.OK|wx.ICON_INFORMATION)


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    conn_str = None
    if len(sys.argv) > 1:
        conn_str = sys.argv[1]
    app = wx.App()
    frm = HelloFrame(None, title='TFW: Replica Set Resilience Demo', conn_str=conn_str)
    frm.Show()
    app.MainLoop()
