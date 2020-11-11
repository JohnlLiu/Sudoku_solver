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
def get_Contour(proc):
	cont, h = cv2.findContours(proc.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cont = sorted(cont, key=cv2.contourArea, reverse=True)

	return cont

contours = get_Contour(proc)

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

def extract_digit(cell, debug=False):
	thresh = cv2.threshold(cell, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	thresh = clear_border(thresh)

	if debug:
		cv2.imshow("Cell Thresh", thresh)
		cv2.waitKey(0)

	cnts = get_Contour(thresh)

	if len(cnts) == 0:
		return None
	
	c = max(cnts, key=cv2.contourArea)
	mask = np.zeros(thresh.shape, dtype="uint8")
	cv2.drawContours(mask, [c], -1, 255, -1)

	(h, w) = thresh.shape
	percentFilled = cv2.countNonZero(mask) / float(w * h)

	if percentFilled < 0.03:
		return None
	
	digit = cv2.bitwise_and(thresh, thresh, mask=mask)

	if debug:
		cv2.imshow("Digit", digit)
		cv2.waitKey(0)
	
	return digit

cv2.imshow("display", img)
cv2.waitKey(0)
cv2.destroyAllWindows()






