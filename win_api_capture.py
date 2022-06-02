
import  win32gui, win32ui, win32con
import numpy as np

class windowCapture:
       
    #Attributes
    
    w=0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0   
    offset_x = 0
    offset_y = 0
       
    #Constructor
    def __init__(self, window_name:str=None):
        
        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:        
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception(f'Window Not Found {window_name}')
        
        
        
        #Calculate window size
        
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect [0]
        self.h = window_rect[3] - window_rect [1]
        
        #Remove window border
        
        border_pixels = 1 #Modificar
        titlebar_pixels = 0 #Modificar
        
        self.w = self.w - (border_pixels *2)
        self.h = self.h - titlebar_pixels - border_pixels
        
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels  
        
        # account for offsets in image to get actual cords
        
        self.offset_x = window_rect [0] + self.cropped_x
        self.offset_y = window_rect [1] + self.cropped_y
    
    def get_screenshot(self): 

        #hwnd = win32gui.FindWindow(None, windowname)
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj,self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(self.w, self.h) , dcObj,(self.cropped_x,self.cropped_y), win32con.SRCCOPY)
        #cDC.BitBlt((0,0),(self.w, self.h) , dcObj,(0,0), win32con.SRCCOPY)

        #Save the screenshot
        #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')

        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape =(self.h,self.w,4)

        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        #Drop Alpha Channel
        img = img[...,:3]
        img = np.ascontiguousarray(img)
        
        return img

    def enum_window_titles(self):
        def callback(handle, data):
            titles.append(win32gui.GetWindowText(handle))

        titles = []
        win32gui.EnumWindows(callback, None)
        return titles
    
    @staticmethod
    def lis_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print (hex(hwnd), win32gui.GetWindowText( hwnd ))
        win32gui.EnumWindows( winEnumHandler, None )
    
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x,pos[1]+self.offset_y)


