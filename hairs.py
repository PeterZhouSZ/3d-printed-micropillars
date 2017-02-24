# REMOVED Dependencies: pillow
# from PIL import Image
# Actual dependencies
import png
import math
import time
import os
import numpy
import time
from stl import mesh
import cProfile
import numpy as np


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
        self.pixelArray = [[True for x in range(width)] for y in range(width)]
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
            self.pixelArray[self.y][self.x] = False
            if (self.number_of_pixels) <= 0:
                break
            new_x, new_y = self.x + self.dx, self.y + self.dy
            if (0 <= new_x < self.width and 0 <= new_y < self.width
                    and self.pixelArray[new_y][new_x] == True):
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
        quantity_left, buffer=0, base_height=3,
        animate=False, save_image=False, save_3d_model=False,
        xy_res=.05, z_res=.05):
    buffer += int(height * slant)
    # print(buffer)
    hairs = [[Cilium(
            width, height, angle, slant,
            position=((width + gap) * x, (width + gap) * y)
        ) for x in range(quantity_top)]
        for y in range(quantity_left)
    ]
    layers = []
    if save_image:
        folder_path = "ImagesFromEpoch" + str(int(time.time()))
        os.makedirs(folder_path)
    for i in range(base_height):
        layers.append([[True for x in range((width + gap) * quantity_top + 2 * buffer)]
            for y in range((width + gap) * quantity_left + 2 * buffer)
        ])
    for i in range(height): # For every layer
        picture_array = [[False for x in range((width + gap) * quantity_top + 2 * buffer)]
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
            new_picture = picture_array[:]
            # for y in range(len(new_picture)):
            #     for x in range(len(new_picture[y])):
            #         (new_picture[y][x] = 255) if new_picture[y][x] else (new_picture[y][x] = 0)
            # img = png.fromarray(picture_array, mode='L')
            # img.save(folder_path + '/' + str(i) +'.png')
        if animate:
            print_array(picture_array)
            time.sleep(.25)
            os.system('cls')
        if save_3d_model:
            layers.append(picture_array)
    if save_3d_model:
        fastSTL(layers, xy_res, z_res)

def fastSTL(layers, xy_res, z_res):
    voxels = 0
    i = 0
    for z in range(len(layers)):
        for y in range(len(layers[z])):
            for x in range(len(layers[z][y])):
                if layers[z][y][x]:
                    voxels += 1
    data = numpy.zeros(voxels * 12, dtype=mesh.Mesh.dtype)
    for z in range(len(layers)):
        for y in range(len(layers[z])):
            for x in range(len(layers[z][y])):
                if layers[z][y][x]:
                    if y == 0 or not layers[z][y-1][x]:
                        data['vectors'][i + 0] = numpy.array(
                            [
                                [x * xy_res + 0, y * xy_res + 0, 0 + z * z_res],
                                [x * xy_res + xy_res, y * xy_res + 0, 0 + z * z_res],
                                [x * xy_res + xy_res, y * xy_res + 0, z_res + z * z_res]
                            ])
                        data['vectors'][i + 1] = numpy.array(
                            [
                                [x * xy_res + 0, y * xy_res + 0, 0 + z * z_res],
                                [x * xy_res + xy_res, y * xy_res + 0, z_res + z * z_res],
                                [x * xy_res + 0, y * xy_res + 0, z_res + z * z_res]
                            ])
                    # Down
                    if z == 0 or not layers[z-1][y][x]:
                        data['vectors'][i + 2] = numpy.array(
                            [
                                [x * xy_res + 0, y * xy_res + xy_res, 0 + z * z_res],
                                [x * xy_res + xy_res, y * xy_res + xy_res, 0 + z * z_res],
                                [x * xy_res + xy_res, y * xy_res + 0, 0 + z * z_res]
                            ])
                        data['vectors'][i + 3] = numpy.array(
                            [
                                [x * xy_res + 0, y * xy_res + xy_res, 0 + z * z_res],
                                [x * xy_res + xy_res, y * xy_res + 0, 0 + z * z_res],
                                [x * xy_res + 0, y * xy_res + 0, 0 + z * z_res]
                            ])
                    # East
                    if x == len(layers[z][y]) - 1 or not layers[z][y][x+1]:
                        data['vectors'][i + 4] = numpy.array(
                            [
                                [x * xy_res + xy_res, y * xy_res + xy_res, 0 + z * z_res],
                                [x * xy_res + xy_res, y * xy_res + xy_res, z_res + z * z_res],
                                [x * xy_res + xy_res, y * xy_res + 0, z_res + z * z_res]
                            ])
                        data['vectors'][i + 5] = numpy.array(
                            [
                                [x * xy_res + xy_res, y * xy_res + xy_res, 0 + z * z_res],
                                [x * xy_res + xy_res, y * xy_res + 0, z_res + z * z_res],
                                [x * xy_res + xy_res, y * xy_res + 0, 0 + z * z_res]
                            ])
                    # Up
                    if z == len(layers) - 1 or not layers[z+1][y][x]:
                        data['vectors'][i + 6] = numpy.array(
                            [
                                [x * xy_res + xy_res, y * xy_res + xy_res, z_res + z * z_res],
                                [x * xy_res + 0, y * xy_res + xy_res, z_res + z * z_res],
                                [x * xy_res + 0, y * xy_res + 0, z_res + z * z_res]
                            ])
                        data['vectors'][i + 7] = numpy.array(
                            [
                                [x * xy_res + xy_res, y * xy_res + xy_res, z_res + z * z_res],
                                [x * xy_res + 0, y * xy_res + 0, z_res + z * z_res],
                                [x * xy_res + xy_res, y * xy_res + 0, z_res + z * z_res]
                            ])
                    # West
                    if x == 0 or not layers[z][y][x-1]:
                        data['vectors'][i + 8] = numpy.array(
                            [
                                [x * xy_res + 0, y * xy_res + xy_res, z_res + z * z_res],
                                [x * xy_res + 0, y * xy_res + xy_res, 0 + z * z_res],
                                [x * xy_res + 0, y * xy_res + 0, 0 + z * z_res]
                            ])
                        data['vectors'][i + 9] = numpy.array(
                            [
                                [x * xy_res + 0, y * xy_res + xy_res, z_res + z * z_res],
                                [x * xy_res + 0, y * xy_res + 0, 0 + z * z_res],
                                [x * xy_res + 0, y * xy_res + 0, z_res + z * z_res]
                            ])
                    # North
                    if y == len(layers[z]) - 1 or not layers[z][y+1][x]:
                        data['vectors'][i + 10] = numpy.array(
                            [
                                [x * xy_res + 0, y * xy_res + xy_res, 0 + z * z_res],
                                [x * xy_res + 0, y * xy_res + xy_res, z_res + z * z_res],
                                [x * xy_res + xy_res, y * xy_res + xy_res, z_res + z * z_res]
                            ])
                        data['vectors'][i + 11] = numpy.array(
                            [
                                [x * xy_res + 0, y * xy_res + xy_res, 0 + z * z_res],
                                [x * xy_res + xy_res, y * xy_res + xy_res, z_res + z * z_res],
                                [x * xy_res + xy_res, y * xy_res + xy_res, 0 + z * z_res]
                            ])
                    i += 12
    big_mesh = mesh.Mesh(data)
    big_mesh.save('hairs' + str(int(time.time())) + '.stl')
if __name__ == "__main__":
    print_same_direction(
        width=10, height=256, angle=0, slant=.03, gap=10,
        quantity_top=5, quantity_left=5, buffer=0,
        animate=False, save_image=False, save_3d_model=True)
# def slowSTL(layers):
#     structure = Solid(name='structure')
#     for z in range(len(layers)):
#         for y in range(len(layers[z])):
#             for x in range(len(layers[z][y])):
#                 if layers[z][y][x]:
#                     # South
#                     if y == 0 or not layers[z][y-1][x]:
#                         structure.add_facet(Vector3d(0, -1, 0),
#                             [
#                                 Vector3d(x * xy_res + 0, y * xy_res + 0, 0 + z * z_res),
#                                 Vector3d(x * xy_res + xy_res, y * xy_res + 0, 0 + z * z_res),
#                                 Vector3d(x * xy_res + xy_res, y * xy_res + 0, z_res + z * z_res)
#                             ])
#                         structure.add_facet(Vector3d(0, -1, 0),
#                             [
#                                 Vector3d(x * xy_res + 0, y * xy_res + 0, 0 + z * z_res),
#                                 Vector3d(x * xy_res + xy_res, y * xy_res + 0, z_res + z * z_res),
#                                 Vector3d(x * xy_res + 0, y * xy_res + 0, z_res + z * z_res)
#                             ])
#                     # Down
#                     if z == 0 or not layers[z-1][y][x]:
#                         structure.add_facet(Vector3d(0, 0, -1),
#                             [
#                                 Vector3d(x * xy_res + 0, y * xy_res + xy_res, 0 + z * z_res),
#                                 Vector3d(x * xy_res + xy_res, y * xy_res + xy_res, 0 + z * z_res),
#                                 Vector3d(x * xy_res + xy_res, y * xy_res + 0, 0 + z * z_res)
#                             ])
#                         structure.add_facet(Vector3d(0, 0, -1),
#                             [
#                                 Vector3d(x * xy_res + 0, y * xy_res + xy_res, 0 + z * z_res),
#                                 Vector3d(x * xy_res + xy_res, y * xy_res + 0, 0 + z * z_res),
#                                 Vector3d(x * xy_res + 0, y * xy_res + 0, 0 + z * z_res)
#                             ])
#                     # East
#                     if x == len(layers[z][y]) - 1 or not layers[z][y][x+1]:
#                         structure.add_facet(Vector3d(1, 0, 0),
#                             [
#                                 Vector3d(x * xy_res + xy_res, y * xy_res + xy_res, 0 + z * z_res),
#                                 Vector3d(x * xy_res + xy_res, y * xy_res + xy_res, z_res + z * z_res),
#                                 Vector3d(x * xy_res + xy_res, y * xy_res + 0, z_res + z * z_res)
#                             ])
#                         structure.add_facet(Vector3d(1, 0, 0),
#                             [
#                                 Vector3d(x * xy_res + xy_res, y * xy_res + xy_res, 0 + z * z_res),
#                                 Vector3d(x * xy_res + xy_res, y * xy_res + 0, z_res + z * z_res),
#                                 Vector3d(x * xy_res + xy_res, y * xy_res + 0, 0 + z * z_res)
#                             ])
#                     # Up
#                     if z == len(layers) - 1 or not layers[z+1][y][x]:
#                         structure.add_facet(Vector3d(0, 0, 1),
#                             [
#                                 Vector3d(x * xy_res + xy_res, y * xy_res + xy_res, z_res + z * z_res),
#                                 Vector3d(x * xy_res + 0, y * xy_res + xy_res, z_res + z * z_res),
#                                 Vector3d(x * xy_res + 0, y * xy_res + 0, z_res + z * z_res)
#                             ])
#                         structure.add_facet(Vector3d(0, 0, 1),
#                             [
#                                 Vector3d(x * xy_res + xy_res, y * xy_res + xy_res, z_res + z * z_res),
#                                 Vector3d(x * xy_res + 0, y * xy_res + 0, z_res + z * z_res),
#                                 Vector3d(x * xy_res + xy_res, y * xy_res + 0, z_res + z * z_res)
#                             ])
#                     # West
#                     if x == 0 or not layers[z][y][x-1]:
#                         structure.add_facet(Vector3d(-1, 0, 0),
#                             [
#                                 Vector3d(x * xy_res + 0, y * xy_res + xy_res, z_res + z * z_res),
#                                 Vector3d(x * xy_res + 0, y * xy_res + xy_res, 0 + z * z_res),
#                                 Vector3d(x * xy_res + 0, y * xy_res + 0, 0 + z * z_res)
#                             ])
#                         structure.add_facet(Vector3d(-1, 0, 0),
#                             [
#                                 Vector3d(x * xy_res + 0, y * xy_res + xy_res, z_res + z * z_res),
#                                 Vector3d(x * xy_res + 0, y * xy_res + 0, 0 + z * z_res),
#                                 Vector3d(x * xy_res + 0, y * xy_res + 0, z_res + z * z_res)
#                             ])
#                     # North
#                     if y == len(layers) - 1 or not layers[z][y+1][x]:
#                         structure.add_facet(Vector3d(0, 1, 0),
#                             [
#                                 Vector3d(x * xy_res + 0, y * xy_res + xy_res, 0 + z * z_res),
#                                 Vector3d(x * xy_res + 0, y * xy_res + xy_res, z_res + z * z_res),
#                                 Vector3d(x * xy_res + xy_res, y * xy_res + xy_res, z_res + z * z_res)
#                             ])
#                         structure.add_facet(Vector3d(0, 1, 0),
#                             [
#                                 Vector3d(x * xy_res + 0, y * xy_res + xy_res, 0 + z * z_res),
#                                 Vector3d(x * xy_res + xy_res, y * xy_res + xy_res, z_res + z * z_res),
#                                 Vector3d(x * xy_res + xy_res, y * xy_res + xy_res, 0 + z * z_res)
#                             ])
#     with open('hair' + str(width) + str(height) + str(angle) + str(slant)
#             + str(gap) + str(quantity_top) + str(quantity_left)
#             + '.stl', 'wb') as f:
#         structure.write_binary(f)
