import cv2
import imutils


def main():
    image = cv2.imread("../data/s1_chana.jpg", 1)
    image = imutils.resize(image, 500)
    cv2.imshow("Orignal Image", image)

    output = cv2.Canny(image, 100, 151, apertureSize=3, L2gradient=True)
    cv2.imshow("Edge Detected Image", output)
    output = cv2.erode(output,None,iterations =3)
    output = cv2.dilate(output,None, iterations =1)
    cv2.imshow('dilation',output)
    fill = cv2.fillConvexPoly

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
import cv2
import imutils


def main():
    image = cv2.imread("../data/moong.jpg", 1)
    o_image = imutils.resize(image, 1000)
    image = cv2.medianBlur(o_image,3)                 #Worked far better, removed all bad contours for chana 
                                                      # median blur worked better with 3 iterations with dilate 3
    #cv2.imshow("Orignal Image", o_image)

    output = cv2.Canny(image, 100, 151, apertureSize=3, L2gradient=True)
    cv2.imshow("Edge Detected Image", output)
    #output = cv2.medianBlur(output,11)                #Before dilation, useless
    output = cv2.dilate(output,None, iterations =1)
    cv2.imshow('dilation',output)
    thresh = cv2.threshold(output, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    _, cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    print(len(cnts))
    
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        roi = o_image[y:y + h, x:x + w]
        cv2.rectangle(o_image,(x,y),(x+w,y+h),(0,255,0),2)
        
    cv2.imwrite('../data/segmentd_19F_1.png',o_image)
    cv2.imshow('segmented', o_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
