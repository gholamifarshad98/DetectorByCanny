from meshCreator import MeshCreator
import matplotlib.pyplot as plt
from builtins import range
import numpy
import os
import cv2

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
# in this part we reduce the quality of image by reduce size and change those image to 640*480
for percentage in numpy.arange(0.1, 1.05, 0.01):
    tempName1 = "BlurImage_percentage_size{}.png".format(int(percentage*100))
    fileAddress1 = os.path.join(paths[0], tempName1)
    tempName2 = "BlurImage_percentage_size_canny{}.png".format(int(percentage*100))
    fileAddress2 = os.path.join(paths[1], tempName2)
    tempSize = (int(percentage * desireSize[0]), int(percentage * desireSize[1]))
    firstStep = cv2.resize(LeftImage, tempSize)
    secondStep = cv2.resize(firstStep, desireSize)
    BlurImages.append(secondStep)
    cv2.imshow("BlurImages image", secondStep)
    cv2.imwrite(fileAddress1,secondStep)
    thirdStep = cv2.Canny(secondStep, selectedThreshold, selectedThreshold)
    apply_canny_array_on_blur.append(thirdStep)
    cv2.imshow("resized image", thirdStep)
    cv2.imwrite(fileAddress2,thirdStep)
    cv2.waitKey(300)

# In this part we change the threshold of canny algorithm
for threshold in range(20, 200, 5):
    LeftImageApplyCanny = cv2.Canny(LeftImage, threshold, threshold)
    tempName = "Threshold{}.png".format(threshold)
    fileAddress = os.path.join(paths[2], tempName)
    apply_canny_array.append(LeftImageApplyCanny)
    step.append(threshold)
    cv2.imwrite(fileAddress, LeftImageApplyCanny)
    cv2.imshow("changing threshold", LeftImageApplyCanny)
    cv2.waitKey(300)

# in this part we mesh 640*480 to grid size (grid_width,grid_height) and after that
# we count number of detected corner in canny algorithm in each grid for each threshold.
grid_width = 80
grid_height = 80
MyMeshCreator = MeshCreator(desireSize[1], desireSize[0], grid_width, grid_height)
meshedImage = MyMeshCreator.draw_mesh(LeftImage)
cv2.imshow("mesh",meshedImage)
cv2.waitKey(100)
results = dict()
i = 0

for image in apply_canny_array:
    print(i)
    results[i] = list(MyMeshCreator.get_white_counts_on_image(image))
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
    i = i + 1
# In this part we count ratio of decrease in number of detected corner
# in canny algorithm in each grid for each threshold.
accumulatedWhitePixel = []
differentiateOfWhite = []
diffStep = []
grid_row = 4
grid_col = 2
for stepInThreshold in results:
    accumulatedWhitePixel.append(results[stepInThreshold][grid_row][grid_col])
for i in range(len(step)-1):
    diffStep.append(step[i])
    differentiateOfWhite.append(-accumulatedWhitePixel[i+1]+accumulatedWhitePixel[i])
fig = plt.figure()
ax1 = fig.add_subplot(121)
plt.title('Grid index is [{},{}]'.format(grid_row,grid_col))
ax2 = fig.add_subplot(122)
plt.title('Grid index is [{},{}]'.format(grid_row,grid_col))
ax1.plot(step, accumulatedWhitePixel)
ax2.plot(diffStep, differentiateOfWhite)
ax1.set_xlabel('threshold')
ax1.set_ylabel('Number of White pixel')
ax2.set_xlabel('threshold')
ax2.set_ylabel('Rate of decrease in number of White pixel')
plt.show()
