from skimage.io import imread, imshow
from skimage.color import rgb2hsv
import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np


def get_marker_mask(img):
    img_hsv = rgb2hsv(img)
    #refer to hue channel (in the colorbar)
    lower_mask = img_hsv[:,:,0] > 0.1
    #refer to hue channel (in the colorbar)
    upper_mask = img_hsv[:,:,0] < 0.3
    #refer to transparency channel (in the colorbar)
    saturation_mask = img_hsv[:,:,1] < 0.2
 
    mask = upper_mask*lower_mask*saturation_mask    
    red = img[:,:,0]*mask
    green = img[:,:,1]*mask
    blue = img[:,:,2]*mask
    marker_masked = np.dstack((red,green,blue))
    return marker_masked

def get_coords(img):
    marker_masked=get_marker_mask(img)
    gray = cv.cvtColor(marker_masked ,cv.COLOR_RGB2GRAY)
    _,thresh = cv.threshold(gray,180, 255, cv.THRESH_BINARY_INV)
    cnt,_= cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    x,y=0,0
    for c in cnt:
        area=cv.contourArea(c)
        if area>100 and area<1000:
            x,y,w,h=cv.boundingRect(c)
            break
    return x,y

def get_mask(x,y,frame):   
    mask=np.zeros((frame.shape[0],frame.shape[1]),np.uint8)
    x2,y2=abs(x+500),abs(y+200)
    x1,y1=abs(x-200),abs(y-650)
    mask[y1:y2,x1:x2]=255

    return mask



# img=cv.imread('sample.png')

# img=cv.cvtColor(img,cv.COLOR_BGR2RGB)
# img=cv.resize(img,(1280,640))

# x,y=get_coords(img)
# mask=get_mask(x,y,img)
# cv.circle(img,(x,y),10,(0,255,0),thickness=-1)

# img=cv.cvtColor(img,cv.COLOR_RGB2BGR)
# img=cv.bitwise_and(img,img,mask=mask)

# cv.imshow('img',img)
# cv.waitKey(0)



#print(frame_width,frame_height)

# coords=(593,458)
# x1,y1=0,0

if __name__=="__main__":
    cap=cv.VideoCapture('video7.mp4')
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    size=(frame_width,frame_height)

    res = cv.VideoWriter('color_segmentation.avi', cv.VideoWriter_fourcc(*'MJPG'),24,size)
    while True:
        success, frame=cap.read()
        frame=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        frame=cv.resize(frame,(1280,640))

        x,y=get_coords(frame)
    
        if x>0 and y>0:
            x1,y1=x,y
            #cv.circle(frame,(x1,y1),10,(0,255,0),thickness=-1)
            mask=get_mask(x1,y1,frame)
            
        else:
            #cv.circle(frame,(x1,y1),10,(0,255,0),thickness=-1)
            mask=get_mask(x1,y1,frame)
    
        frame=cv.cvtColor(frame,cv.COLOR_RGB2BGR)

        frame=cv.bitwise_and(frame,frame,mask=mask)
        cv.imshow('View',frame)
        if success:
            frame=cv.resize(frame,(frame_width,frame_height))
            res.write(frame)

        if cv.waitKey(20) & 0XFF==ord('d'):
            break

    cap.release()
    cv.destroyAllWindows()


