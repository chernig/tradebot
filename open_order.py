# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'open_order.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OpenOrd(object):
    def setupUi(self, OpenOrd):
        OpenOrd.setObjectName("OpenOrd")
        OpenOrd.resize(379, 326)
        self.formLayout = QtWidgets.QFormLayout(OpenOrd)
        self.formLayout.setObjectName("formLayout")
        self.comboBox = QtWidgets.QComboBox(OpenOrd)
        self.comboBox.setObjectName("comboBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.radioButton = QtWidgets.QRadioButton(OpenOrd)
        self.radioButton.setObjectName("radioButton")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.radioButton)
        self.label_2 = QtWidgets.QLabel(OpenOrd)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(OpenOrd)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.label_6 = QtWidgets.QLabel(OpenOrd)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.lineEdit_2 = QtWidgets.QLineEdit(OpenOrd)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.checkBox = QtWidgets.QCheckBox(OpenOrd)
        self.checkBox.setObjectName("checkBox")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.checkBox)
        self.label_3 = QtWidgets.QLabel(OpenOrd)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_3 = QtWidgets.QLineEdit(OpenOrd)
        self.lineEdit_3.setEnabled(False)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.lineEdit_3)
        self.checkBox_2 = QtWidgets.QCheckBox(OpenOrd)
        self.checkBox_2.setObjectName("checkBox_2")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.checkBox_2)
        self.label_4 = QtWidgets.QLabel(OpenOrd)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.lineEdit_4 = QtWidgets.QLineEdit(OpenOrd)
        self.lineEdit_4.setEnabled(False)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.lineEdit_4)
        self.label_5 = QtWidgets.QLabel(OpenOrd)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.lineEdit_5 = QtWidgets.QLineEdit(OpenOrd)
        self.lineEdit_5.setEnabled(True)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.lineEdit_5)
        self.checkBox_3 = QtWidgets.QCheckBox(OpenOrd)
        self.checkBox_3.setObjectName("checkBox_3")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.checkBox_3)
        self.buttonBox = QtWidgets.QDialogButtonBox(OpenOrd)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.buttonBox)
        self.label = QtWidgets.QLabel(OpenOrd)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.radioButton_2 = QtWidgets.QRadioButton(OpenOrd)
        self.radioButton_2.setObjectName("radioButton_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.radioButton_2)

        self.retranslateUi(OpenOrd)
        self.buttonBox.accepted.connect(OpenOrd.accept)
        self.buttonBox.rejected.connect(OpenOrd.reject)
        QtCore.QMetaObject.connectSlotsByName(OpenOrd)

    def retranslateUi(self, OpenOrd):
        _translate = QtCore.QCoreApplication.translate
        OpenOrd.setWindowTitle(_translate("OpenOrd", "Dialog"))
        self.radioButton.setText(_translate("OpenOrd", "Long"))
        self.label_2.setText(_translate("OpenOrd", "Amoiunt"))
        self.label_6.setText(_translate("OpenOrd", "Rate"))
        self.checkBox.setText(_translate("OpenOrd", "Stop"))
        self.label_3.setText(_translate("OpenOrd", "Stop"))
        self.checkBox_2.setText(_translate("OpenOrd", "Trailing Step"))
        self.label_4.setText(_translate("OpenOrd", "Trailing Step"))
        self.label_5.setText(_translate("OpenOrd", "Limit"))
        self.checkBox_3.setText(_translate("OpenOrd", "In pips"))
        self.label.setText(_translate("OpenOrd", "Symbol"))
        self.radioButton_2.setText(_translate("OpenOrd", "Short"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OpenOrd = QtWidgets.QDialog()
    ui = Ui_OpenOrd()
    ui.setupUi(OpenOrd)
    OpenOrd.show()
    sys.exit(app.exec_())
