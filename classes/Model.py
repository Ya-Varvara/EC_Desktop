# import os

from handlers.importFileHandler import import_model
from handlers.mtd import MT1D

from ui.ModelPlotWidget import MTDPlotWidget

# ============ Parent Classes ====================================
class Method:
    def __init__(self):
        self.result_data = None
        self.graph = None

class OneColumnModel:
    def __init__(self, Ro=None, H=None, freq=None):
        self.Ro = Ro
        self.H = H
        self.freq_data = freq
        self.methods = {}

    def calculate_mt1d(self):
        self.methods['mt1d'] = mtdMethod(self.freq_data)

# ============ Child Classes ======================================

# ======== Methods
class mtdMethod(Method):
    def __init__(self, data):
        super(mtdMethod, self).__init__()
        freq, Ro, H = data
        self.result_data = MT1D(freq, len(Ro), H)
        self.graph = MTDPlotWidget()
        self.graph.draw_mtd_graph(self.result_data)

# ======== Models
class GridModel:
    def __init__(self, file_path):
        self.file_path = file_path
        res = import_model(file_path)
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
        self.get_data_for_mt1d(point)
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

class Point(OneColumnModel):
    def __init__(self, parent, x, y):
        super(Point, self).__init__()
        self.parent = parent
        self.x = x
        self.y = y
        self.is_alive = True
    # end def __init__
# end class Point

class SimpleModel(OneColumnModel):
    def __init__(self, model_file_path, Ro, H, freq_data=None):
        super(SimpleModel, self).__init__(Ro, H, freq_data)
        self.file_path = model_file_path
    # end def __init__
# end class SimpleModel




