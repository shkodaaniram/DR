import wx
import wx.lib.agw.genericmessagedialog as GMD
import os
import cv2
import numpy as np
import utils
import CONST
import OD_localization

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(900, 657))
        self.createMenu()
        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        rightPanel = wx.Panel(panel, -1)
        leftPanel = wx.Panel(panel, -1, style=wx.SUNKEN_BORDER)
        img = wx.EmptyImage(CONST.screen_resol_x, CONST.screen_resol_y)
        self.Image = wx.StaticBitmap(leftPanel, wx.ID_ANY, wx.BitmapFromImage(img))
        leftPanel.SetBackgroundColour('black')

        localize_disc = wx.Button(rightPanel, -1, 'Localize', size=(170, -1))
        self.Bind(wx.EVT_BUTTON, self.localize_optic_disc, id=localize_disc.GetId())

        leftPanel.SetSizer(vbox)
        hbox.Add(rightPanel, 0, wx.EXPAND | wx.RIGHT, 5)
        hbox.Add(leftPanel, 1, wx.EXPAND)
        hbox.Add((3, -1))
        panel.SetSizer(hbox)
        self.Centre()
        self.Show(True)

    def initConst(self):
        self.FILEPATH = ''
        self.IMAGE_ID = ''
        self.EYE_ORIENT = ''
        self.IMAGE = []

    def createMenu(self):
        menubar = wx.MenuBar()
        file = wx.Menu()
        help = wx.Menu()
        file.Append(101, '&Open\tCtrl+O', 'Open a new document')
        file.Append(102, '&Save\tCtrl+S', 'Save the document')
        file.AppendSeparator()
        quit = wx.MenuItem(file, 105, '&Quit\tCtrl+Q', 'Quit the Application')
        help.Append(106, '&About\tCtrl+H')
        file.AppendItem(quit)
        menubar.Append(file, '&File')
        menubar.Append(help, '&Help')
        self.SetMenuBar(menubar)
        self.CreateStatusBar()

        self.Centre()
        self.Bind(wx.EVT_MENU, self.onQuit, id=105)
        self.Bind(wx.EVT_MENU, self.onOpenImage, id=101)
        self.Bind(wx.EVT_MENU, self.onSaveImage, id=102)
        self.Bind(wx.EVT_MENU, self.onAboutBox, id=106)

    def onAboutBox(self, event):
        main_message = "This program should be used for optic disc localization on fundus eye images.\n\n" + \
            "For image loading pick menu item 'File'->'Open' or 'Ctrl+O' then select image to download.\n" + \
            "For image saving pick menu item 'File'->'Save' or 'Ctrl+S'.\n" + \
            "Pick menu item 'File'->'Quit' or 'Ctrl+Q' to close the program.\n" + \
            "\n   Program includes automatic and non-automatic modes.\n" + \
            "1. Automatic mode: pick 'Automatic' type of localization and click on 'Localize' button.\n" + \
            "2. Non-automatic mode: pick 'Non-automatic' type of localization, click on the center of\n" + \
            "   optic disc on the image, after that click on 'Localize' button.\n" + \
            "After image processing finished the successful message will be displayed.\n\n\n" + \
            "     Also program has several additional options.\n" + \
            "1. Click on 'Binarization' button to view result of image binarization which is used to " + \
            "   truncate image.\n" + \
            "2. Click on 'Green channel' button to view green channel of RGB image.\n" + \
            "3. Click on 'Morphological operations' button to view result of applying image closing\n" + \
            "   and opening to selected image.\n" + \
            "4. Click on 'Truncate' button to view result of truncated image.\n"
        dlg = GMD.GenericMessageDialog(None, main_message, "Help", agwStyle=wx.ICON_INFORMATION | wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def onQuit(self, event):
        self.Close()

    def onOpenImage(self, event):
        filters = 'Image files(*.bmp;*.png;*.jpg;*.jpeg)|*.bmp;*.png;*.jpg;*.jpeg'
        dlg = wx.FileDialog(self, message="Open an Image...", defaultDir=os.getcwd(),
                            defaultFile="", wildcard=filters, style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            orientAndId = ((dlg.GetFilename()).split('.')[0]).split('_')
            print 'filename: ' + filename
            self.FILEPATH = filename
            self.IMAGE_ID = orientAndId[0]
            self.EYE_ORIENT = orientAndId[-1].lower()
            self.onViewImage(filename)

        dlg.Destroy() # we don't need the dialog any more so we ask it to clean-up

    def onViewImage(self, filepath):
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        self.Width = img.GetWidth()
        self.Height = img.GetHeight()
        img_scaled = utils.onScaleImg(img)
        self.Image.SetBitmap(wx.BitmapFromImage(img_scaled))
        self.Refresh()
        #image resizing
        cv2.imwrite(CONST.resized_img_path, utils.resizeImg(self.FILEPATH))
        print 'Image resized and ready to be processed'

    def onSaveImage(self, event):
        filters = 'Image files(*.bmp;*.png;*.jpg;*.jpeg)|*.bmp;*.png;*.jpg;*.jpeg'
        dlg = wx.FileDialog(self, message="Save an Image...", defaultDir=os.getcwd(),
                            defaultFile="", wildcard=filters, style=wx.SAVE | wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            print filename
            cv2.imwrite(filename, cv2.imread(self.FILEPATH_RESULT))
        dlg.Destroy() # we don't need the dialog any more so we ask it to clean-up

    def localize_optic_disc(self, event):
        OD_localization.get_optic_disc(self)

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'Optic disk localization and vessels segmentation')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop()
