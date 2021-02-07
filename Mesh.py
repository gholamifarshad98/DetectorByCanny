class Mesh:
    def __init__(self, start_x, start_y, width, height):
        self.width = width
        self.height = height
        self.startX = start_x
        self.startY = start_y

    def count_of_white(self, input_image):
        white_counter = 0
        for i in range(self.width):
            for j in range(self.height):
                if input_image[self.startX+i, self.startY + j] >= 200:
                    white_counter = white_counter + 1
        return white_counter

    def get_start_end_point(self):
        corners = dict()
        start_point = (self.startY, self.startX)
        end_point = (self.startY + self.height, self.startX + self.width)
        corners["start"] = start_point
        corners["end"] = end_point
        return corners

