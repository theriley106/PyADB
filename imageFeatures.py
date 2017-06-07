'''
Created on 2014/01/27

@author: MOMO
'''
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import Image
path = 'a.jpg'
'''
@param path: image path
@return: image's brightness evaluated in its YUV space
''' 
def get_brightness_feature(path=path):
    img = cv2.imread(path)
    YUV = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    sum = 0.0
    count = 0.0
    for i in range(0, len(YUV)):
        for j in range(0, len(YUV[0])):
            element = YUV[i][j]
            count = count+1
            sum = sum+element[0]
    #print "get image: "+ path+"'s brightness feature. (" + str(sum/count)+")"
    return sum/count

'''
@param path: image path
@return: image's average saturation evaluated in its HSV space
'''
def get_saturation_feaure(path=path):
    img = cv2.imread(path)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    sum = 0.0
    count = 0.0
    for i in range(0, len(hsv)):
        for j in range(0, len(hsv[0])):
            element = hsv[i][j]
            count = count+1
            sum = sum+element[1]
    #print "get image: "+ path+"'s saturation feature. (" + str(sum/count)+")"
    return sum/count

'''
@param path: image path
@return: image's colorfulness feature evaluated in its rgb space 
'''
def get_colorfulness_feature(path=path):
    imgBGR = cv2.imread(path)
    img = np.array(imgBGR, dtype='int64')
    rg = []
    yb = []
    for i in range(0, len(img)):
        for j in range(0, len(img[0])):
            element = img[i][j]
            rg.append(float(element[2]-element[1]))
            temp = float(element[2]+element[1])
            yb.append(temp/2-element[0])
    numrg = np.array(rg)
    numyb = np.array(yb)
    drg = np.std(numrg)
    dyb = np.std(numyb)
    arg = np.average(numrg)
    ayb = np.average(numyb)
    cf = math.sqrt(math.pow(drg, 2)+math.pow(dyb, 2))+0.3*math.sqrt(math.pow(arg,2)+math.pow(ayb,2))
    #print "get image: "+ path+"'s colorfulness feature. (" + str(cf)+")"
    return cf

'''
@param path: image path
@return: image's naturalness feature evaluated in its HSL space
'''
def get_naturalness_feature(path=path):
    img = cv2.imread(path)
    hls = cv2.cvtColor(img,cv2.COLOR_BGR2HLS)
    skin = []
    grass = []
    sky = []
    count = 0.0
    for i in range(0, len(hls)):
        for j in range(0, len(hls[0])):
            element = hls[i][j]
            count = count + 1
            if element[1]>=20 and element[1]<=80 and element[2]>0.1:
                if element[0]>=25 and element[0]<=70:
                    skin.append(element[2])
                elif element[0]>=95 and element[0]<=135:
                    grass.append(element[2])
                elif element[0]>=185 and element[0]<=260:
                    sky.append(element[2])
                else:
                    pass
    if len(skin)==0:
        askin = 0.0
    else:
        askin = np.average(np.array(skin))
        
    if len(grass)==0:
        agrass = 0.0
    else:
        agrass = np.average(np.array(grass))
        
    if len(sky)==0:
        asky = 0.0
    else:
        asky = np.average(np.array(sky))
    
    n_skin = math.pow(math.e, -0.5*math.pow((askin-0.76)/0.52,2))
    n_grass = math.pow(math.e, -0.5*math.pow((agrass-0.81)/0.53,2))
    n_sky = math.pow(math.e, -0.5*math.pow((asky-0.43)/0.22,2))
    n = (len(skin)/count)*n_skin+(len(grass)/count)*n_grass+(len(sky)/count)*n_sky
    #print "get image: "+ path+"'s naturalness feature. (" + str(n)+")"
    return n

'''
@param path: image path
@return: image's contrast feature evaluated in its gray space
'''
def get_contrast_feature(path=path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    avg = np.average(np.array(gray))
    sum = 0.0
    count = 0.0
    for i in range(0, len(gray)):
        for j in range(0, len(gray[0])):
            element = gray[i][j]
            count = count+1
            sum = sum + math.pow((element-avg), 2)
    c = sum/(count-1)
    #print "get image: "+ path+"'s contrast feature. (" + str(c)+")"
    return c

'''
@param path: image path
@return: image's sharpness feature
'''
def get_sharpness_feature(path=path):
    kernel_size = 3
    scale = 1
    delta = 0
    ddepth = cv2.CV_16S

    img = cv2.imread(path)
    img = cv2.GaussianBlur(img,(3,3),0)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    gray_lap = cv2.Laplacian(gray,ddepth,ksize = kernel_size,scale = scale,delta = delta)
    s = np.max(np.array(gray_lap))
    #print "get image: "+ path+"'s sharpness feature. (" + str(s)+")"
    return s
#test
#code

def GrabAttractiveness(d):
    return(str(get_brightness_feature(d) + get_sharpness_feature(d) + get_contrast_feature(d) + get_naturalness_feature(d) + get_colorfulness_feature(d) + get_saturation_feaure(d))[0:2])

#print(GrabAttractiveness('e.jpg'))