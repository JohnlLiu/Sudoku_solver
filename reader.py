import cv2
import numpy as np
import operator

def read_img():

    image_url = 'test_puzzle.png' #load image from local file
    img = cv2.imread(image_url, cv2.IMREAD_GRAYSCALE) #apply grayscale to image
    proc = cv2.GaussianBlur(img.copy(), (9, 9), 0)  #gaussian blur to reduce noise obtain from thresholding 

    #adaptive thresholding used to segment image by splitting pixel to foreground and background based on intensity of pixel
    proc = cv2.adaptiveThreshold(proc, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11, 2)

    proc = cv2.bitwise_not(proc, proc) #invert colours in order to extract the grid

    kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]], np.uint8) #

    proc = cv2.dilate(proc, kernel) #dilation used to reduce noise in thresholding algorithm 

    #find contours and corners of the sudoku puzzle
    contours, h = cv2.findContours(proc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    puzzleCnt = None


    #loop through contours to find the cooridinates of the 4 corners
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            puzzleCnt = approx
            break    

    top_left = puzzleCnt[np.argmin([pt[0][0] + pt[0][1] for pt in puzzleCnt])][0]
    top_right = puzzleCnt[np.argmax([pt[0][0] - pt[0][1] for pt in puzzleCnt])][0]
    bottom_left = puzzleCnt[np.argmin([pt[0][0] - pt[0][1] for pt in puzzleCnt])][0]
    bottom_right = puzzleCnt[np.argmax([pt[0][0] + pt[0][1] for pt in puzzleCnt])][0]

    cv2.imshow("display", proc)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

read_img()
