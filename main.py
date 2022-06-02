
import cv2 as cv

from time import time

from win_api_capture import windowCapture

loop_time = time()

#w = 800
#h = 600
windoname = 'Sena_Innova_MinCiencias'

#Instanciando la clase

wincap = windowCapture(windoname)

#windowCapture.lis_window_names()
#exit()

while (True):
    
    #screen = np.array(get_screenshot(w,h,windoname))
    #screen = cv.cvtColor(screen,cv.COLOR_RGB2BGR)
    
    screen = wincap.get_screenshot()
    
    cv.imshow('Desktop', screen)
    print (f'FPS: { 1 / (time() - loop_time)}')
    loop_time = time()
    
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
   