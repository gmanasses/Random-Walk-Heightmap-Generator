"""
    This algorithm makes a 16 bit grayscale heightmap using PIL libary, OpenCV and Numpy.
    With mode I;16, increasing pixel values until max value (65535)

    DIRECTIONS TO CHOOSE (BASED IN COMPASS ROSE)
       0        1        2
        \       |       /
    
     3 -- CURRENT PIXEL -- 4
    
        /       |       \
       5        6        7
"""

# Imports
from PIL import Image
from random import randrange
import cv2
import numpy as np
import time
import psutil
import os


# Fixed Vars
OUTPUT_FOLDER = "Images/Results/"
FILE_NAME = "HeightMap_RandomWalk"
FILE_FORMAT = ".png"
IMAGE_HEIGHT = 500
IMAGE_WIDTH = 500
MAX_PIXEL_VALUE = 65535

# Random Walk Vars 
STEP_SIZE = 1  # in pixels
TOTAL_NUMBER_OF_STEPS = 10700000
GRAYSCALE_CHANGE_PERCENTAGE = 0.007
CURRENT_POS = (IMAGE_HEIGHT//2, IMAGE_WIDTH//2)



# Functions
def GetRandomCompassRoseDirection():
    return randrange(0, 8)


def DoTheStep(currentPixelPos, direction, stepSize):
    for i in range(stepSize):
        futurePixel = GetFuturePixel(currentPixelPos, direction)

        pixelIsInside = CheckPixelIsInside(futurePixel)
        if not pixelIsInside:
            answer = ChangeDirection(currentPixelPos, direction)
            direction = answer[0]
            futurePixel = answer[1]

        colorToPaint = GetNewPixelColor(futurePixel)
        image.putpixel(futurePixel, colorToPaint)
 
        currentPixelPos = futurePixel

    return currentPixelPos


def GetFuturePixel(currentPixel, direction):
    futurePixel = currentPixel
    if direction == 0 :
        futurePixel = (futurePixel[0]-1, futurePixel[1]-1)
    elif direction == 1:
        futurePixel = (futurePixel[0], futurePixel[1]-1)
    elif direction == 2:
        futurePixel = (futurePixel[0]+1, futurePixel[1]-1)
    elif direction == 3:
        futurePixel = (futurePixel[0]-1, futurePixel[1])
    elif direction == 4:
        futurePixel = (futurePixel[0]+1, futurePixel[1])
    elif direction == 5:
        futurePixel = (futurePixel[0]-1, futurePixel[1]+1)
    elif direction == 6:
        futurePixel = (futurePixel[0], futurePixel[1]+1)
    elif direction == 7:
        futurePixel = (futurePixel[0]+1, futurePixel[1]+1)

    return futurePixel


def CheckPixelIsInside(pixel):
    if(pixel[0]>1 and pixel[0]<IMAGE_WIDTH-1) and (pixel[1]>1 and pixel[1]<IMAGE_HEIGHT-1):
        return True
    else:
        return False


def ChangeDirection(pixel, direction):
    futurePixel = pixel
    newDirection = direction
    if pixel[0] <= 1 and direction == 3:
        newDirection = 4
        futurePixel = GetFuturePixel(pixel, newDirection)
    elif pixel[0] <= 1 and direction == 0:
        newDirection = 2
        futurePixel = GetFuturePixel(pixel, newDirection)
    elif pixel[0] <= 1 and direction == 5:
        newDirection = 7
        futurePixel = GetFuturePixel(pixel, newDirection)
    elif pixel[1] <= 1 and direction == 0:
        newDirection = 5
        futurePixel = GetFuturePixel(pixel, newDirection)
    elif pixel[1] <= 1 and direction == 1:
        newDirection = 6
        futurePixel = GetFuturePixel(pixel, newDirection)
    elif pixel[1] <= 1 and direction == 2:
        newDirection = 7
        futurePixel = GetFuturePixel(pixel, newDirection)
    elif pixel[0] >= IMAGE_WIDTH-1 and direction == 2:
        newDirection = 0
        futurePixel = GetFuturePixel(pixel, newDirection)
    elif pixel[0] >= IMAGE_WIDTH-1 and direction == 4:
        newDirection = 3
        futurePixel = GetFuturePixel(pixel, newDirection)
    elif pixel[0] >= IMAGE_WIDTH-1 and direction == 7:
        newDirection = 5
        futurePixel = GetFuturePixel(pixel, newDirection)
    elif pixel[1] >= IMAGE_HEIGHT-1 and direction == 5:
        newDirection = 0
        futurePixel = GetFuturePixel(pixel, newDirection)
    elif pixel[1] >= IMAGE_HEIGHT-1 and direction == 6:
        newDirection = 1
        futurePixel = GetFuturePixel(pixel, newDirection)
    elif pixel[1] >= IMAGE_HEIGHT-1 and direction == 7:
        newDirection = 2
        futurePixel = GetFuturePixel(pixel, newDirection)
    return [newDirection, futurePixel]


def GetNewPixelColor(pixelPos):
    value = GetValueOfPixel(pixelPos)

    if(value == MAX_PIXEL_VALUE):
        return value
    else:
        newValue = int(value + (MAX_PIXEL_VALUE * GRAYSCALE_CHANGE_PERCENTAGE))
        if newValue > MAX_PIXEL_VALUE:
            newValue = MAX_PIXEL_VALUE

        return newValue


def GetValueOfPixel(pixelPosition):     
    return image.getpixel(pixelPosition)



# Main Function
if __name__ == "__main__":
    cpu_counter = 0
    totalCPUpercentage = 0
    process = psutil.Process(os.getpid())

    # Starting capture of execution time
    startTime = time.time()
    totalCPUpercentage = totalCPUpercentage + process.cpu_percent()
    cpu_counter = cpu_counter + 1

    # Creating a full black image to manipulating
    image = Image.new(mode="I;16", size=(IMAGE_WIDTH, IMAGE_HEIGHT))
    totalCPUpercentage = totalCPUpercentage + process.cpu_percent()
    cpu_counter = cpu_counter + 1

    # generating random walk
    for i in range(TOTAL_NUMBER_OF_STEPS // STEP_SIZE):
        CURRENT_POS = DoTheStep(CURRENT_POS, GetRandomCompassRoseDirection(), STEP_SIZE)
        totalCPUpercentage = totalCPUpercentage + process.cpu_percent()
        cpu_counter = cpu_counter + 1

    # converting to np array
    np_image = np.array(image)
    totalCPUpercentage = totalCPUpercentage + process.cpu_percent()
    cpu_counter = cpu_counter + 1

    # Applying GaussianBlur to make a better result
    gau_image = cv2.GaussianBlur(np_image, (5,5), 0)
    totalCPUpercentage = totalCPUpercentage + process.cpu_percent()
    cpu_counter = cpu_counter + 1

    # Showing and saving images
    cv2.imshow("Original Image", np_image)
    totalCPUpercentage = totalCPUpercentage + process.cpu_percent()
    cpu_counter = cpu_counter + 1

    cv2.imwrite(OUTPUT_FOLDER + FILE_NAME + FILE_FORMAT, np_image)
    totalCPUpercentage = totalCPUpercentage + process.cpu_percent()
    cpu_counter = cpu_counter + 1

    cv2.imshow("Gaussian Image", gau_image)
    totalCPUpercentage = totalCPUpercentage + process.cpu_percent()
    cpu_counter = cpu_counter + 1

    cv2.imwrite(OUTPUT_FOLDER +  "Gaussian_" + FILE_NAME + FILE_FORMAT, gau_image)
    totalCPUpercentage = totalCPUpercentage + process.cpu_percent()
    cpu_counter = cpu_counter + 1

    # Ending capture of execution time
    endTime = time.time()

    # Geting total time of execution
    totalTime = endTime - startTime
    print("Total Time: "+ str('%.3f' % totalTime) + " seconds")

    # Getting max % usage of RAM
    print('Memory used: ' + str('%.3f' % (process.memory_percent() * 100)) + " %")
    
    # Getting average % usage of CPU
    print('CPU USAGE: ' + str('%.3f' % ((totalCPUpercentage/cpu_counter) * 100)) + ' %')

    # Close all images with ESC key
    cv2.waitKey(0)
    cv2.destroyAllWindows()