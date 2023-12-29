'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 1A of Pharma Bot (PB) Theme (eYRC 2022-23).
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
# Filename:			task_1a.py
# Functions:		detect_traffic_signals, detect_horizontal_roads_under_construction, detect_vertical_roads_under_construction,
#					detect_medicine_packages, detect_arena_parameters
# 					[ Comma separated list of functions in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import cv2
import numpy as np


##############################################################

################# ADD UTILITY FUNCTIONS HERE #################


##############################################################

def detect_traffic_signals(maze_image):

    img = maze_image
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img2 = cv2.GaussianBlur(img2, (5, 5), 0)
    Canny = cv2.Canny(img2, 75, 150)
    img4 = Canny
    l_r = np.array([0, 100, 100])
    u_r = np.array([10, 255, 255])
    l_b = np.array([110, 50, 50])
    u_b = np.array([130, 255, 255])
    mask2 = cv2.inRange(hsv, l_b, u_b)
    res1 = cv2.bitwise_and(img, img, mask=mask2)

    mask = cv2.inRange(hsv, l_r, u_r)
    res = cv2.bitwise_and(img, img, mask=mask)
    ress = cv2.bitwise_or(res, res1)
    ress1 = cv2.cvtColor(ress, cv2.COLOR_BGR2GRAY)

    corners = cv2.goodFeaturesToTrack(ress1, 150, 0.01, 50)
    corners = np.int0(corners)
    l = []

    for i in corners:
        x, y = i.ravel()
        cv2.circle(img, (x, y), 3, (0, 255, 0), -1)
        l.append((x, y))
    l.reverse()
    l.sort()
    alpha = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'C1', 'C2', 'C3', 'C4', 'C5',
             'C6', 'C7', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'F1', 'F2',
             'F3', 'F4', 'F5', 'F6', 'F7', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7']
    d = {}
    j = 0
    for al in alpha:
        d[al] = l[j]
        j = j + 1

    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    corners1 = cv2.goodFeaturesToTrack(gray, 150, 0.001, 50)
    corners1 = np.int0(corners1)
    l1 = []

    for j in corners1:
        x, y = j.ravel()
        l1.append((x, y))

    traffic_signals = []

    for k in l1:
        for key in d:
            if (d[key] == k):
                traffic_signals.append(key)
    traffic_signals.sort()

    return traffic_signals


def detect_vertical_roads_under_construction(maze_image):
    """
    Purpose:
    ---
    This function takes the image as an argument and returns a list
    containing the missing horizontal links

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `horizontal_roads_under_construction` : [ list ]
            list containing missing horizontal links

    Example call:
    ---
    horizontal_roads_under_construction = detect_horizontal_roads_under_construction(maze_image)
    """
    vertical_roads_under_construction = []

    img = maze_image
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    l_r = np.array([0, 100, 100])
    u_r = np.array([10, 255, 255])
    l_b = np.array([110, 50, 50])
    u_b = np.array([130, 255, 255])
    mask2 = cv2.inRange(hsv, l_b, u_b)
    res1 = cv2.bitwise_and(img, img, mask=mask2)

    mask = cv2.inRange(hsv, l_r, u_r)
    res = cv2.bitwise_and(img, img, mask=mask)
    ress = cv2.bitwise_or(res, res1)
    ress1 = cv2.cvtColor(ress, cv2.COLOR_BGR2GRAY)

    corners = cv2.goodFeaturesToTrack(ress1, 150, 0.01, 50)
    corners = np.int0(corners)
    l = []

    for i in corners:
        x, y = i.ravel()
        cv2.circle(img, (x, y), 3, (0, 255, 0), -1)
        l.append((x, y))
    l.reverse()

    l.sort()

    d = l[7][0] - l[0][0]

    de = int(d / 2)
    for i in range(7):
        for j in range(6):
            width = l[0][0] + (i * d)

            height = l[0][1] + (j * d) + de

            a = img[height][width]

            if a[0] == 255 and a[1] == 255 and a[2] == 255:
                f = 1 + j
                vertical_roads_under_construction.append((chr(65 + i) + str(1 + j) + "-" + chr(65 + i) + str(2 + j)))
    return vertical_roads_under_construction


def detect_horizontal_roads_under_construction(maze_image):
    """
    Purpose:
    ---
    This function takes the image as an argument and returns a list
    containing the missing vertical links

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `vertical_roads_under_construction` : [ list ]
            list containing missing vertical links

    Example call:
    ---
    vertical_roads_under_construction = detect_vertical_roads_under_construction(maze_image)
    """
    horizontal_roads_under_construction = []

    img = maze_image

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    l_r = np.array([0, 100, 100])
    u_r = np.array([10, 255, 255])
    l_b = np.array([110, 50, 50])
    u_b = np.array([130, 255, 255])
    mask2 = cv2.inRange(hsv, l_b, u_b)
    res1 = cv2.bitwise_and(img, img, mask=mask2)

    mask = cv2.inRange(hsv, l_r, u_r)
    res = cv2.bitwise_and(img, img, mask=mask)
    ress = cv2.bitwise_or(res, res1)
    ress1 = cv2.cvtColor(ress, cv2.COLOR_BGR2GRAY)

    corners = cv2.goodFeaturesToTrack(ress1, 150, 0.01, 50)
    corners = np.int0(corners)
    l = []

    for i in corners:
        x, y = i.ravel()
        cv2.circle(img, (x, y), 3, (0, 255, 0), -1)
        l.append((x, y))
    l.reverse()

    l.sort()

    d = l[7][0] - l[0][0]

    de = int(d / 2)

    for i in range(6):
        for j in range(7):
            width = l[0][0] + (i * d) + de

            height = l[0][1] + (j * d)

            a = img[height][width]

            if a[0] == 255 and a[1] == 255 and a[2] == 255:
                horizontal_roads_under_construction.append(
                    (chr(65 + i) + str(1 + j) + "-" + chr(65 + i + 1) + str(1 + j)))

    return horizontal_roads_under_construction


def detect_medicine_packages(maze_image):
    """
    Purpose:
    ---
    This function takes the image as an argument and returns a nested list of
    details of the medicine packages placed in different shops

    ** Please note that the shop packages should be sorted in the ASCENDING order of shop numbers
       as well as in the alphabetical order of colors.
       For example, the list should first have the packages of shop_1 listed.
       For the shop_1 packages, the packages should be sorted in the alphabetical order of color ie Green, Orange, Pink and Skyblue.

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `medicine_packages` : [ list ]
            nested list containing details of the medicine packages present.
            Each element of this list will contain
            - Shop number as Shop_n
            - Color of the package as a string
            - Shape of the package as a string
            - Centroid co-ordinates of the package
    Example call:
    ---
    medicine_packages = detect_medicine_packages(maze_image)
    """
    medicine_packages = []

    img = maze_image
    cropped = img[96:206, 96:706]
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY_INV)
    hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)

    res = cv2.bitwise_and(cropped, cropped, mask=thresh)

    l_b = np.array([110, 50, 50])
    u_b = np.array([130, 255, 255])

    mask = cv2.inRange(hsv, l_b, u_b)
    res1 = cv2.bitwise_and(cropped, cropped, mask=mask)

    ress1 = cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)

    corners = cv2.goodFeaturesToTrack(ress1, 150, 0.01, 10)
    corners = np.int0(corners)
    l = []

    for i in corners:
        x, y = i.ravel()
        cv2.circle(cropped, (x, y), 3, (0, 255, 0), -1)
        l.append((x, y))
    l.sort()

    i = 0
    j = 108
    k = 190
    m = 108
    p = 190
    h = 0
    # img[98:196,108:196]
    l4 = []

    dic1 = {'A1': (22, 22), 'A2': (22, 62), 'A3': (62, 22), 'A4': (62, 62), 'A5': (22, 21), 'A6': (22, 61),
            'A7': (62, 21), 'A8': (62, 61)}
    d1 = {'A1': [130, 130], 'A2': [130, 170], 'A3': [170, 130], 'A4': [170, 170], 'A5': [130, 129], 'A6': [130, 169],
          'A7': [170, 129], 'A8': [170, 169]}

    dic2 = {'A1': (22, 22), 'A2': (22, 62), 'A3': (62, 22), 'A4': (62, 62), 'A5': (22, 21), 'A6': (22, 61),
            'A7': (62, 21), 'A8': (62, 61)}
    d2 = {'A1': [230, 130], 'A2': [230, 170], 'A3': [270, 130], 'A4': [270, 170], 'A5': [230, 129], 'A6': [230, 169],
          'A7': [270, 129], 'A8': [270, 169]}

    dic3 = {'A1': (22, 22), 'A2': (22, 62), 'A3': (62, 22), 'A4': (62, 62), 'A5': (22, 21), 'A6': (22, 61),
            'A7': (62, 21), 'A8': (62, 61)}
    d3 = {'A1': [330, 130], 'A2': [330, 170], 'A3': [370, 130], 'A4': [370, 170], 'A5': [330, 129], 'A6': [330, 169],
          'A7': [370, 129], 'A8': [370, 169]}

    dic4 = {'A1': (22, 22), 'A2': (22, 62), 'A3': (62, 22), 'A4': (62, 62), 'A5': (22, 21), 'A6': (22, 61),
            'A7': (62, 21), 'A8': (62, 61)}
    d4 = {'A1': [430, 130], 'A2': [430, 170], 'A3': [470, 130], 'A4': [470, 170], 'A5': [430, 129], 'A6': [430, 169],
          'A7': [470, 129], 'A8': [470, 169]}

    dic5 = {'A1': (22, 22), 'A2': (22, 62), 'A3': (62, 22), 'A4': (62, 62), 'A5': (22, 21), 'A6': (22, 61),
            'A7': (62, 21), 'A8': (62, 61)}
    d5 = {'A1': [530, 130], 'A2': [530, 170], 'A3': [570, 130], 'A4': [570, 170], 'A5': [530, 129], 'A6': [530, 169],
          'A7': [570, 129], 'A8': [570, 169]}

    dic6 = {'A1': (22, 22), 'A2': (22, 62), 'A3': (62, 22), 'A4': (62, 62), 'A5': (22, 21), 'A6': (22, 61),
            'A7': (62, 21), 'A8': (62, 61)}
    d6 = {'A1': [630, 130], 'A2': [630, 170], 'A3': [670, 130], 'A4': [670, 170], 'A5': [630, 129], 'A6': [630, 169],
          'A7': [670, 129], 'A8': [670, 169]}

    while (i < len(l)):
        l3 = []
        colors = []
        crop = img[j:k, m:p]
        gray1 = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray1, 240, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        hsv_frame = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        h += 1
        shop = "Shop_" + str(h)
        if (shop == "Shop_1"):
            dictionary = dic1
            answer = d1
        elif (shop == "Shop_2"):
            dictionary = dic2
            answer = d2
        elif (shop == "Shop_3"):
            dictionary = dic3
            answer = d3
        elif (shop == "Shop_4"):
            dictionary = dic4
            answer = d4
        elif (shop == "Shop_5"):
            dictionary = dic5
            answer = d5
        elif (shop == "Shop_6"):
            dictionary = dic6
            answer = d6

        l2 = []
        for c in contours:

            approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True)
            cv2.drawContours(img, [approx], 0, (255, 0, 0), 5)
            M = cv2.moments(c)
            if M['m00'] != 0:
                x = int(M['m10'] / M['m00'])
                y = int(M['m01'] / M['m00'])
                cv2.circle(crop, (x, y), 2, (0, 0, 0), -1)
                l2.append((x, y))
                pixel_center = hsv_frame[y, x]
                hue_value = pixel_center[0]
                if (hue_value < 22):
                    color = "Orange"


                elif (hue_value < 78):
                    color = "Green"


                elif (hue_value < 131):
                    color = "Skyblue"



                else:
                    color = "Pink"

                if (len(approx) == 3):

                    s = "Triangle"
                elif (len(approx) == 4):

                    s = "Square"
                else:

                    s = "Circle"
                colors.append(color)

        s1 = 0
        for f in l2:
            for key in dictionary:
                if (f == dictionary[key]):
                    ans = answer[key]
            l3.append([shop, colors[s1], s, ans])
            s1 = s1 + 1
        l3.sort(key=lambda x: x[1])
        if (len(l3) != 0):
            l4.append(l3)

        p += 100
        m += 100
        i += 4

    for i in l4:
        for j in i:
            medicine_packages.append(j)

    return medicine_packages


def detect_arena_parameters(maze_image):
    """
    Purpose:
    ---
    This function takes the image as an argument and returns a dictionary
    containing the details of the different arena parameters in that image

    The arena parameters are of four categories:
    i) traffic_signals : list of nodes having a traffic signal
    ii) horizontal_roads_under_construction : list of missing horizontal links
    iii) vertical_roads_under_construction : list of missing vertical links
    iv) medicine_packages : list containing details of medicine packages

    These four categories constitute the four keys of the dictionary

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `arena_parameters` : { dictionary }
            dictionary containing details of the arena parameters

    Example call:
    ---
    arena_parameters = detect_arena_parameters(maze_image)
    """
    arena_parameters = {}

    traffic = detect_traffic_signals(maze_image)
    hori = detect_horizontal_roads_under_construction(maze_image)
    veri = detect_vertical_roads_under_construction(maze_image)
    medicine = detect_medicine_packages(maze_image)

    arena_parameters['traffic_signals'] = traffic
    arena_parameters['horizontal_roads_under_construction'] = hori
    arena_parameters['vertical_roads_under_construction'] = veri
    arena_parameters['medicine_packages_present'] = medicine

    return arena_parameters


######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########

if __name__ == "__main__":

    # path directory of images in test_images folder
    img_dir_path = "C:\\Users\\91984\\Desktop\\elon\\PB_Task1_Windows\\Task1A\\public_test_images\\"

    # path to 'maze_0.png' image file
    file_num = 0
    img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'
    print(img_file_path)
    # read image using opencv
    maze_image = cv2.imread(img_file_path)

    print('\n============================================')
    print('\nFor maze_' + str(file_num) + '.png')

    # detect and print the arena parameters from the image
    arena_parameters = detect_arena_parameters(maze_image)

    print("Arena Prameters: ", arena_parameters)

    # display the maze image
    cv2.imshow("image", maze_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    choice = input('\nDo you want to run your script on all test images ? => "y" or "n": ')

    if choice == 'y':

        for file_num in range(1, 15):
            # path to maze image file
            img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'

            # read image using opencv
            maze_image = cv2.imread(img_file_path)

            print('\n============================================')
            print('\nFor maze_' + str(file_num) + '.png')

            # detect and print the arena parameters from the image
            arena_parameters = detect_arena_parameters(maze_image)

            print("Arena Parameter: ", arena_parameters)

            # display the test image
            cv2.imshow("image", maze_image)
            cv2.waitKey(2000)
            cv2.destroyAllWindows()



