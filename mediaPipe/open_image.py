import cv2
import sys

img = cv2.imread('capture.jpg')
if img is None:
    sys.exit('Could Not Read the image')
    
cv2.imshow('Title', img)

k = cv2.waitKey(0)

while k == cv2.waitkey('q'):
    if k == ord("q"):
        sys.exit("done")

    
    #cv2.destroyAllWindows()
