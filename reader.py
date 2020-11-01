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

squares = []
side = img.shape[:1]
side = side[0] / 9
for j in range(9):
    for i in range(0):
        p1 = (i * side, j * side)
        p2 = ((i+1) * side, (j+1) * side)
        squares.append((p1, p2))

def create_rect(img, square):
    return img[int(rect[0][1]):int(rect[1][1]), int(rect[0][0]):int(rect[1][0])]

def scale_and_centre(img, size, margin=0, background=0):

	h, w = img.shape[:2]

	def centre_pad(length):

		if length % 2 == 0:
			side1 = int((size - length) / 2)
			side2 = side1
		else:
			side1 = int((size - length) / 2)
			side2 = side1 + 1
		return side1, side2

	def scale(r, x):
		return int(r * x)

	if h > w:
		t_pad = int(margin / 2)
		b_pad = t_pad
		ratio = (size - margin) / h
		w, h = scale(ratio, w), scale(ratio, h)
		l_pad, r_pad = centre_pad(w)
	else:
		l_pad = int(margin / 2)
		r_pad = l_pad
		ratio = (size - margin) / w
		w, h = scale(ratio, w), scale(ratio, h)
		t_pad, b_pad = centre_pad(h)

	img = cv2.resize(img, (w, h))
	img = cv2.copyMakeBorder(img, t_pad, b_pad, l_pad, r_pad, cv2.BORDER_CONSTANT, None, background)
	return cv2.resize(img, (size, size))

def find_largest_feature(inp_img, scan_tl=None, scan_br=None):	

	img = inp_img.copy()  # Copy the image, leaving the original untouched
	height, width = img.shape[:2]

	max_area = 0
	seed_point = (None, None)

	if scan_tl is None:
		scan_tl = [0, 0]

	if scan_br is None:
		scan_br = [width, height]

	#Loop through the image
	for x in range(scan_tl[0], scan_br[0]):
		for y in range(scan_tl[1], scan_br[1]):
			#Only on light or white squares
			if img.item(y, x) == 255 and x < width and y < height:  
				area = cv2.floodFill(img, None, (x, y), 64)
				if area[0] > max_area:  #Gets the maximum bound area which should be the grid
					max_area = area[0]
					seed_point = (x, y)

	#Colour everything grey 
	for x in range(width):
		for y in range(height):
			if img.item(y, x) == 255 and x < width and y < height:
				cv2.floodFill(img, None, (x, y), 64)

	mask = np.zeros((height + 2, width + 2), np.uint8)  #Mask that is 2 pixels bigger than the image

	# Highlight the main feature
	if all([p is not None for p in seed_point]):
		cv2.floodFill(img, mask, seed_point, 255)

	top, bottom, left, right = height, 0, width, 0

	for x in range(width):
		for y in range(height):
			if img.item(y, x) == 64:  # Hide anything that isn't the main feature
				cv2.floodFill(img, mask, (x, y), 0)

			# Find the bounding parameters
			if img.item(y, x) == 255:
				top = y if y < top else top
				bottom = y if y > bottom else bottom
				left = x if x < left else left
				right = x if x > right else right

	bbox = [[left, top], [right, bottom]]
	return img, np.array(bbox, dtype='float32'), seed_point

def extract_digit(img, rect, size):
    digit = create_rect(img, rect)

    h, w = digit.shape[:2]
    margin = int(np.mean([h, w]) / 2.5)
    _, bbox, seed, = find_largest_feature(digit, [margin, margin], [w-margin, h-margin])
    digit = create_rect(digit, bbox)

    w = bbox[1][0] - bbox[0][0]
    h = bbox[1][1] - bbox[0][1]

    if w > 0 and h > 0 and (w * h) > 100 and len(digit) > 0:
        return scale_and_centre(digit, size, 4)
    else:
        return np.zeros((size, size), np.uint8) 

digits = []

for square in squares:
    digits.append(extract_digit(img, square, 28))


#show extracted digits
rows = []
with_border = [cv2.copyMakeBorder(img.copy(), 1, 1, 1, 1, cv2.BORDER_CONSTANT, None, 255) for img in digits]
for i in range(9):
    row = np.concatenate(with_border[i * 9:((i+1) * 9)], axis=1)
    rows.append(row)
img = np.concatenate(rows)


cv2.imshow("display", img)
cv2.waitKey(0)
cv2.destroyAllWindows()






