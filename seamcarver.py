#!/usr/bin/env python3

from picture import Picture
from math import sqrt

class SeamCarver(Picture):
    def energy(self, i: int, j: int) -> float:
        w = self.width()  - 1
        h = self.height() - 1

        if (  i < 0 or 
              j < 0 or 
              i > w or
              j > h    ):
            raise IndexError

        left_i  = (i - 1) if (i != 0) else (w)
        right_i = (i + 1) if (i != w) else (0)
        top_j   = (j - 1) if (j != 0) else (h)
        bot_j   = (j + 1) if (j != h) else (0)

        r_x = abs(self[left_i, j][0] - self[right_i, j][0])
        g_x = abs(self[left_i, j][1] - self[right_i, j][1])
        b_x = abs(self[left_i, j][2] - self[right_i, j][2])
        r_y = abs(self[i, top_j][0] - self[i, bot_j][0])
        g_y = abs(self[i, top_j][1] - self[i, bot_j][1])
        b_y = abs(self[i, top_j][2] - self[i, bot_j][2])

        delta_x = r_x**2 + g_x**2 + b_x**2
        delta_y = r_y**2 + g_y**2 + b_y**2

        e = sqrt(delta_x + delta_y)
        
        return e

    ## TO-DO: fill in the methods below
    def find_vertical_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        vertical seam

        Milestone 2 (pytest -m m2)
        '''
        raise NotImplementedError

    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam

        Milestone 3 (pytest -m m3)
        '''
        raise NotImplementedError

    def remove_vertical_seam(self, seam: list[int]):
        '''
        Remove a vertical seam from the picture

        Milestone 4 (pytest -m m4)
        '''
        raise NotImplementedError

    def remove_horizontal_seam(self, seam: list[int]):
        '''
        Remove a horizontal seam from the picture

        Milestone 5 (pytest -m m5)
        '''
        raise NotImplementedError

class SeamError(Exception):
    pass
