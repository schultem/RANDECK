import win32gui,win32api,win32con,ImageGrab
from window_rect import WindowRect

class Window(object):
    """Wrapper for PyHANDLE object operations"""

    def __init__(self, window_name):
        self.name = window_name
        self.hwnd = win32gui.FindWindow(None,self.name)
        if not self.hwnd:
            raise Exception('"%s" is not running, make sure it has been started.'%self.name)

    def coords_update(func):
       def func_wrapper(self, *args,**kwargs):
           self._set_coords()
           return func(self, *args,**kwargs)
       return func_wrapper

    @coords_update
    def make_visible(self):
        """Check if target window is completely visible or move it if it's not"""
        if self._client_coord.x > self._screen_coord.x or self._client_coord.y > self._screen_coord.y \
           or self._client_coord.origin_x < self._screen_coord.origin_x or self._client_coord.origin_y < self._screen_coord.origin_y:
            win32gui.MoveWindow(self.hwnd, 
                                self._screen_coord.origin_x, self._screen_coord.origin_y,
                                self._client_coord.width, self._client_coord.height, 
                                True)

    @coords_update
    def get_screenshot(self, rect=None):
        """Given a bounding WindowRect box return a PIL image of this window"""
        return ImageGrab.grab( (rect if rect else self._client_coord) )

    @coords_update
    def get_screen_coord(self):
        """Get a WindowRect of the screen resolution"""
        return self._screen_coord
        
    @coords_update
    def get_client_coord(self):
        """Get a WindowRect of the client app window"""
        return self._client_coord

    @coords_update
    def click(self, window_coord):
        """Click on a coord relative to this window client coordinates, ie from (0,0) to (width,height)"""
        coord = self._client_coord.origin + window_coord
        if coord.x > self._client_coord.x or coord.y > self._client_coord.y:
            raise Exception('Tried to click on %s which is outside of the "%s" window.'%(coord,self.name))

        win32api.SetCursorPos(tuple(coord))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,coord.x,coord.y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,coord.x,coord.y,0,0)

    def activate(self):
        """Make a target window the active top window"""
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOWNORMAL)
        win32gui.BringWindowToTop(self.hwnd)
        win32gui.SetForegroundWindow(self.hwnd)

    def _set_coords(self):
        self._client_coord = WindowRect(win32gui.GetWindowRect(self.hwnd))
        self._screen_coord = WindowRect((0,0,win32api.GetSystemMetrics(0),win32api.GetSystemMetrics(1)))
