import matplotlib.pyplot as plt
from builtins import range
import numpy
import os
import cv2


def compare_two_images(ref_image, blur_image, result, ref_height, ref_width):
    for row in range(ref_height):
        for col in range(ref_width):
            result[row][col] = result[row][col] + abs(int(ref_image[row][col]) - int(blur_image[row][col]))
    return result


def compare_images(ref_image, images):
    image_differentiate = []
    ref_height, ref_width = ref_image.shape
    print(ref_height, ref_width)
    for row in range(ref_height):
        temp_row = []
        for col in range(ref_width):
            temp_row.append(0)
        image_differentiate.append(temp_row)
    counter = 0
    for blur_image in images:
        print("Image {} is processed".format(counter))
        counter += 1
        image_differentiate = compare_two_images(ref_image, blur_image, image_differentiate, ref_height, ref_width)
    convert_result = numpy.array(image_differentiate)
    normalized_data = (255*(convert_result - numpy.min(convert_result))/numpy.ptp(convert_result)).astype(numpy.uint8)
    return normalized_data


def xor_results(first_input, second_input, selected_threshold):
    result = []
    for row in range(len(first_input)):
        temp_result = []
        for col in range(len(first_input[0])):
            if abs(first_input[row][col] - second_input[row][col]) > int(selected_threshold):
                temp_result.append(int(255))
            else:
                temp_result.append(int(0))
        result.append(temp_result)
    numpy_result = numpy.array(result)
    normalized_data = (255 * (numpy_result - numpy.min(numpy_result)) / numpy.ptp(numpy_result)).astype(numpy.uint8)
    cv2.imwrite('opencv_gray_{}.png'.format(selected_threshold), normalized_data)
    cv2.imshow("xor", normalized_data)
    cv2.waitKey(1000)


LeftImage = cv2.imread("data/im0.png", cv2.IMREAD_GRAYSCALE)
RightImage = cv2.imread("data/im1.png", cv2.IMREAD_GRAYSCALE)
width = 640
height = 480
desireSize = (width, height)
LeftImage = cv2.resize(LeftImage, desireSize)
RightImage = cv2.resize(RightImage, desireSize)

ParentPath = os.curdir
paths = []
DirectoryWithoutBlur = "result\\CannyWithoutBlurThreshold"
DirectoryWithBlur = "result\\CannyWithBlurThreshold"
BlurData = "result\\BlurData"

paths.append(BlurData)
paths.append(DirectoryWithoutBlur)
paths.append(DirectoryWithBlur)
for item in paths:
    path = os.path.join(ParentPath, item)
    if not os.path.exists(path):
        os.makedirs(path)

step = []
BlurImages = []
apply_canny_array_on_blur = []
apply_canny_array = []
selectedThreshold = 80
rightImages = []
leftImages = []
# in this part we reduce the quality of image by reduce size and change those image to 640*480
for percentage in numpy.arange(0.1, 1.05, 0.01):
    tempSize = (int(percentage * desireSize[0]), int(percentage * desireSize[1]))
    leftTemp = cv2.resize(LeftImage, tempSize)
    rightTemp = cv2.resize(RightImage, tempSize)
    leftImages.append(cv2.resize(leftTemp, desireSize))
    rightImages.append(cv2.resize(rightTemp, desireSize))


leftImage_differentiate = compare_images(LeftImage, leftImages)
cv2.imwrite("efe.png",leftImage_differentiate)
rightImage_differentiate = compare_images(RightImage, rightImages)
for threshold in range (0,200,10):
    xor_results(leftImage_differentiate, rightImage_differentiate, threshold)
