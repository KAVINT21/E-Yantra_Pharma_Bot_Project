'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 1B of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_1b.py
# Functions:		detect_Qr_details, detect_ArUco_details
# 					[ Comma separated list of functions in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the five available  ##
## modules for this task                                    ##
##############################################################
import numpy as np
import cv2
from cv2 import aruco
import math
from pyzbar import pyzbar
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################





##############################################################

def detect_Qr_details(image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns a dictionary such
    that the message encrypted in the Qr code is the key and the center
    co-ordinates of the Qr code is the value, for each item in the dictionary

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `Qr_codes_details` : { dictionary }
            dictionary containing the details regarding the Qr code
    
    Example call:
    ---
    Qr_codes_details = detect_Qr_details(image)
    """    
    Qr_codes_details = {}

    img = image
    l = []

    for code in pyzbar.decode(img):
        decoded_data = code.data.decode("utf-8")
        rect_pts = code.rect
        if decoded_data:
            pts = np.array([code.polygon], np.int32)

            M = cv2.moments(pts)
            if M['m00'] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(img, (cx, cy), 7, (255, 0, 0), -1)
                l.append((cx, cy))

    decoded = pyzbar.decode(image)

    k = 0
    for i in decoded:
        for j in i:

            if type(j) == bytes:
                string = j.decode('utf-8')
                Qr_codes_details.update({string: list(l[k])})
                k += 1
    return Qr_codes_details
    


def detect_ArUco_details(image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns a dictionary such
    that the id of the ArUco marker is the key and a list of details of the marker
    is the value for each item in the dictionary. The list of details include the following
    parameters as the items in the given order
        [center co-ordinates, angle from the vertical, list of corner co-ordinates] 
    This order should be strictly maintained in the output

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `ArUco_details_dict` : { dictionary }
            dictionary containing the details regarding the ArUco marker
    
    Example call:
    ---
    ArUco_details_dict = detect_ArUco_details(image)
    """    
    ArUco_details_dict = {} #should be sorted in ascending order of ids
    ArUco_corners = {}

    id = []
    img = image

    marker_dict = aruco.Dictionary_get(aruco.DICT_5X5_50)
    param_markers = aruco.DetectorParameters_create()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, reject = aruco.detectMarkers(gray, marker_dict, parameters=param_markers)
    req1 = []
    k = 0

    for id1 in marker_IDs:
        id.append(int(id1[0]))

    req = []

    for i in marker_corners:
        req.append(tuple(i[0][0]))
        req1.append(tuple(i[0][0]))
        req1.append(tuple(i[0][1]))
        req1.append(tuple(i[0][2]))
        req1.append(tuple(i[0][3]))

    j = 1
    d1 = {}
    for i in req1:
        d1[j] = i
        j += 1

    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    ret, thresh = cv2.threshold(blur, 90, 255, cv2.THRESH_BINARY)

    Canny = cv2.Canny(thresh, 10, 70)
    contours, pt = cv2.findContours(Canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    l = []
    angle = []
    angle1 = []
    cnt = 0
    centers = []
    cont = []
    pos = []
    d = {}
    cnt1 = 0
    corners = []
    for c in contours:
        area = cv2.contourArea(c)
        if (area > 5000):
            # cv2.drawContours(img,c,-1,(0,255,0),3)

            M = cv2.moments(c)
            if M['m00'] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(img, (cx, cy), 7, (0, 0, 255), -1)
                centers.append((cx, cy))

                approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True)

                # cv2.circle(img,(261,260),7,(0,255,0),-1)
                color = (0, 255, 0)
                count = 1
                cnt += 1
                if (cnt % 2 == 0):
                    continue

                for i in approx:
                    corners.append(tuple(i[0]))
                    for j in i:
                        cnt1 += 1
                        k = tuple(j)
                        if (count == 1 or count == 2):
                            l.append(k)
                        if (count == 4):
                            angle.append(k)
                        if (count == 1 or count == 4):
                            angle1.append(k)
                        if (count == 2):
                            pos.append(k)
                        cv2.circle(img, k, 2, color, -1)
                        d[cnt1] = k
                        count += 1
                    if (count == 2):
                        color = (0, 0, 0)
                    elif (count == 3):
                        color = (255, 255, 255)
                    elif (count == 4):
                        color = (241, 82, 240)

    l1 = []
    i = 0
    j = 1

    while (j <= len(l)):
        l1.append([l[i], l[j]])
        i += 2
        j += 2

    c = 0

    for i in angle:
        extension = (i[0], i[1] - 100)

    j = 1
    k = 0

    points = angle1.copy()
    p = 2
    while (j <= len(angle1)):
        o = angle1[k][1] - 100
        points.insert(p, (angle1[k][0], o))
        p += 3
        k += 2  # 2
        j += 2

    for i in l1:
        cx = (i[0][0] + i[1][0]) // 2
        cy = (i[0][1] + i[1][1]) // 2

        cv2.line(img, centers[c], (cx, cy), (255, 0, 0), 3)
        c += 2

    res = []
    i = 0
    j = 1
    k = 2
    while (k <= len(points)):
        res.append([points[i], points[j], points[k]])
        i += 3
        j += 3
        k += 3

    def slope(p1, p2):
        return (p2[0] - p1[0]) / (p2[1] - p1[1])

    l = 0
    keys = []
    j = 0
    ans = []
    for i in res:
        b = i[-3]

        a = i[-1]

        c = i[-2]

        m1 = slope(b, a)

        m2 = slope(b, c)
        angle = math.atan((m2 - m1) / 1 + m1 * m2)
        angle = round(math.degrees((angle)))
        for key in d:
            for i in req:
                if (abs(i[0] - d[key][0]) <= 3 and abs(i[0] - d[key][0]) >= 0):
                    keys.append(key)
        diff1 = diff2 = diff3 = diff4 = 0
        for k in req1:
            if (abs(k[0] - b[0]) <= 27 and abs(k[0] - b[0]) >= 0 and abs(k[1]-b[1])<=27 and abs(k[1]-b[1])>=0):
                diff1 = abs(b[0] - k[0])
                diff2 = abs(b[1] - k[1])


                

                final1 = diff2 - diff1


            if (abs(k[0] - c[0]) <= 27 and abs(k[0] - c[0]) >= 0 and abs(k[1]-c[1])<=27 and abs(k[1]-c[1])>=0):
                diff3 = abs(c[0] - k[0])
                diff4 = abs(c[1] - k[1])

                final2 = diff4 - diff3


        answer=final1+final2

        if (keys[j] == 3 or keys[j] == 7 or keys[j] == 11 or keys[j] == 15 or keys[j] == 19 or keys[j] == 23 or keys[
            j] == 27 or keys[j] == 31):
            angle = (angle + 90 + answer)
        elif (keys[j] == 1 or keys[j] == 5 or keys[j] == 9 or keys[j] == 13 or keys[j] == 17 or keys[j] == 21 or keys[
            j] == 25 or keys[j] == 29):
            angle = (-(90 - angle + answer))
        elif (keys[j] % 4 == 0):
            angle = (-(180 - angle + answer))
        else:
            angle = angle + answer
        angle = int(angle)
        ans.append(angle)
        cv2.putText(img, str(angle), pos[l], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4)
        l += 1
        j += 1

    dictionary = {}
    list2 = []
    o = 0
    i = 0

    while (i < len(centers)):
        list1 = []
        list1.append(list(centers[i]))
        list1.append(ans[o])
        o += 1
        i += 2
        list2.append(list1)
    dictionary = {}
    j = 0
    for i in id:
        dictionary[i] = list2[j]
        j += 1

    '''sorted_value_index = np.argsort(dictionary.values())
    dictionary_keys = list(dictionary.keys())
    ArUco_details_dict = {dictionary_keys[i]: sorted(
        dictionary.values())[i] for i in range(len(dictionary_keys))}'''
    ArUco_details_dict=dictionary



    return ArUco_details_dict, ArUco_corners

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THE CODE BELOW #########	

# marking the Qr code with center and message

def mark_Qr_image(image, Qr_codes_details):
    for message, center in Qr_codes_details.items():
        encrypted_message = message
        x_center = int(center[0])
        y_center = int(center[1])
        
        cv2.circle(img, (x_center, y_center), 5, (0,0,255), -1)
        cv2.putText(image,str(encrypted_message),(x_center + 20, y_center+ 20),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2)

    return image

# marking the ArUco marker with the center, angle and corners

def mark_ArUco_image(image,ArUco_details_dict, ArUco_corners):

    for ids, details in ArUco_details_dict.items():
        center = details[0]
        cv2.circle(image, center, 5, (0,0,255), -1)

        corner = ArUco_corners[int(ids)]
        cv2.circle(image, (int(corner[0][0]), int(corner[0][1])), 5, (50, 50, 50), -1)
        cv2.circle(image, (int(corner[1][0]), int(corner[1][1])), 5, (0, 255, 0), -1)
        cv2.circle(image, (int(corner[2][0]), int(corner[2][1])), 5, (128, 0, 255), -1)
        cv2.circle(image, (int(corner[3][0]), int(corner[3][1])), 5, (255, 255, 255), -1)

        tl_tr_center_x = int((corner[0][0] + corner[1][0]) / 2)
        tl_tr_center_y = int((corner[0][1] + corner[1][1]) / 2) 

        cv2.line(image,center,(tl_tr_center_x, tl_tr_center_y),(255,0,0),5)
        display_offset = 2*int(math.sqrt((tl_tr_center_x - center[0])**2+(tl_tr_center_y - center[1])**2))
        cv2.putText(image,str(ids),(center[0]+int(display_offset/2),center[1]),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        angle = details[1]
        cv2.putText(image,str(angle),(center[0]-display_offset,center[1]),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    return image

if __name__ == "__main__":

    # path directory of images in test_images folder
    img_dir_path = "public_test_cases/"

    # choose whether to test Qr or ArUco images
    choice = input('\nWhich images do you want to test ? => "q" or "a": ')

    if choice == 'q':

        marker = 'qr'

    else:

        marker = 'aruco'

    for file_num in range(0,2):
        img_file_path = img_dir_path +  marker + '_' + str(file_num) + '.png'

        # read image using opencv
        img = cv2.imread(img_file_path)

        print('\n============================================')
        print('\nFor '+ marker  +  str(file_num) + '.png')

        # testing for Qr images
        if choice == 'q':
            Qr_codes_details = detect_Qr_details(img)
            print("Detected details of Qr: " , Qr_codes_details)

            # displaying the marked image
            img = mark_Qr_image(img, Qr_codes_details)
            cv2.imshow("img",img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # testing for ArUco images
        else:    
            ArUco_details_dict, ArUco_corners = detect_ArUco_details(img)
            print("Detected details of ArUco: " , ArUco_details_dict)

            #displaying the marked image
            img = mark_ArUco_image(img, ArUco_details_dict, ArUco_corners)  
            cv2.imshow("img",img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
