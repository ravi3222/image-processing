import cv2
import numpy as np

# For OpenCV2 image display
WINDOW_NAME = 'leafTracker' 

def track(image):

    '''Accepts BGR image as Numpy array
       Returns: (x,y) coordinates of centroid if found
                (-1,-1) if no centroid was found
                None if user hit ESC
    '''
    orig_img= image.copy()
    # Blur the image to reduce noise
    blur = cv2.GaussianBlur(image, (5,5),0)
    #blur = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HLS)

    #Convert to grayscale
    gray = cv2.cvtColor(hsv,cv2.COLOR_BGR2GRAY)

    # Threshold the image
    thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV+ cv2.THRESH_OTSU)[1]# + cv2.THRESH_OTSU)[1]
    
    #Dilation
    thresh = cv2.dilate(thresh, None, iterations=3)
    #cv2.imwrite('thresh7/Threshold6_{}.jpg'.format(frame_count),thresh)
    
    #Contour
    image, contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    xz=0
    yz=xz
    count=1
    o_img= orig_img.copy()
    for c in contours:
        #print(c)
        if cv2.contourArea(c) >= 300:
            x, y, w, h = cv2.boundingRect(c)
            roi = orig_img[y-yz:y + h+ yz, x-xz:x + w+ xz]            
            cv2.rectangle(o_img,(x,y),(x+w,y+h),(0,255,0),2)
            M = cv2.moments(c)
            print(M)
            if 0 not in roi.shape:
                print("[INFO]: Image {}: Shape: {} Area: ({}) Location: ({},{},{},{})...".format(count, roi.shape, cv2.contourArea(c),x,y,w,h))
                Centroid = (int((x + x + w) /2), int((y + y + h) /2))
                YCentroid= (y+y+h)/2
                #cv2.circle(frame, Centroid, 1, (0, 0, 255), 4)
                cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 255, 255), 2)
                #print("[INFO]: extracted loaction: {}...".format(path))
                print("ROI======>",roi.shape,"Area:",cv2.contourArea(c))
                # Display full-color image
                cv2.imshow(WINDOW_NAME, o_img)

                # Force image display, setting centroid to None on ESC key input
                if cv2.waitKey(1) & 0xFF == 27:
                    ctr = None

"""
    # Take the moments to get the centroid
    moments = cv2.moments(bmask)
    m00 = moments['m00']
    centroid_x, centroid_y = None, None
    if m00 != 0:
        centroid_x = int(moments['m10']/m00)
        centroid_y = int(moments['m01']/m00)

    # Assume no centroid
    ctr = (-1,-1)

    # Use centroid if it exists
    if centroid_x != None and centroid_y != None:

        ctr = (centroid_x, centroid_y)

        # Put black circle in at centroid in image
        cv2.circle(image, ctr, 4, (0,0,0))

    # Display full-color image
    cv2.imshow(WINDOW_NAME, image)

    # Force image display, setting centroid to None on ESC key input
    if cv2.waitKey(1) & 0xFF == 27:
        ctr = None
    
    # Return coordinates of centroid
    return ctr
"""

# Test with input from camera
if __name__ == '__main__':

    capture = cv2.VideoCapture('F:/image-processing/object-tracking/sample.MTS')

    while True:

        okay, image = capture.read()

        if okay:

            if not track(image):
                break
          
            if cv2.waitKey(1) & 0xFF == 27:
                break

        else:

           print('Capture failed')
           break