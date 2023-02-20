import os

from PyQt5.QtWidgets import QWidget, QMenu, QAction, QTreeWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

from ui.base_ui.TreeWidget import Ui_Form

from classes.Model import SimpleModel


class TreeWidget(QWidget):
    def __init__(self, parent=None):
        super(TreeWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.parent = parent

        self.popMenu = QMenu()
        self.init_popMenu()

        self.tree = {}

        self.tree_top_items = {'model': QTreeWidgetItem(['Модель']),
                               'calc_graph': QTreeWidgetItem(['Расчитанные кривые']),
                               'monitor_data': QTreeWidgetItem(['Данные наблюдения'])}
        self.ui.projectTreeWidget.setHeaderLabel('Дерево проекта')
        self.ui.projectTreeWidget.addTopLevelItem(self.tree_top_items['model'])
        # self.ui.projectTreeWidget.addTopLevelItem(self.tree_top_items['calc_graph'])
        # self.ui.projectTreeWidget.addTopLevelItem(self.tree_top_items['monitor_data'])
        self.ui.projectTreeWidget.itemClicked.connect(self.tree_item_clicked)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_popMenu)
    # end def __init__

    def init_popMenu(self):
        deleteAction = QAction('Удалить', self)
        deleteAction.triggered.connect(self.delete_model)
        self.popMenu.addAction(deleteAction)

        # deletePointAction = QAction('Удалить точку', self)
        # deletePointAction.triggered.connect(self.delete_point)
        # self.popMenu.addAction(deletePointAction)
    # end def init_popMenu

    def show_popMenu(self):
        item = self.ui.projectTreeWidget.currentItem()
        if item in self.tree_top_items.values():
            return
        cursor = QCursor()
        self.popMenu.popup(cursor.pos())

    def tree_item_clicked(self):
        item = self.ui.projectTreeWidget.currentItem()
        print(item.text(0))
        name = item.text(0)
        if item.parent() in self.tree_top_items.values():
            if 'Модель' in name:
                self.parent.current_model_id = int(name.split(' ')[1]) - 1
            else:
                for i in range(len(self.parent.models)):
                    if self.parent.models[i].file_path is not None and name == os.path.basename(self.parent.models[i].file_path):
                        self.parent.current_model_id = i
            self.parent.set_model_widget(self.parent.current_model_id)
            if isinstance(self.parent.models[self.parent.current_model_id], SimpleModel) and self.parent.models[self.parent.current_model_id].mtd_graph:
                self.parent.set_graph_widget(self.parent.models[self.parent.current_model_id])
        elif item not in self.tree_top_items.values():
            model = item.parent()
            for i in range(len(self.parent.models)):
                if self.parent.models[i].file_path is not None and model.text(0) == os.path.basename(self.parent.models[i].file_path):
                    self.parent.current_model_id = i
            coor = name.split(' ')[1][1:-1].split(',')
            point = self.parent.models[self.parent.current_model_id].find_point(int(coor[0]), int(coor[1]))
            self.parent.set_model_widget(self.parent.current_model_id)
            self.parent.set_graph_widget(point)

    # end def tree_item_clicked

    def add_model(self, model):
        if model.file_path is None:
            child = QTreeWidgetItem([f'Модель {self.parent.current_model_id + 1}'])
        else:
            child = QTreeWidgetItem([os.path.basename(model.file_path)])
        self.tree[model] = child
        self.tree_top_items['model'].addChild(child)
    # end def add_model

    def add_point(self, point):
        child = QTreeWidgetItem([f'Точка ({point.x},{point.y})'])
        self.tree_top_items['model'].child(self.parent.current_model_id).addChild(child)
    # end def add_point

    def delete_model(self):
        item = self.ui.projectTreeWidget.currentItem()
        name = item.text(0)
        if item.parent() in self.tree_top_items.values():
            if 'Модель' in name:
                self.parent.delete_model(int(name.split(' ')[1]) - 1)
                self.tree_top_items['model'].removeChild(self.ui.projectTreeWidget.currentItem())
            else:
                for i in range(len(self.parent.models)):
                    if self.parent.models[i].file_path is not None and name == os.path.basename(self.parent.models[i].file_path):
                        self.parent.current_model_id = i
                self.parent.delete_model(self.parent.current_model_id)
                self.tree_top_items['model'].removeChild(self.ui.projectTreeWidget.currentItem())
        elif item not in self.tree_top_items.values():
            model = item.parent()
            for i in range(len(self.parent.models)):
                if self.parent.models[i].file_path is not None and model.text(0) == os.path.basename(self.parent.models[i].file_path):
                    self.parent.current_model_id = i
            self.parent.delete_point(name, self.parent.models[self.parent.current_model_id])
            model.removeChild(self.ui.projectTreeWidget.currentItem())
    # end def delete_model

    def delete_point(self):
        pass
    # end def delete_point

