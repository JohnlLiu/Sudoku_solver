import cv2
import numpy as np
import operator


image_url = 'test_puzzle.png' #load image from local file
img = cv2.imread(image_url, cv2.IMREAD_GRAYSCALE) #apply grayscale to image

def pre_process(img, skip_dilate=None):
    proc = cv2.GaussianBlur(img.copy(), (9, 9), 0)  #gaussian blur to reduce noise obtain from thresholding 

    #adaptive thresholding used to segment image by splitting pixel to foreground and background based on intensity of pixel
    proc = cv2.adaptiveThreshold(proc, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11, 2)

    proc = cv2.bitwise_not(proc, proc) #invert colours in order to extract the grid

    kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]], np.uint8) #

    if skip_dilate is None:
        proc = cv2.dilate(proc, kernel) #dilation used to reduce noise in thresholding algorithm 

    return proc

proc = pre_process(img)

#find contours and corners of the sudoku puzzle
contours, h = cv2.findContours(proc, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)

puzzleCnt = None


#loop through contours to find the cooridinates of the 4 corners
for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    if len(approx) == 4:
        puzzleCnt = approx
        break    

#assign corners with corresponding cooridinates
top_left = puzzleCnt[np.argmin([pt[0][0] + pt[0][1] for pt in puzzleCnt])][0]
top_right = puzzleCnt[np.argmax([pt[0][0] - pt[0][1] for pt in puzzleCnt])][0]
bottom_left = puzzleCnt[np.argmin([pt[0][0] - pt[0][1] for pt in puzzleCnt])][0]
bottom_right = puzzleCnt[np.argmax([pt[0][0] + pt[0][1] for pt in puzzleCnt])][0]

#return top_left, top_right, bottom_left, bottom_right

#crop image
#top_left, top_right, bottom_right, bottom_left = crop_rect[0], crop_rect[1], crop_rect[2], crop_rect[3]
src = np.array([top_left, top_right, bottom_right, bottom_left], dtype='float32')

#function to calculate scalar distance between two points
def dist_between(p1, p2):
        a = p2[0] - p1[0]
        b = p2[1] - p1[1]
        return np.sqrt((a**2) + (b**2))

side = max([dist_between(bottom_left, top_right),
            dist_between(top_left, bottom_left),
            dist_between(bottom_right, bottom_left),
            dist_between(top_left, top_right)])

dst = np.array([[0, 0], [side - 1, 0], [side - 1, side - 1], [0, side - 1]], dtype='float32')
m = cv2.getPerspectiveTransform(src, dst)
n = cv2.warpPerspective(img, m, (int(side), int(side)))


#start to find grids from the sudoku puzzle

img = pre_process(n, skip_dilate=True)

edge_h = np.shape(img)[0]
edge_w = np.shape(img)[1]
celledge_h = edge_h // 9
celledge_w = edge_w // 9

tempGrid = []
for i in range(celledge_h, edge_h + 1, celledge_h):
    for j in range(celledge_h, edge_w + 1, celledge_w):
        rows = img[i - celledge_h: i]
        tempGrid.append([rows[k][j - celledge_w: j] for k in range(len(rows))])


cv2.imshow("display", img)
cv2.waitKey(0)
cv2.destroyAllWindows()






