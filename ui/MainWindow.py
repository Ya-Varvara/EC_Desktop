from PyQt5.QtWidgets import QMainWindow, QFileDialog, QAction

from PyQt5.QtGui import QIcon

from classes.Model import GridModel, SimpleModel

from ui.base_ui.MainWindow import Ui_MainWindow

from ui.mtdInputDialog import mtdInputDialog
from ui.SimpleModelDialog import SimpleModelDialog
from ui.TreeWidget import TreeWidget

from handlers.supportDialogs import open_file, save_file
from handlers.importFileHandler import import_model

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowIcon(QIcon('zeva.ico'))

        self.tree = TreeWidget(self)

        self.initUI()

        self.models = []
        self.model_widgets = []
        self.graphics_widgets = []
        self.current_model_id = -1
        self.current_graphic_id = -1

    # end def __init__

    def initUI(self):
        self.ui.openModelAction.triggered.connect(self.open_model)
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

        self.ui.projectTreeDockWidget.setWidget(self.tree)
        # self.ui.projectTreeWidget.itemClicked.connect(self.tree_item_clicked)
    # end def init_ui

    def delete_model(self, model_id):
        model = self.models[model_id]
        if isinstance(model, GridModel):
            points = model.get_points()
            for point in points:
                if point.methods:
                    for method in point.methods.values():
                        self.ui.graphicsStackedWidget.removeWidget(method.graph)
            self.ui.sectionStackedWidget.removeWidget(model.widget)
        elif isinstance(model, SimpleModel):
            if model.methods:
                for method in model.methods.values():
                    self.ui.graphicsStackedWidget.removeWidget(method.graph)
            self.ui.sectionStackedWidget.removeWidget(model.widget)
        self.current_model_id -= 1
        self.models.pop(model_id)

    def delete_point(self, point_name, model):
        xy = point_name.split(' ')[1][1:-1].split(',')
        point = model.find_point(int(xy[0]), int(xy[1]))
        point.is_alive = False
        for method in point.methods.values():
            self.ui.graphicsStackedWidget.removeWidget(method.graph)

    def check_freq_data(self, model):
        if model.freq_data is not None:
            return True
        dialog = mtdInputDialog()
        dialog.show()
        if dialog.exec_():
            model.freq_data = dialog.data
            return True
        return False
    # end def get_mtd_data

    def calculate_mt1d(self):
        def add_widget(widget):
            self.ui.graphicsStackedWidget.addWidget(widget)
            self.ui.graphicsStackedWidget.setCurrentWidget(widget)
            self.show()

        if len(self.models) == 0:
            self.ui.statusbar.showMessage('Нет модели для расчета', 2000)
            self.open_model()
            return

        self.ui.statusbar.showMessage('Расчет MT1D', 1000)

        model = self.models[self.current_model_id]

        if isinstance(model, SimpleModel) and self.check_freq_data(model):
            model.calculate_mt1d()
            add_widget(model.methods['mt1d'].graph)
        else:
            points = model.get_points()
            if points is None:
                self.ui.statusbar.showMessage('Нет точек для расчета', 2000)
                return
            if self.check_freq_data(model):
                for point in points:
                    if 'mt1d' not in point.methods.keys():
                        point.calculate_mt1d()
                        self.tree.add_point(point)
                        add_widget(point.methods['mt1d'].graph)
                return
    # end def calculate_mt1d

    def calculate_tdem(self):
        self.ui.statusbar.showMessage('Расчет TDEM1D', 1000)
    # end def calculate_tdem

    # def tree_item_clicked(self):
    #     item = self.ui.projectTreeWidget.currentItem()
    #     print(item.text(0))
    #     name = item.text(0)
    #     if item.parent() in self.tree_top_items.values():
    #         if 'Модель' in name:
    #             self.current_model_id = int(name.split(' ')[1]) - 1
    #         else:
    #             for i in range(len(self.models)):
    #                 if self.models[i].file_path is not None and name == os.path.basename(self.models[i].file_path):
    #                     self.current_model_id = i
    #         self.set_model_widget(self.current_model_id)
    #         if isinstance(self.models[self.current_model_id], SimpleModel) and self.models[self.current_model_id].mtd_graph:
    #             self.set_graph_widget(self.models[self.current_model_id])
    #     elif item not in self.tree_top_items.values():
    #         model = item.parent()
    #         for i in range(len(self.models)):
    #             if self.models[i].file_path is not None and model.text(0) == os.path.basename(self.models[i].file_path):
    #                 self.current_model_id = i
    #         coor = name.split(' ')[1][1:-1].split(',')
    #         point = self.models[self.current_model_id].find_point(int(coor[0]), int(coor[1]))
    #         self.set_model_widget(self.current_model_id)
    #         self.set_graph_widget(point)
    # end def tree_item_clicked

    def open_period_file(self):
        dialog = mtdInputDialog()
        dialog.show()
        if dialog.exec_():
            self.models[self.current_model_id].freq_data = dialog.data
    # end def open_period_file

    def open_model(self):
        file_path = open_file()

        if not file_path:
            print("Error")
            return

        data = import_model(file_path)

        if data[0] == 'dsaa':
            model = GridModel(file_path, data)
        elif data[0] == 'one row':
            model = SimpleModel(file_path, data[1], data[2])
        elif data[0] == 'one row with freq':
            model = SimpleModel(file_path, data[1], data[2], data[3])
        else:
            model = None
            print('[ERROR] Unknown type of file')

        if model:
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
        model.widget.parent = self

        self.ui.sectionStackedWidget.addWidget(model.widget)
        self.ui.sectionStackedWidget.setCurrentWidget(model.widget)
        self.show()

        self.tree.add_model(self.models[self.current_model_id])

    def set_graph_widget(self, model):
        key = next(iter(model.methods))
        self.ui.graphicsStackedWidget.setCurrentWidget(model.methods[key].graph)
    # end def set_graph_widget

    def set_model_widget(self, model):
        self.ui.sectionStackedWidget.setCurrentWidget(model.widget)
        if isinstance(model, SimpleModel):
            if model.methods:
                key = next(iter(model.methods))
                self.ui.graphicsStackedWidget.setCurrentWidget(model.methods[key].graph)
            else:
                self.ui.graphicsStackedWidget.setCurrentWidget(self.ui.sectionStackedWidgetPage1)

    # end def set_model_widget

    def create_model_data(self):
        pass
    # end def open_model_data_file

    def save_graphics(self):
        file_path = save_file()

        if not file_path:
            print("Error")
            return

        if len(self.models) == 0:
            return

        model = self.models[self.current_model_id]

        if isinstance(model, SimpleModel):
            model_result = model.save_methods_result()
            if model_result:
                with open(file_path, 'w') as file:
                    file.write(model_result)

        elif isinstance(model, GridModel):
            model_result = []
            points = model.get_points()
            for i in range(len(points)):
                model_result.append(f'\nPoint {i + 1}\n')
                model_result.append(points[i].save_methods_result())
            with open(file_path, 'w') as file:
                file.write('\n'.join(model_result))
    # end def save_graphics
# end class MainWindow
