import win32gui,win32api,win32con,ImageGrab
from app_exceptions import UserException

class Window(object):
    """Wrapper for PyHANDLE object operations"""

    def __init__(self, window_name):
        self.name = window_name
        self.hwnd = win32gui.FindWindow(None,name)
        if not self.hwnd:
            raise UserException('Check that "%s" is running.'%self.name)

    def activate():
        """Make a target window the active top window"""
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOWNORMAL)
        win32gui.BringWindowToTop(self.hwnd)
        win32gui.SetForegroundWindow(self.hwnd)

    def make_visible():
        """Check if target window is completely visible or raise UserException"""
        window_rect = win32gui.GetWindowRect(self.hwnd)
        resolution_rect = (0,0,win32api.GetSystemMetrics(0),win32api.GetSystemMetrics(1))
    
        if window_rect[2]>resolution_rect[2] or window_rect[3]>resolution_rect[3] \
           or window_rect[0]<0 or window_rect[1]<0:
            raise UserException('TODO: need to move the target app window if it is not entirely visible.')

    def get_screenshot(hwnd):
        return ImageGrab.grab(win32gui.GetWindowRect(hwnd))
