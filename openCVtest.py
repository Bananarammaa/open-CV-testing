import cv2
import numpy as np

cap = cv2.VideoCapture(0)
camera_width = 240
camera_height = 320
center_x = 122
center_y = 150
angle_of_camera = 67
degrees_per_x_error = -angle_of_camera / camera_width
shouldGo = True

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([168,188,0])
    upper_blue = np.array([180,255,255])

    lower_teal = np.array([71,186,101])
    upper_teal = np.array([97,255,255])

    lower_red = np.array([162,181,60])
    upper_red = np.array([179,255,255])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    kernel = np.ones((3,3),np.uint8)
    erosion = cv2.erode(mask,kernel,iterations = 1)
    blur = cv2.blur(erosion,(9,9))
    dilation = cv2.dilate(mask,kernel,iterations = 3)#fills in stuff
    opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)#removes outside noise


    #image, contours = cv2.findContours(opening,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #image, contours, hierarchy = cv2.findContours(opening,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours,hierarchy = cv2.findContours(opening, 1, 2)




    if len(contours) < 1:
        print"there are no contours found"
    #else if (cv2.waitKey(0)) after the else runs, make a boolean switch and force the else if to be the only one to change it
    else:
        contour = contours[0]
        contourMax = 0
        contourMaxPerimeter = 0
        contourX = 0
        contourY = 0
        for contour in contours:
            M = cv2.moments(contour)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour,True)
            if perimeter > contourMaxPerimeter:
                contourMax = contour
                contourMaxPerimeter = perimeter
                contourX = cx
                contourY = cy






                print "LargestX: " +str(contourX)#    wpilib.SmartDashboard.putNumber("CUSTOM Largest x", contourX)
                print "LargestY: "+ str(contourY)#    wpilib.SmartDashboard.putNumber("CUSTOM Largest y", contourY)
                print "X Error: "+ str(center_x-contourX)#    wpilib.SmartDashboard.putNumber("CUSTOM X Error", self.center_x - contourX)
                print "Y error:"+ str(center_y-contourY)#    wpilib.SmartDashboard.putNumber("CUSTOM Y Error", self.center_y - contourY)
                print "rotation error"+ str(degrees_per_x_error*(center_x-contourX))#    wpilib.SmartDashboard.putNumber("CUSTOM Rotate Error", self.degrees_per_x_error * (self.center_x - contourX))



    #CONTOURS
    #contours, hierarchy = cv2.findContours(opening,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    #cv2.imshow('frame',frame)
                cv2.imshow('mask',mask)
    #cv2.imshow('res',res)
    #cv2.imshow('blur', contours)
    #cv2.imshow('erosion', erosion)

                cv2.waitKey(0)

                """k = cv2.waitKey(5) & 0xFF
                if k == 27:
                    break"""

                cv2.destroyAllWindows()
