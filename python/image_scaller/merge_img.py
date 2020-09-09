# -*- coding: utf-8 -*-

import cv2
import sys
import numpy as np
import png

image_slices_path   = sys.argv[1]       #путь слайсов
new_image_name      = sys.argv[2]      #имя изображения
# new_image_h         = int(sys.argv[3])  #высота в px
# new_image_w         = int(sys.argv[4])  #ширина в px
new_image_side_h    = int(sys.argv[3])  #высота в частяъх
new_image_side_w    = int(sys.argv[4])  #ширина в частях

counter = 0

slice_list = []

for count_slice_h in range(0:new_image_side_h):
        for count_slice_w in range(0:new_image_side_w):
                slice_list.append(cv2.imread(image_slices_path + "img_{0:0>3}.jpg".format(counter+1)))
                

def mergeRows(slice_list, rowNum):
        newRow = np.zeros((1, 112000, 3), np.uint8)
        for i in range(len(slice_list)-1):
                newRow[i:i, 10000*(i-1):10000*i]

                


# ==================================== OLD CODE =========================================
# new_image = np.zeros((new_image_h, new_image_w, 3), np.uint8)
# new_image.fill(255)
# image_part_h = new_image_h/new_image_side_h
# image_part_w = new_image_w/new_image_side_w
# counter = 1

# #print "h_i: {} || w_i: {}".format(img_height, img_width)

# for i in range(1, new_image_side_h+1):
#     for j in range(1, new_image_side_w+1):
#         img_part = cv2.imread("C:\Users\Illusion of control\Desktop\waifu2x-DeadSix27-vc15-cv401-win64_v523_no_unicode\out\img_{0:0>3}.jpg".format(counter+1))
#         # smth = np.zeros((100, 100, 3), np.uint8)
#         # smth1 = np.zeros((100, 100, 3), np.uint8)
#         # smth[0:100, 0:100]= smth1 #img_part[0:100, 0:100]
#         # break
#         #new_image[(image_part_h*(i-1)):(image_part_h*i), (image_part_w*(j-1)):(image_part_w*j)] = img_part
#         new_image[image_part_h*(i-1):image_part_h*i, image_part_w*(j-1):image_part_w*j]  = img_part
#         print "h: {} || w: {}".format(i,j)
#         cv2.imwrite("C:\Users\Illusion of control\Documents\Projects\home.scripts\image_scaller\%" + str(counter) + new_image_name, new_image)
#         counter = counter +1
# #cv2.imwrite(new_image_name, smth)
# #cv2.imwrite("C:\Users\Illusion of control\Documents\Projects\home.scripts\image_scaller\%" + new_image_name, new_image)