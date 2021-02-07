from Mesh import Mesh
import cv2


class MeshCreator:
    def __init__(self, width, height, mesh_width, mesh_height):
        self.width = width
        self.height = height
        self.meshWidth = mesh_width
        self.meshHeight = mesh_height
        self.num_of_row = int(self.height/self.meshHeight)
        self.num_of_col = int(self.width/self.meshWidth)
        self.meshList = []
        self.create_mesh()
        self.meshResult = []

    def create_mesh(self):
        for j in range(self.num_of_row):
            row_mesh_list = []
            for i in range(self.num_of_col):
                row_mesh_list.append(Mesh(i*self.meshWidth, j*self.meshHeight,self.meshWidth, self.meshHeight))
            self.meshList.append(row_mesh_list)
            self.meshList

    def get_white_counts_on_image(self, image):
        self.meshResult = []
        for j in range(self.num_of_row):
            temp_result = []
            for i in range(self.num_of_col):
                temp_result.append(self.meshList[j][i].count_of_white(image))
            self.meshResult.append(temp_result)
        return self.meshResult

    def draw_mesh(self, img):
        color = (255, 0, 0)
        thickness = int(2)
        for rowEle in self.meshList:
            for element in rowEle:
                mesh_corners = element.get_start_end_point()
                img = cv2.rectangle(img, mesh_corners["start"], mesh_corners["end"], color, 2)
        return img


