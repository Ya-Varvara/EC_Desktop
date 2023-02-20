import os

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QAction, QTreeWidgetItem

from PyQt5.QtGui import QIcon

from classes.Model import GridModel, SimpleModel, Point

from ui.base_ui.MainWindow import Ui_MainWindow

from ui.ModelPlotWidget import ModelPlotWidget, MTDPlotWidget
from ui.mtdInputDialog import mtdInputDialog
from ui.SimpleModelDialog import SimpleModelDialog
from ui.SimpleModelWidget import SimpleModelWidget
from ui.TreeWidget import TreeWidget


class MainWindow(QMainWindow):
    tree_top_items = {}
    models = []
    model_widgets = []
    graphics_widgets = []
    current_model_id = -1
    current_graphic_id = -1

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowIcon(QIcon('zeva.ico'))

        self.tree = TreeWidget(self)
        self.ui.projectTreeDockWidget.setWidget(self.tree)

        self.initUI()
    # end def __init__

    def initUI(self):
        self.ui.openModelAction.triggered.connect(self.open_grid_model)
        self.ui.createModelAction.triggered.connect(self.create_simple_model)
        self.ui.saveFileAction.triggered.connect(self.save_graphics)
        self.ui.loadPeriodDataAction.triggered.connect(self.open_period_file)
        self.ui.createPeriodDataAction.triggered.connect(self.open_period_file)

        computeMTDAction = QAction('Расчет MT1D', self)
        computeMTDAction.triggered.connect(self.calculate_mt1d)

        computeTDEMAction = QAction('Расчет TDEM1D', self)
        computeTDEMAction.triggered.connect(self.calculate_tdem)

        self.ui.toolBar.addAction(computeMTDAction)
        self.ui.toolBar.addAction(computeTDEMAction)

        # self.ui.projectTreeWidget.itemClicked.connect(self.tree_item_clicked)
    # end def init_ui

    def delete_model(self, model_id):
        model = self.models[model_id]
        if isinstance(model, GridModel):
            points = model.get_points()
            for point in points:
                if point.mtd_graph:
                    self.ui.graphicsStackedWidget.removeWidget(point.mtd_graph)
            self.ui.sectionStackedWidget.removeWidget(self.model_widgets[model_id])
            self.model_widgets.pop(model_id)
        elif isinstance(model, SimpleModel):
            if model.mtd_graph:
                self.ui.graphicsStackedWidget.removeWidget(model.mtd_graph)
            self.ui.sectionStackedWidget.removeWidget(self.model_widgets[model_id])
            self.model_widgets.pop(model_id)
        self.current_model_id -= 1
        self.models.pop(model_id)

    def delete_point(self, point_name, model):
        xy = point_name.split(' ')[1][1:-1].split(',')
        point = model.find_point(int(xy[0]), int(xy[1]))
        point.is_alive = False
        self.ui.graphicsStackedWidget.removeWidget(point.mtd_graph)



    def get_mtd_data(self):
        dialog = mtdInputDialog()
        dialog.show()
        if dialog.exec_():
            self.models[self.current_model_id].mtd_data = dialog.data
            return True
        return False
    # end def get_mtd_data

    def calculate_mt1d(self):
        if len(self.models) == 0:
            self.ui.statusbar.showMessage('Нет модели для расчета', 2000)
            self.open_grid_model()
            return
        self.ui.statusbar.showMessage('Расчет MT1D', 1000)
        model = self.models[self.current_model_id]

        def create_plot(model):
            model.mtd_graph = MTDPlotWidget(self)
            model.mtd_graph.draw_mtd_graph(model.get_mt1d())

            self.ui.graphicsStackedWidget.addWidget(model.mtd_graph)
            self.ui.graphicsStackedWidget.setCurrentWidget(model.mtd_graph)
            # self.current_graphic_id = len(self.graphics_widgets) - 1
            self.show()

            if isinstance(model, Point):
                self.tree.add_point(model)
        if isinstance(model, SimpleModel):
            print('Yes')
            if model.mtd_data is None:
                if self.get_mtd_data():
                    create_plot(model)
        elif isinstance(model, GridModel):
            points = model.get_points()
            if model.mtd_data is None:
                if not self.get_mtd_data():
                    return
            if points is None:
                self.ui.statusbar.showMessage('Нет точек для расчета', 2000)
                return
            for point in points:
                if point.mtd_graph is None:
                    model.get_data_for_mt1d(point)
                    create_plot(point)
    # end def calculate_mt1d

    def calculate_tdem(self):
        self.ui.statusbar.showMessage('Расчет TDEM1D', 1000)
        pass

    # end def calculate_tdem

    def tree_item_clicked(self):
        item = self.ui.projectTreeWidget.currentItem()
        print(item.text(0))
        name = item.text(0)
        if item.parent() in self.tree_top_items.values():
            if 'Модель' in name:
                self.current_model_id = int(name.split(' ')[1]) - 1
            else:
                for i in range(len(self.models)):
                    if self.models[i].file_path is not None and name == os.path.basename(self.models[i].file_path):
                        self.current_model_id = i
            self.set_model_widget(self.current_model_id)
            if isinstance(self.models[self.current_model_id], SimpleModel) and self.models[self.current_model_id].mtd_graph:
                self.set_graph_widget(self.models[self.current_model_id])
        elif item not in self.tree_top_items.values():
            model = item.parent()
            for i in range(len(self.models)):
                if self.models[i].file_path is not None and model.text(0) == os.path.basename(self.models[i].file_path):
                    self.current_model_id = i
            coor = name.split(' ')[1][1:-1].split(',')
            point = self.models[self.current_model_id].find_point(int(coor[0]), int(coor[1]))
            self.set_model_widget(self.current_model_id)
            self.set_graph_widget(point)
    # end def tree_item_clicked

    def open_period_file(self):
        # file_path = self.open_data_file()
        #
        # if not file_path:
        #     print("Error")
        #     return

        dialog = mtdInputDialog()
        dialog.show()
        if dialog.exec_():
            self.models[self.current_model_id].mtd_data = dialog.data
    # end def open_period_file

    def open_grid_model(self):
        def is_name(str):
            try:
                float(str.split()[0])
                return False
            except ValueError:
                return True

        file_path = self.open_data_file()

        if not file_path:
            print("Error")
            return

        if os.path.splitext(file_path)[1] == '.grd':
            model = GridModel(file_path)
        else:
            with open(file_path, 'r') as f:
                file_type = f.readline()
                if is_name(file_type):
                    name = f.readline()
                    data = f.read().split('\n')
                    Ro_list = []
                    H_list = []
                    for pair in data:
                        if pair:
                            rh = pair.split()
                            Ro_list.append(float(rh[0]))
                            if len(rh) > 1:
                                H_list.append(float(rh[1]))
                    model = SimpleModel(file_path, Ro_list, H_list)
                else:
                    NT, T, Q = (float(x) for x in file_type.split())  # NT, T, Q
                    N = int(f.readline().strip())
                    Ro_list = [float(i) for i in f.readline().split()]
                    H_list = [float(i) for i in f.readline().split()]
                    model = SimpleModel(file_path, Ro_list, H_list, (NT, T, Q))
        self.add_model(model)
    # end def open_model_data_file

    def create_simple_model(self):
        dialog = SimpleModelDialog()
        dialog.show()
        if dialog.exec_():
            data = dialog.data
            file_path = dialog.file_name
            model = SimpleModel(file_path, data[0], data[1], data[2])
            self.add_model(model)
    # end def create_simple_model

    def add_model(self, model):
        self.models.append(model)
        self.current_model_id = len(self.models) - 1

        if isinstance(model, GridModel):
            self.model_widgets.append(ModelPlotWidget(parent=self, width=5, height=4, dpi=100))
            self.model_widgets[self.current_model_id].draw_model(model)
            self.model_widgets[self.current_model_id].axes.set_xlabel('meters')
            self.model_widgets[self.current_model_id].axes.set_ylabel('meters')
            # self.model_widgets[self.current_model_id].fig.colorbar(mappable=ScalarMappable)
        elif isinstance(model, SimpleModel):
            self.model_widgets.append(SimpleModelWidget(self.models[self.current_model_id]))

        self.ui.sectionStackedWidget.addWidget(self.model_widgets[self.current_model_id])
        self.ui.sectionStackedWidget.setCurrentWidget(self.model_widgets[self.current_model_id])
        self.show()

        self.tree.add_model(self.models[self.current_model_id])

    def set_graph_widget(self, model):
        if model.mtd_graph:
            self.ui.graphicsStackedWidget.setCurrentWidget(model.mtd_graph)
    # end def set_graph_widget

    def set_model_widget(self, widget_id):
        self.ui.sectionStackedWidget.setCurrentWidget(self.model_widgets[widget_id])
    # end def set_model_widget

    def create_model_data(self):
        pass
    # end def open_model_data_file

    def save_graphics(self):
        file_path = self.save_data_file()

        if not file_path:
            print("Error")
            return

        if len(self.models) == 0:
            return

        model = self.models[self.current_model_id]

        if isinstance(model, SimpleModel):
            mtd_result = model.get_mt1d()
            with open(file_path, 'w') as file:
                file.write('sqrtT  RoT  Pht \n')
                data = [' '.join([str(round(mtd_result['T'][i], 4)), str(round(mtd_result['RoT'][i], 2)), str(round(mtd_result['Pht'][i], 2))]) for
                        i in range(len(mtd_result['T']))]
                file.write('\n'.join(data))
        elif isinstance(model, GridModel):
            with open(file_path, 'w') as file:
                file.write('sqrtT  RoT  Pht \n')
                points = model.get_points()
                for i in range(len(points)):
                    file.write(f'Point {i+1}\n')
                    mtd_result = points[i].mtd_result
                    data = [' '.join([str(round(mtd_result['T'][i], 4)), str(round(mtd_result['RoT'][i], 2)),
                                      str(round(mtd_result['Pht'][i], 2))]) for i in range(len(mtd_result['T']))]
                    file.write('\n'.join(data))
    # end def save_graphics

    def open_data_file(self):
        file_filter = 'Text File (*.txt);; Grid File (*.grd)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Открыть файл',
            filter=file_filter,
            initialFilter='Text File (*.txt)'
        )
        if response[0]:
            return response[0]
        else:
            return 0
    # end def open_data_file

    def save_data_file(self):
        file_filter = 'Text File (*.txt)'
        response = QFileDialog.getSaveFileName(
            parent=self,
            caption='Сохранить файл',
            filter=file_filter,
            initialFilter='Text File (*.txt)',
            directory='data_file.txt'
        )
        if response[0]:
            return response[0]
        else:
            return 0
    # end def open_data_file
# end class MainWindow
