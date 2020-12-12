# pip install pandas opencv-python
# visit pyGuru on youtube

import cv2
import pandas as pd
import numpy as np

# --------------------------------------------------------------------------

img_path = 'colorpic.jpg'
csv_path = 'colors.csv'

# reading csv file
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv(csv_path, names=index, header=None)

# reading image
blnk_img = np.zeros((120, 800, 3))
img = cv2.imread(img_path)
img = cv2.resize(img, (800,600))

#declaring global variables
clicked = False
r = g = b = xpos = ypos = 0

#function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R,G,B):
	minimum = 1000
	for i in range(len(df)):
		d = abs(R - int(df.loc[i,'R'])) + abs(G - int(df.loc[i,'G'])) + abs(B - int(df.loc[i,'B']))
		if d <= minimum:
			minimum = d
			cname = df.loc[i, 'color_name']
	return cname

#function to get x,y coordinates of mouse double click
def draw_function(event, x, y, flags, params):
	if event == cv2.EVENT_MOUSEMOVE:
		global b, g, r, xpos, ypos, clicked
		clicked = True
		xpos = x
		ypos = y
		b,g,r = img[y,x]
		b = int(b)
		g = int(g)
		r = int(r)

# creating window
cv2.namedWindow('Image')
cv2.namedWindow('Color Details')
cv2.setMouseCallback('Image', draw_function)


while True:
	cv2.imshow('Image', img)
	cv2.imshow('Color Details', blnk_img)
	if clicked:
		#cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle 
		cv2.rectangle(blnk_img, (20,20), (700,100), (255,255,255), -1)

		#Creating text string to display( Color name and RGB values )
		text1 = get_color_name(r,g,b)
		text2 = 'R = ' + str(r) + ' G = ' + str(g) + ' B = ' + str(b)
		#cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
		cv2.putText(blnk_img, text1, (50,50), 2, 0.8, (0,0,0), 2, cv2.LINE_AA)
		cv2.putText(blnk_img, text2, (50,90), 2, 0.8, (0,0,0), 2, cv2.LINE_AA)

		#For very light colours we will display text in black colour
		# if r+g+b >=600:
		# 	cv2.putText(blnk_img, text1, (50,50), 2, 0.8, (0,0,0), 2, cv2.LINE_AA)
		# 	cv2.putText(blnk_img, text2, (50,90), 2, 0.8, (0,0,0), 2, cv2.LINE_AA)

	if cv2.waitKey(20) & 0xFF == 27:
		break

cv2.destroyAllWindows()
