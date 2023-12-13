''' ver from 3/9/22
clear all the un-necessay and add the From Date
this change is only for GIT to start - try gain mnual on17/11/23
'''
import wx
from  Komoot_Ana3 import K_Analize
from datetime import datetime as dt
from datetime import timedelta


class Mp3Panel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.data = [] # output to list
        self.index = 0
        self.conf = []
        self.summary = [] # output to summary
        self.build_panel(self.data)


    def build_panel(self, data):
        # -----change backgorund color -------#
        self.SetBackgroundColour("#8be587")
        font1 = wx.Font(15, family=wx.FONTFAMILY_MODERN, style=0, weight=90,
                       underline=True, faceName="", encoding=wx.FONTENCODING_DEFAULT)
        font2 = wx.Font(12, family=wx.FONTFAMILY_MODERN, style=0, weight=90,
                       underline=True, faceName="", encoding=wx.FONTENCODING_DEFAULT)

        self.labelOne = wx.StaticText(self, wx.ID_ANY, 'choose between the choices')
        self.labelOne.SetFont(font1)
        InputFour1_2 = ['Weekly Summary', 'Detailed Tours']
        InputFour3_4_5 = ['From last year', 'From day one', 'From date']
        self.rbox1_2 = wx.RadioBox(self, label='Report', pos=(100, 100), choices=InputFour1_2,
                                   majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox3_4_5 = wx.RadioBox(self, label='Duration', pos=(100, 100), choices=InputFour3_4_5,
                                majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox1_2.Bind(wx.EVT_RADIOBOX, self.onRadioBox1_2)
        self.inputFour1, self.inputFour2 = True, False #default values for radio box
        self.rbox3_4_5.Bind(wx.EVT_RADIOBOX, self.onRadioBox3_4_5)
        self.inputFour3, self.inputFour4, self.inputFour5 = True, False, False #default values for radio box
        self.DateTitle = wx.StaticText(self, wx.ID_ANY, ':Date DD/MM/YYYY')
        self.DateTitle.SetFont(font2)
        self.inputDate = wx.TextCtrl(self,  size = (100 ,25) ,value=':Date DD/MM/YYYY')
        self.inputDate.SetFont(font2)


        mainSizer = wx.BoxSizer(wx.VERTICAL) #Main sizer =>the table that everything go
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        # inputOneSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputFourSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputDateSizer = wx.BoxSizer(wx.HORIZONTAL)

        titleSizer.Add(self.labelOne,0,  wx.ALIGN_CENTER)
        inputFourSizer.Add(self.rbox1_2, 0, wx.ALL | wx.EXPAND, 10)
        inputFourSizer.Add(self.rbox3_4_5, 0, wx.ALL| wx.EXPAND,  10)

        inputDateSizer.Add(self.inputDate, 1, wx.ALL , 5)
        inputDateSizer.Add(self.DateTitle, 1, wx.ALL | wx.EXPAND, 10)
        mainSizer.Add(titleSizer, 0, wx.CENTER)

        mainSizer.Add(inputFourSizer, 0, wx.ALL | wx.TEXT_ALIGNMENT_RIGHT, 5)
        mainSizer.Add(inputDateSizer, 0, wx.ALL | wx.TEXT_ALIGNMENT_RIGHT, 5)


        #============ From here is the ListCTRL Box for the detailed list ============#
        self.list_ctrl = wx.ListCtrl( self, size = (-1, 350), style = wx.LC_REPORT | wx.BORDER_SUNKEN )
        self.list_ctrl.InsertColumn(0, "Number of Rides", width = 175)
        self.list_ctrl.InsertColumn(1, "Duration", width = 175)
        self.list_ctrl.InsertColumn(2, "Distance", width = 175)
        self.list_ctrl.InsertColumn(4, "1st Date of Week", width = 175)


        #-----fill the main tabel -------#
        #self.fill_table()

        self.summrizeWindow = wx.ListCtrl(
            self, size=(-1, 70),
            style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.EXPAND)

        self.summrizeWindow.InsertColumn(0, "Number of Rides", width=175)
        self.summrizeWindow.InsertColumn(1, "Duration", width=175)
        self.summrizeWindow.InsertColumn(2, "Distance", width=175)

        mainSizer.Add(self.list_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        edit_button = wx.Button(self, label = "Tours Summary")
        edit_button.Bind(wx.EVT_BUTTON, self.on_sum_btn)
        mainSizer.Add(edit_button, 0, wx.ALL | wx.CENTRE, 5)
        mainSizer.Add(self.summrizeWindow, 0, wx.ALL | wx.CENTER, 5)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)

    def fill_table(self):
        index = 0
        for i in self.data:
            self.list_ctrl.InsertItem(index, i[3])
            self.list_ctrl.SetItem(index, 1, str(i[1]))
            self.list_ctrl.SetItem(index, 2, str(i[2]))
            self.list_ctrl.SetItem(index, 3, str(i[0]))
            index += 1

    def fill_summary(self):
        #self.summrizeWindow.ClearAll()
        index = 0
        sum = self.summary
        self.summrizeWindow.InsertItem(index, str(sum[2]))
        self.summrizeWindow.SetItem(index, 1, (sum[0]))
        self.summrizeWindow.SetItem(index,2, (sum[1]))




    def on_sum_btn(self, event):
        if frame.pathname == '!':
            resp = wx.MessageBox('You must choose input file', 'Warning',
                                 wx.OK | wx.CANCEL | wx.ICON_WARNING)
        else:
            date = dt.today() - timedelta(days=365)
            self.getRadioStatus()
            if self.conf[5]== True:
                typed_date = self.inputDate.GetLineText(0)
                try:
                    date = dt.strptime(typed_date, "%d/%m/%Y")
                    print(date)
                except ValueError:
                    resp = wx.MessageBox('Date in format dd/mm/yyyy', 'Warning',
                                         wx.OK | wx.CANCEL | wx.ICON_WARNING)

            self.conf[0] = date.strftime("%m/%d/%Y") #in purpose the day and the month swapped because pandas takes
            #                                         it in the opposite places #
            run_k = K_Analize(frame.pathname, self.conf)
            run_k.fill_data()
            self.list_ctrl.DeleteAllItems() #cleen the screen
            self.data = run_k.data
            self.fill_table()   #fill the table on the screen
            self.summary =  run_k.summary
            # print(self.summary)
            self.fill_summary()

    def onRadioBox1_2(self, event):
        if self.rbox1_2.GetStringSelection() == "Weekly Summary":
            self.inputFour1, self.inputFour2 = True, False
        else:
            self.inputFour1, self.inputFour2 = False, True

        print(self.rbox1_2.GetStringSelection(), ' is clicked from Radio Box 1 2')

    def onRadioBox3_4_5(self, event):

        if self.rbox3_4_5.GetStringSelection() == "From last year":
            self.inputFour3, self.inputFour4, self.inputFour5 = True, False, False
        elif self.rbox3_4_5.GetStringSelection() == "From day one":
            self.inputFour3, self.inputFour4, self.inputFour5,  = False, True, False
        else:
            self.inputFour3, self.inputFour4, self.inputFour5 = False, False, True

        print(self.rbox3_4_5.GetStringSelection(), ' is clicked from Radio Box 3_4_5')



    def closeProgram(self):
        # self.GetParent() will get the frame which
        # has the .Close() method to close the program
        self.GetParent().Close()

    def getRadioStatus(self):
        '''
        this def collects data from all buttons
        '''
        conf = []
        # conf.append(self.inputTxtOne.GetValue())
        conf.append("This option canceled")
        conf.append(self.inputFour1)
        conf.append(self.inputFour2)
        conf.append(self.inputFour3)
        conf.append(self.inputFour4)
        conf.append(self.inputFour5)
        self.conf = conf
        ''' This one canceled because the program creates CSV file anyhow'''


#------------End of Class PANEL ----------------------#


class KomootFrame(wx.Frame):
    def __init__(self, parent = None):
        super().__init__(parent, -1, title = 'Komoot Tours  Statistical Tool by Doron Shafrir', size=(900, 720))
        self.SetMinSize((900, 600))
        self.CenterOnParent()
        self.create_panel()
        self.create_menu()
        self.Show()
        self.pathname = ''

    def create_panel(self):
        self.panel = Mp3Panel(self)

    def create_menu(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        user_menu = wx.Menu()
        menu_bar.Append(file_menu, '& HTML File')
        menu_bar.Append(user_menu, "&Change User")
        open_folder_menu_item = file_menu.Append(wx.ID_ANY, 'Open File', 'Open a file with html extension')
        create_file_to_update_item = file_menu.Append(wx.ID_ANY, 'Update the main file', 'create a file with csv extension')
        user_menu_change = user_menu.Append(wx.ID_ANY, 'change user name and passwerd', 'create new user name')

        self.Bind(event = wx.EVT_MENU, handler = self.on_open_file, source = open_folder_menu_item)
        self.Bind(event = wx.EVT_MENU, handler = self.on_update, source= create_file_to_update_item)
        self.Bind(event = wx.EVT_MENU, handler=self.change_user, source=user_menu_change)
        self.SetMenuBar(menu_bar)

    def on_open_folder(self, event):
        title = "Choose a directory: "
        dlg = wx.DirDialog(self, title, style = wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.panel.update_mp3_list((dlg.GetPath()))
        dlg.Destroy()

    def on_open_file(self, event):

        with wx.FileDialog(self, "Open .html file", wildcard="html file (*.html)|*.html",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            #Proceed loading the file chosen by the user
            self.pathname = fileDialog.GetPath()
            print (self.pathname)
    #--Once you activate the update in menue it will go and create new main from the html file.
    def on_update(self, event):
        pseudo_conf = [True, False, False, True]
        dlg = wx.MessageDialog(None, "Do you want to update?", 'Updater', wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            if frame.pathname == '':
                resp = wx.MessageBox('You must choose input file', 'Warning',
                                     wx.OK | wx.CANCEL | wx.ICON_WARNING)
            else:
                #Fetch_Data(self.pathname)
                run_k = K_Analize(frame.pathname, pseudo_conf)
                run_k.create_from_html()

        else:
            pass

    def change_user(self, event):
        pass

if __name__ == '__main__':
    app = wx.App(False)
    frame = KomootFrame()
    app.MainLoop()