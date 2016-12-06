import serial
import time
import wx
import glob
import sys
i = 0


def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def OnClick(event):
    global i
    pos = event.GetPosition()
    posx = 2.5*pos.y*0.27
    posy = 2.5*pos.x*(-0.25)+90
    spd = cFrame.choice.GetCurrentSelection()
    conne.serialconection(spd, int(posx), int(posy))
    i += 1
    cFrame.dialog.AppendText(
        "#%s, speed selection is: %s, slected position is :(%s,%s) \n" %
        (i, spd, int(posx), int(posy)))


def SpeedDef(event):
    speed = cFrame.choice.GetStringSelection()
    cFrame.dialog.AppendText("Current speed setting is %s. \n" % speed)


def PortChoices(event):
    com = cFrame.choice0.GetStringSelection()
    try:
        conne.reconect(com)
    except:
        cFrame.dialog.AppendText("%s is already connected\n" % com)


def pbutton(event):
    global i
    pos_x = cFrame.pos1.GetValue()
    pos_y = cFrame.pos2.GetValue()
    spd = cFrame.choice.GetCurrentSelection()

    conne.serialconection(spd, pos_x, pos_y)
    i += 1  # counter of step
    cFrame.dialog.AppendText(
        "#%s, speed selection is: %s, given position is :(%s,%s)\n" %
        (i, spd, pos_x, pos_y))


class SerialArdunio():

    def __init__(self, baud=9600, g_spd=1, g_pos1=78, g_pos2=15):
        self.port = serial_ports()
        self.baud = baud
        self.spd = g_spd
        self.pos1 = g_pos1
        self.pos2 = g_pos2
        self.ser = serial.Serial(self.port[0], self.baud, timeout=1)

    def reconect(self, com):
        self.ser = serial.Serial(com, self.baud, timeout=1)

    def serialconection(self, spd, posx, posy):
        # convert all type to string
        arrow = str(spd)+','+str(posx)+','+str(posy)
        self.ser.write(arrow.encode('ascii')+'\n')  # encode to ASCII


class MyFrame(wx.Frame):

    def __init__(self, parent=None, id=-1,):
        wx.Frame.__init__(
            self,
            parent,
            id,
            title="Servo Control",
            size=(
                600,
                335))
        self.sppedList = ['0', '1', '2']
        self.portlist = serial_ports()
        self.text0 = wx.StaticText(self, -1, "Port:", (225, 8))
        self.text1 = wx.StaticText(self, -1, "Speed:", (315, 8))
        self.choice0 = wx.Choice(self, -1, (250, 5), choices=self.portlist)
        self.choice0.SetStringSelection(self.portlist[0])
        self.choice = wx.Choice(self, -1, (350, 5), choices=self.sppedList)
        self.choice.SetStringSelection(self.sppedList[0])

        self.sendButton = wx.Button(
            self, label='Set', pos=(
                170, 5), size=(
                50, 25))
        self.text2 = wx.StaticText(self, -1, "pos.x", (5, 8))
        self.pos1 = wx.TextCtrl(self, pos=(35, 5), size=(50, 25))
        self.text3 = wx.StaticText(self, -1, "pos.y", (85, 8))
        self.pos2 = wx.TextCtrl(self, pos=(115, 5), size=(50, 25))
        self.dialog = wx.TextCtrl(
            self, pos=(
                5, 35), size=(
                390, 260), style=wx.TE_MULTILINE | wx.HSCROLL)
        self.dialog.AppendText(
            "Default setting is : Port : %s   Speed : %s \n" %
            (self.portlist[0], self.sppedList[0]))  # self.ww, self.wh = controlmap(self)
        self.sendButton.Bind(wx.EVT_BUTTON, pbutton)
        self.choice0.Bind(wx.EVT_CHOICE, PortChoices)
        self.choice.Bind(wx.EVT_CHOICE, SpeedDef)
        self.panel = wx.Panel(self)
        self.ImageBox()

    def ImageBox(self):
        image = wx.Image('controlmap.png')
        self.w = image.GetWidth()
        self.h = image.GetHeight()
        self.mapscale = image.Scale(self.w/2.5, self.h/2.5)
        self.bitmap = self.mapscale.ConvertToBitmap()
        self.cordmap = wx.StaticBitmap(
            self, -1, wx.BitmapFromImage(self.mapscale), (420, 15))

if __name__ == '__main__':
    app = wx.App()
    cFrame = MyFrame()
    cFrame.Center()
    cFrame.Show()
    cFrame.dialog.AppendText("Map size is(%d,%d)\n" % (cFrame.w, cFrame.h))
    time.sleep(1)
    cFrame.cordmap.Bind(wx.EVT_LEFT_DOWN, OnClick)
    conne = SerialArdunio()

    app.MainLoop()
