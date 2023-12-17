from Interface import *

if __name__ == '__main__':
    app = wx.App(False)
    frame = Interface(None,  style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
    frame.Show()
    app.MainLoop()