#!/usr/bin/env python3

from PIL import Image
from picture import Picture
from math import sqrt

class SeamCarver(Picture):
    def _clamp_to_width(self, i: int) -> int:
        if i < 0:
            return 0
        elif i >= self.width():
            return self.width() - 1
        return i

    def _clamp_to_height(self, j: int) -> int:
        if j < 0:
            return 0
        elif j >= self.height():
            return self.height() - 1
        return j

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

    def find_vertical_seam(self) -> list[int]:
        ## This dictionary contains all of the minimum energy seams as described by the recurrence
        ## M[i,j] = e(i,j) + min(M[i-1, j-1], M[i, j-1], M[i+1, j-1])
        M = dict()

        ## sets up the table with infinities for 'unexplored' values
        ## NOTE: maybe we're able to skip this somehow...
        for i in range(self.width()):
            for j in range(self.height()):
                M[i, j] = float('inf')

        last_row_min = float('inf')
        min_col = 0

        ## bottom-up DP
        for j in range(self.height()):
            for i in range(self.width()):
                if j == 0:
                    M[i, j] = self.energy(i, j)
                else:
                    M[i, j] = self.energy(i, j) + \
                        min(  M[self._clamp_to_width(i-1), j-1],
                              M[i,                         j-1],
                              M[self._clamp_to_width(i+1), j-1]  )
                if j == self.height() - 1 and M[i, j] < last_row_min:
                    last_row_min = M[i, j]
                    min_col = i

        seam = [min_col]

        ## working back up
        for row in range(self.height() - 1, 0, -1):
            prev_col = seam[-1]
            ## NOTE: this can *probably* just be initialized as one of the three values
            ## and only compare the remaining two. probably.
            min_next_col = prev_col
            for next_col in [prev_col - 1, prev_col, prev_col + 1]:
                if M[self._clamp_to_width(next_col), row - 1] < M[min_next_col, row - 1]:
                    min_next_col = self._clamp_to_width(next_col)
            seam.append(min_next_col)
        
        seam.reverse()
        return seam

        

    ## TO-DO: fill in the methods below
    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam

        Milestone 3 (pytest -m m3)
        '''

        transposed_img = Image.new('RGB', (self.height(), self.width()))
        transposed_img.putdata([self[j, i] for j in range(self.width()) for i in range(self.height())])

        transposed_seam_carver = SeamCarver(transposed_img)

        return transposed_seam_carver.find_vertical_seam()

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
