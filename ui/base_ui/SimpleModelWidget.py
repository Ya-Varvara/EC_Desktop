# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\base_ui\SimpleModelWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(586, 202)
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.modelTableWidget = QtWidgets.QTableWidget(self.groupBox)
        self.modelTableWidget.setAlternatingRowColors(False)
        self.modelTableWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.modelTableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.modelTableWidget.setRowCount(8)
        self.modelTableWidget.setObjectName("modelTableWidget")
        self.modelTableWidget.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.modelTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.modelTableWidget.setHorizontalHeaderItem(1, item)
        self.modelTableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.modelTableWidget.horizontalHeader().setHighlightSections(True)
        self.modelTableWidget.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.modelTableWidget, 0, 1, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.NT_label = QtWidgets.QLabel(self.groupBox_2)
        self.NT_label.setObjectName("NT_label")
        self.gridLayout_2.addWidget(self.NT_label, 0, 0, 1, 1)
        self.T_label = QtWidgets.QLabel(self.groupBox_2)
        self.T_label.setObjectName("T_label")
        self.gridLayout_2.addWidget(self.T_label, 1, 0, 1, 1)
        self.T_lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.T_lineEdit.setObjectName("T_lineEdit")
        self.gridLayout_2.addWidget(self.T_lineEdit, 1, 1, 1, 1)
        self.NT_lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.NT_lineEdit.setObjectName("NT_lineEdit")
        self.gridLayout_2.addWidget(self.NT_lineEdit, 0, 1, 1, 1)
        self.Q_label = QtWidgets.QLabel(self.groupBox_2)
        self.Q_label.setObjectName("Q_label")
        self.gridLayout_2.addWidget(self.Q_label, 2, 0, 1, 1)
        self.Q_lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.Q_lineEdit.setObjectName("Q_lineEdit")
        self.gridLayout_2.addWidget(self.Q_lineEdit, 2, 1, 1, 1)
        self.freq_edit = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.freq_edit.setObjectName("freq_edit")
        self.gridLayout_2.addWidget(self.freq_edit, 3, 1, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_2, 0, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Модель"))
        item = self.modelTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Ro"))
        item = self.modelTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "H"))
        self.groupBox_2.setTitle(_translate("Form", "Параметры частот"))
        self.NT_label.setText(_translate("Form", "NT"))
        self.T_label.setText(_translate("Form", "T"))
        self.Q_label.setText(_translate("Form", "Q"))
