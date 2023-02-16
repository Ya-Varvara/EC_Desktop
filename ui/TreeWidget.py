from PyQt5.QtWidgets import QWidget, QMenu, QAction, QTreeWidgetItem

from ui.base_ui.TreeWidget import Ui_Form


class TreeWidget(QWidget):
    def __init__(self):
        super(TreeWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.popMenu = QMenu()
        self.init_popMenu()

        self.tree_top_items = {'model': QTreeWidgetItem(['Модель']),
                               'calc_graph': QTreeWidgetItem(['Расчитанные кривые']),
                               'monitor_data': QTreeWidgetItem(['Данные наблюдения'])}
        self.ui.projectTreeWidget.setHeaderLabel('Дерево проекта')
        self.ui.projectTreeWidget.addTopLevelItem(self.tree_top_items['model'])
        self.ui.projectTreeWidget.addTopLevelItem(self.tree_top_items['calc_graph'])
        self.ui.projectTreeWidget.addTopLevelItem(self.tree_top_items['monitor_data'])
    # end def __init__

    def init_popMenu(self):
        deleteAction = QAction('Удалить', self)
        # addPointAction.triggered.connect(self.add_point)
        self.popMenu.addAction(deleteAction)

        # deletePointAction = QAction('Удалить точку', self)
        # deletePointAction.triggered.connect(self.delete_point)
        # self.popMenu.addAction(deletePointAction)
    # end def init_popMenu

    def add_model(self):
        pass
    # end def add_model

    def add_point(self):
        pass
    # end def add_point

    def delete_model(self):
        pass
    # end def delete_model

    def delete_point(self):
        pass
    # end def delete_point

