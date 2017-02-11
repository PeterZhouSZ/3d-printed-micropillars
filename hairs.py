# REMOVED Dependencies: pillow
# from PIL import Image
# Actual dependencies
import png
import math
import time
import os
import numpy
import time

class Cilium:
    # Apologies if this is ugly, I'm not familiar with Python classes
    def __init__(self, width, height, angle=0, slant=0,
            position=(0,0), start=(0,0)):
            # angle is radians from east direction
            # slant is run/rise
            # start is the beginning of the staircase
        self.width = width
        self.height = height
        self.angle = angle
        self.slant = slant
        # TODO add profile
        self.pixelArray = [[255 for x in range(width)] for y in range(width)] # 255 for white
        self.number_of_pixels = width * width # Actually a float where
                                              # ceil(number_of_pixels) is
                                              # the real number of pixels
        self.position = position
        self.offset = [0, 0]
        self.x = start[0]
        self.y = start[1]
        self.dx = 1
        self.dy = 0

    def get_new_layer(self):
        old_number_of_pixels = self.number_of_pixels
        self.number_of_pixels = (self.number_of_pixels
                - self.width * self.width / self.height)
        # print("old: ", old_number_of_pixels, " new: ", self.number_of_pixels)
        for i in range(
                math.ceil(old_number_of_pixels) - math.ceil(self.number_of_pixels)
        ):
            self.pixelArray[self.y][self.x] = 0 # 0 for false
            if (self.number_of_pixels) <= 0:
                break
            new_x, new_y = self.x + self.dx, self.y + self.dy
            if (0 <= new_x < self.width and 0 <= new_y < self.width
                    and self.pixelArray[new_y][new_x] == 255): # 255 for white
                self.x, self.y = new_x, new_y
            else:
                self.dx, self.dy = -1 * self.dy, self.dx
                self.x, self.y = self.x + self.dx, self.y + self.dy
        self.offset[0] += math.cos(self.angle) * self.slant
        self.offset[1] += math.sin(self.angle) * self.slant
        return self.pixelArray, self.position, (int(self.offset[0]), int(self.offset[1]))

def print_array(array):
    for y in range(len(array)):
        for x in range(len(array[y])):
            print('\u2588 ', end='') if array[y][x] else print('. ', end='')
        print()
    print()

def print_same_direction(width, height, angle, slant, gap, quantity_top,
        quantity_left, buffer=0, animate=False, save_image=False):
    buffer += int(height * slant)
    print(buffer)
    hairs = [[Cilium(
            width, height, angle, slant,
            position=((width + gap) * x, (width + gap) * y)
        ) for x in range(quantity_top)]
        for y in range(quantity_left)
    ]
    if save_image:
        folder_path = "ImagesFromEpoch" + str(int(time.time()))
        os.makedirs(folder_path)
    # for x in range(height):
    #     for row in hairs:
    #         for hair in row:
    #             layer, lol1, lol2 = hair.get_new_layer()
    #             print_array(layer)
    for i in range(height): # TODO CHANGE 1 TO HEIGHT # For every layer
        picture_array = [[0 for x in range((width + gap) * quantity_top + 2 * buffer)] # 0 for black
            for y in range((width + gap) * quantity_left + 2 * buffer)
        ]
        # would be MUCH improved with matrix operations
        for row in hairs:
            for hair in row:
                # print ("hair position: ", hair.position)
                hair_array, position, offset = hair.get_new_layer()
                for y in range(len(hair_array)):
                    # print_array(picture_array)
                    # print("buffer: ", buffer, " offset: ", offset, " position: ", position)
                    big_row = int(buffer + offset[1] + position[1] + y)
                    start = int(buffer + offset[0] + position[0])
                    end = int(start + len(hair_array[y]))
                    picture_array[big_row] \
                        = (picture_array[big_row][:start]
                        + hair_array[y]
                        + picture_array[big_row][end:])
        if save_image:
            img = png.fromarray(picture_array, mode='L')
            img.save(folder_path + '/' + str(i) +'.png')
        if animate:
            print_array(picture_array)
            time.sleep(.25)
            os.system('cls')

if __name__ == "__main__":
    print_same_direction(
        width=3, height=32, angle=0, slant=.13, gap=1,
        quantity_top=2, quantity_left=2, buffer=0,
        animate=True, save_image=False)