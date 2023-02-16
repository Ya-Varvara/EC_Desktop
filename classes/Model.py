# import os

from handlers.importFileHandler import import_model
from handlers.mtd import MT1D


class GridModel:
    def __init__(self, file_path):
        self.file_path = file_path
        res = import_model(file_path)
        if res[0] == 'dsaa':
            self.file_type, self.x, self.y, self.Vp, self.x_min, self.x_max, self.y_min, self.y_max, self.Vp_min, self.Vp_max, self.Nx, self.Ny = res
        self.points = None
        self.mtd_data = None
        self.tdem_data = None
    # end def __init__

    def get_points(self):
        return self.points

    def find_point(self, x, y):
        for point in self.points:
            if point.x == x and point.y == y and point.is_alive:
                return point
        return None
    # end def find_point

    def get_data_for_mt1d(self, point):
        if point.Ro is None or point.H is None:
            all_data = self.Vp[:, point.x//10-1]
            Ro_list = []
            H_list = []
            for value in all_data:
                if not Ro_list or Ro_list[-1] != value:
                    Ro_list.append(value)
                    H_list.append(1)
                else:
                    H_list[-1] += 1
            k = abs(self.y_max-self.y_min)/self.Ny
            point.Ro, point.H = Ro_list, [round(x*k) for x in H_list]
        return
    # end def get_data_for_mt1d

    def add_point(self, xy):
        point = Point(self, xy[0], xy[1])
        if self.points:
            self.points.append(point)
        else:
            self.points = [point]
    # end def add_point

    def delete_point(self, xy):
        for each in self.points:
            if each.x == xy[0] and each.y == xy[1] and each.is_alive:
                each.is_alive = False
                return
        return
    # end def add_point
# end class GridModel

class Point:
    def __init__(self, parent, x, y):
        self.parent = parent
        self.x = x
        self.y = y
        self.mtd_result = None
        self.is_alive = True
        self.Ro = None
        self.H = None
        self.mtd_graph = None
    # end def __init__

    def get_mt1d(self):
        if self.mtd_result is None:
            self.mtd_result = MT1D(self.parent.mtd_data, len(self.Ro), self.Ro, self.H)
        return self.mtd_result
    # end def get_mtd
# end class Point

class SimpleModel:
    def __init__(self, model_file_path, Ro, H, freq_data):
        self.file_path = model_file_path
        self.Ro = Ro
        self.H = H
        self.mtd_data = freq_data
        self.mtd_result = None
        self.mtd_graph = None

    def get_mt1d(self):
        if self.mtd_result is None:
            self.mtd_result = MT1D(self.mtd_data, len(self.Ro), self.Ro, self.H)
        return self.mtd_result




