import cv2
import sys

img = cv2.imread(sys.argv[1])
img_height, img_width, _ = img.shape
grid_height = int(sys.argv[2])
grid_width  = int(sys.argv[3])
grid_side_h = img_height/grid_height
grid_side_w = img_width/grid_width
counter = 1

print "h_i: {} || w_i: {}".format(img_height, img_width)

for i in range(1, grid_height+1):
    for j in range(1, grid_width+1):
        new_img = img[grid_side_h*(i-1):grid_side_h*i, grid_side_w*(j-1):grid_side_w*j]
        print "h: {} || w: {}".format(i,j)
        cv2.imwrite("img/img-%.3d.jpg" % (counter+1), new_img)
        counter = counter +1
