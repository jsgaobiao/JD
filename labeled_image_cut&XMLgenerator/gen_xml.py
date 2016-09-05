import cv2
import copy
import math
import sys
from cv2 import cv
import numpy as np

def sqr(x) :
    return x * x

# input : image & 4 paraments of a rectangle(centre, theta, width, height)
# output : the image enclosed by the rectangle
def subimage(image, centre, theta, width, height) :
    output_image = cv.CreateImage((width, height), image.depth, image.nChannels)
    mapping = np.array([[np.cos(theta), -np.sin(theta), centre[0]],
                        [np.sin(theta), np.cos(theta), centre[1]]])
    map_matrix_cv = cv.fromarray(mapping)
    cv.GetQuadrangleSubPix(image, output_image, map_matrix_cv)
    return output_image

# input : image & 4 points of a rectangle(start from the left-top point, anticlockwise)
# output : the image enclosed by the rectangle
def cutRect(image, points):
    centre = ((points[0][0] + points[2][0]) / 2.0, (points[0][1] + points[2][1]) / 2.0)
    width = math.sqrt(sqr(points[0][0] - points[1][0]) + sqr(points[0][1] - points[1][1]))
    height = math.sqrt(sqr(points[0][0] - points[3][0]) + sqr(points[0][1] - points[3][1]))
    theta = math.atan(float(points[1][0] - points[0][0]) / float(points[1][1] - points[0][1]))
    output = subimage(image, centre, theta, int(width), int(height))
    return output

def formatTheta(theta, x, y):
    if (x < 0 and y > 0):
        theta += math.pi
    if (x < 0 and y < 0):
        theta -= math.pi
    return theta

def rangeTheta(theta):
    while theta > math.pi:
        theta -= math.pi * 2
    while theta < - math.pi:
        theta += math.pi * 2
    return theta

# rotate anticlockwise
def boundingThetaRect(image, points, theta) :
    while theta > math.pi / 2.0:
        theta -= math.pi / 2.0
    while theta < -math.pi / 2.0:
        theta += math.pi / 2.0
    rot_points = copy.deepcopy(points)
    height, width, channels = image.shape
    mid_height = float(height) / 2.0
    mid_width = float(width) / 2.0
    # rotate clockwise
    tot = 0
    for point in points:
        point0 = float(float(point[0]) - mid_height)
        point1 = float(float(point[1]) - mid_width)
        length = math.sqrt(sqr(point0) + sqr(point1))
        if math.fabs(point0) < 0.000001:
            beta = math.atan(float(point1) / 0.000001)
        else:
            beta = math.atan(float(point1) / float(point0))
        beta = formatTheta(beta, point0, point1)
        alpha = beta + theta
        alpha = rangeTheta(alpha)
        rot_points[tot][1] = length * math.sin(alpha)
        rot_points[tot][0] = length * math.cos(alpha)
        tot += 1

    rot_points = rot_points.reshape((-1, 1, 2))
    x, y, w, h = cv2.boundingRect(rot_points)
    rot_rect = np.array([[x, y], [x, y + h], [x + w, y + h], [x + w, y]])
    # rotate back
    tot = 0
    ret = np.array([[x, y], [x, y + h], [x + w, y + h], [x + w, y]], np.int32)
    for point in rot_rect:
        length = math.sqrt(sqr(point[0]) + sqr(point[1]))
        if math.fabs(point[0]) < 0.000001:
            beta = math.atan(float(point[1]) / 0.000001)
        else:
            beta = math.atan(float(point[1]) / float(point[0]))
        beta = formatTheta(beta, point[0], point[1])
        alpha = beta - theta
        alpha = rangeTheta(alpha)
        ret[tot][1] = length * math.sin(alpha)
        ret[tot][0] = length * math.cos(alpha)
        ret[tot][1] += mid_width
        ret[tot][0] += mid_height
        tot += 1
    ret = ret.reshape((-1, 1, 2))
    return ret

def output_head(filename, img):
    fout.write("<annotation>\n")
    height, width, channels = img.shape
    fout.write("\t<filename>" + filename + "</filename>\n")
    fout.write("\t<size>\n")
    fout.write("\t\t<width>" + str(width) + "</width>\n")
    fout.write("\t\t<height>" + str(height) + "</height>\n")
    fout.write("\t\t<depth>" + str(channels) + "</depth>\n")
    fout.write("\t</size>\n")

def output_object(name, minx, miny, maxx, maxy):
    fout.write("\t<object>\n")
    fout.write("\t\t<name>" + name + "</name>\n")
    fout.write("\t\t<bndbox>\n")
    fout.write("\t\t\t<xmin>" + str(minx) + "</xmin>\n")
    fout.write("\t\t\t<ymin>" + str(miny) + "</ymin>\n")
    fout.write("\t\t\t<xmax>" + str(maxx) + "</xmax>\n")
    fout.write("\t\t\t<ymax>" + str(maxy) + "</ymax>\n")
    fout.write("\t\t</bndbox>\n")
    fout.write("\t</object>\n")

#############  example  ############
'''
ori = cv2.imread('porn.jpg')
img = cv.LoadImage('porn.jpg')

cnt = np.array([[200, 400], [200, 600], [300, 600], [300, 400]])
cv2.polylines(ori, [cnt], True, (0, 0, 255), 1)
poly = boundingThetaRect(ori, cnt, -0.9)   # rotate boundingRect anticlockwise
cv2.polylines(ori, [poly], True, (0, 255, 0), 2)

# given 4 points of a rectangle and cut it
#patch = subimage(img, (270,455), np.pi * 2, 100, 200)
patch = cutRect(img, [[200,400],[250,550],[350,500],[300,350]])
cv.ShowImage("cutRect", patch)

cv2.imshow("boundingThetaRect", ori)
cv2.waitKey(0)
'''
############# main ##############

arg1 = sys.argv[1]  #'porn.jpg'
arg2 = sys.argv[2]  #'porn.lbl'
arg3 = sys.argv[3]  #'porn.xml'
input_theta = 0

print arg1
ori = cv2.imread(arg1)
img = cv.LoadImage(arg1)
print arg1
fin = open(arg2)
fout = open(arg3, "w")

output_head(arg1, ori)
_height, _width, _channels = ori.shape

tot = 0
for line in fin:
    label = eval(line.rstrip('\n'))
    cnt = copy.deepcopy(label[1])
    cnt = np.array(cnt)
    cv2.polylines(ori, [cnt], True, (0, 0, 255), 1)
    poly = boundingThetaRect(ori, cnt, input_theta)   # rotate boundingRect anticlockwise
    _x, _y, _w, _h = cv2.boundingRect(poly)
    output_object(label[0], max(0,_x), max(0,_y), min(_width-1, _x + _w),min(_height-1, _y + _h))
    cv2.polylines(ori, [np.array([[_x, _y], [_x, _y + _h], [_x + _w, _y + _h], [_x + _w, _y]], np.int32)], True, (0, 255, 0), 2)

#cv2.imshow("boundingThetaRect", ori)
#cv2.waitKey(0)
fout.write("</annotation>\n")
fin.close()
fout.close()
