import Tkinter,tkMessageBox,tkFont,traceback,time,datetime,random
import win32gui,win32api,win32con

from config import config
from src.window import Window
from src.app_exceptions import UserException
from src.coord import Coord

class RandomizeGUI(object):

    def randomize(self):
        try:
            self.log("========================================")
            self.log("Begin randomizing....")

            self.log("Activivating %s window"%config.TARGET_APP_NAME)
            self.target_app_window = AppWindow(config.TARGET_APP_NAME, self.config)
            self.target_app_window.activate()
            
            self.log("Detected %s"%self.target_app_window.get_client_coord())
            
            self.log("Making %s window visible"%config.TARGET_APP_NAME)
            self.target_app_window.make_visible()

            self.log("Choosing a random hero")
            self.target_app_window.click(random.choice(self.config.HERO_COORDS))
            self.target_app_window.click(self.config.CHOOSE_HERO)

    	    self.log("Build custom deck")
            time.sleep(self.config.MENU_DELAY)
            self.target_app_window.click(self.config.CUSTOM_DECK)
            self.target_app_window.click(self.config.CHOOSE_CUSTOM_DECK)

            random_cards = random.sample( range(self.config.CARDS_PER_PAGE*self.config.PAGES_PER_HERO), 
                                                             self.config.DECK_SIZE)

            self.log("Choosing cards: %s"%random_cards)
            self.choose_cards(random_cards)

            #self.target_app_window.get_screenshot().save('test.jpg','JPEG')
            self.log("Finished randomizing",'green')

        except UserException as e:
            self.log( str(e), 'red' )
        except Exception  as e:
            self.log( "ERROR: "+ str(e), 'red' )

    def choose_cards(self, cards):
        time.sleep(self.config.MENU_DELAY)
        page = 0
        for card in sorted(cards):
            for page in xrange(page, card//self.config.CARDS_PER_PAGE):
                self.target_app_window.click(self.config.NEXT_PAGE)
                time.sleep(self.config.PAGE_DELAY)
            
            page = card//self.config.CARDS_PER_PAGE

            time.sleep(self.config.CLICK_DELAY)
            self.target_app_window.click(self.config.CARD_PAGE_COORDS[card%self.config.CARDS_PER_PAGE])
    
    def log(self, message, color='blue'):
       now = datetime.datetime.now().strftime("%H:%M:%S")
       message = "<"+str(now)+">: "+message+'\n'
       self.textline+=1

       self.text.config(state=Tkinter.NORMAL)
       self.text.insert(Tkinter.END, message)
       self.text.tag_add(message, "%d.%d"%(self.textline, 1), "%d.%d"%(self.textline, len(str(now))+1))
       self.text.tag_config(message, background="white", foreground=color)
       self.text.config(state=Tkinter.DISABLED)
       self.text.see(Tkinter.END)

    def run(self):
        self.root.mainloop()

    def __init__(self, config):
        #master window
        self.root = Tkinter.Tk()
        self.config = config
        self.root.wm_title(self.config.APP_NAME)
        try:
            self.root.iconbitmap(self.config.ICON_PATH)
        except:
            pass

        #frame/grid
        self.frame = Tkinter.Frame(self.root, bd=2, relief=Tkinter.SUNKEN)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        #text box
        self.textline = 0
        self.yscrollbar = Tkinter.Scrollbar(self.frame)
        self.yscrollbar.grid(row=0, column=1, sticky=Tkinter.N+Tkinter.S)
        self.xscrollbar = Tkinter.Scrollbar(self.frame, orient=Tkinter.HORIZONTAL)
        self.xscrollbar.grid(row=1, column=0, sticky=Tkinter.E+Tkinter.W)
        self.text = Tkinter.Text(self.frame, wrap=Tkinter.NONE, bd=0,
                         xscrollcommand=self.xscrollbar.set,
                         yscrollcommand=self.yscrollbar.set)
        self.text.grid(row=0, column=0, sticky=Tkinter.N+Tkinter.S+Tkinter.E+Tkinter.W)
        self.xscrollbar.config(command=self.text.xview)
        self.yscrollbar.config(command=self.text.yview)

        #randomize button
        randomize_button = Tkinter.Button(self.frame,
                           text ="Randomize",
                           command = self.randomize,
                           font = tkFont.Font(family="System",size=42))
        randomize_button.grid(row=2, column=0, sticky=Tkinter.N+Tkinter.S+Tkinter.E+Tkinter.W)

        self.log("======%s======="%(config.APP_DESCRIPTION))
        self.log(config.HELP_MESSAGE)

        self.frame.pack()

class AppWindow(Window):

    def __init__(self, window_name, app_config):
        self.config = app_config
        self._last_cursor_pos = None
        super(AppWindow,self).__init__(window_name)
            
    def click(self, window_coord):
        time.sleep(self.config.PAGE_DELAY)
        if self._last_cursor_pos and self._last_cursor_pos != win32gui.GetCursorPos():
            raise UserException('Detected that the mouse was moved manually, aborting')

        standardized_width = (self._client_coord.height/self.config.STANDARD_SCALE.height)*self.config.STANDARD_SCALE.width
        padding = (self._client_coord.width - standardized_width) // 2

        standardized_x = padding +  (standardized_width/self.config.STANDARD_SCALE.height)*window_coord.x
        standardized_y = (self._client_coord.height/self.config.STANDARD_SCALE.height)*window_coord.y

        super(AppWindow,self).click(Coord(standardized_x, standardized_y))
        self._last_cursor_pos = win32gui.GetCursorPos()

if __name__ == "__main__":
    gui = RandomizeGUI(config())
    gui.run()
