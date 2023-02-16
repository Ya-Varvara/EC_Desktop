from PyQt5.QtWidgets import QWidget, QTableWidgetItem

from ui.base_ui.SimpleModelWidget import Ui_Form

class SimpleModelWidget(QWidget):
    def __init__(self, model):
        super(SimpleModelWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.model = model
        self.draw_model()

    def draw_model(self):
        self.ui.modelTableWidget.setRowCount(len(self.model.Ro))
        for row in range(self.ui.modelTableWidget.rowCount()-1):
            self.ui.modelTableWidget.setItem(row, 0, QTableWidgetItem(str(self.model.Ro[row])))
            self.ui.modelTableWidget.setItem(row, 1, QTableWidgetItem(str(self.model.H[row])))
        self.ui.modelTableWidget.setItem(len(self.model.Ro)-1, 0, QTableWidgetItem(str(self.model.Ro[-1])))

        if self.model.mtd_data is None:
            return
        if isinstance(self.model.mtd_data, tuple):
            self.ui.NT_lineEdit.setText(str(self.model.mtd_data[0]))
            self.ui.T_lineEdit.setText(str(self.model.mtd_data[1]))
            self.ui.Q_lineEdit.setText(str(self.model.mtd_data[2]))
        else:
            self.ui.NT_lineEdit.setText(str(len(self.model.mtd_data)))
            self.ui.T_lineEdit.setText(str(self.model.mtd_data[0]))
            self.ui.Q_lineEdit.setDisabled(True)
            self.ui.freq_edit.setPlainText('\n'.join([str(x) for x in self.model.mtd_data]))

    def add_mtd_data(self):
        if isinstance(self.model.mtd_data, tuple):
            self.ui.NT_lineEdit.setText(str(self.model.mtd_data[0]))
            self.ui.T_lineEdit.setText(str(self.model.mtd_data[1]))
            self.ui.Q_lineEdit.setText(str(self.model.mtd_data[2]))
        else:
            self.ui.NT_lineEdit.setText(str(len(self.model.mtd_data)))
            self.ui.T_lineEdit.setText(str(self.model.mtd_data[0]))
            self.ui.Q_lineEdit.setDisabled(True)
            self.ui.freq_edit.setPlainText('\n'.join([str(x) for x in self.model.mtd_data]))
