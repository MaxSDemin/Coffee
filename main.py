import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QWidget, QDialog, QMessageBox
from PyQt5 import QtCore, QtWidgets
import sqlite3

class Main_UI(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(666, 480)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.button_close = QtWidgets.QPushButton(Form)
        self.button_close.setObjectName("button_close")
        self.gridLayout.addWidget(self.button_close, 1, 4, 1, 1)
        self.button_del = QtWidgets.QPushButton(Form)
        self.button_del.setObjectName("button_del")
        self.gridLayout.addWidget(self.button_del, 1, 2, 1, 1)
        self.button_add = QtWidgets.QPushButton(Form)
        self.button_add.setObjectName("button_add")
        self.gridLayout.addWidget(self.button_add, 1, 0, 1, 1)
        self.table = QtWidgets.QTableWidget(Form)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.AnyKeyPressed|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.table.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.table, 0, 0, 1, 5)
        self.button_edit = QtWidgets.QPushButton(Form)
        self.button_edit.setObjectName("button_edit")
        self.gridLayout.addWidget(self.button_edit, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 3, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Кофе"))
        self.button_close.setText(_translate("Form", "Закрыть"))
        self.button_del.setText(_translate("Form", "Удалить"))
        self.button_add.setText(_translate("Form", "Добавить"))
        self.button_edit.setText(_translate("Form", "Редактировать"))

class Coffee(QWidget, Main_UI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.add_window = Form_add_edit()
        self.header = (
            'ID', 'Назвение сорта', 'Степень обжарки', 'Степень помола',
            'Описание вкуса', 'Цена, руб.', 'Вес упаковки г.')
        self.load_db()
        self.bind_button()
        self.set_box()
        self.mode = ''

    def bind_button(self):
        self.button_add.clicked.connect(self.add_new_record)
        self.button_edit.clicked.connect(self.edit_record)
        self.button_close.clicked.connect(self.close)
        self.button_del.clicked.connect(self.del_row)

    def load_db(self):
        connect_bd = sqlite3.connect('data/coffee.db')
        cursor = connect_bd.cursor()
        res = cursor.execute('''select coffee.ID, name, objar, pom, vkus, price, objem  from coffee, obj, pomol
                               where coffee.objarka = obj.ID and coffee.pomol = pomol.ID''').fetchall()
        vyborka = []
        for i in res:
            vyborka.append(i)
        connect_bd.close()
        self.view_table(vyborka)

    def view_table(self, sorted_list):
        num_col = len(sorted_list[0])
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.table.setColumnCount(num_col)
        for i, row in enumerate(sorted_list):
            self.table.setRowCount(self.table.rowCount() + 1)
            for k, item in enumerate(row):
                self.table.setItem(i, k, QTableWidgetItem(str(item)))
        self.table.setHorizontalHeaderLabels(self.header)
        self.table.resizeColumnsToContents()

    def set_box(self):
        self.add_window.comboBox_proj.addItem('')
        self.add_window.comboBox_pomol.addItem('')
        connect_bd = sqlite3.connect('data/coffee.db')
        cursor = connect_bd.cursor()
        res = cursor.execute('''select *  from  obj''').fetchall()
        for i in res:
            self.add_window.comboBox_proj.addItem(i[1])
        res = cursor.execute('''select *  from  pomol''').fetchall()
        for i in res:
            self.add_window.comboBox_pomol.addItem(i[1])
        connect_bd.close()

    def add_new_record(self):
        data = []
        column = self.table.columnCount()
        for i in range(column):
            data.append('')
        self.set_edit_form(data)
        self.add_window.show()

    def edit_record(self):
        row = self.table.currentRow()
        if int(row) < 0:
            return
        column = self.table.columnCount()
        row_data = []
        for i in range(column):
            cell = self.table.item(row, i).text()
            row_data.append(cell)
        self.set_edit_form(row_data)
        self.add_window.show()
        self.mode = 'edit'

    def set_edit_form(self, data):
        self.add_window.label_id.setText(data[0])
        self.add_window.sort.setText(data[1])
        self.add_window.comboBox_proj.setCurrentText(data[2])
        self.add_window.comboBox_pomol.setCurrentText(data[3])
        self.add_window.vkus.setText(data[4])
        self.add_window.price.setText(data[5])
        self.add_window.vol.setText(data[6])

    def update_db(self):
        name = self.add_window.sort.text()
        obj = self.add_window.comboBox_proj.currentIndex()
        pomol = self.add_window.comboBox_pomol.currentIndex()
        vkus = self.add_window.vkus.toPlainText()
        price = self.add_window.price.text()
        vol = self.add_window.vol.text()
        connect_bd = sqlite3.connect('data/coffee.db')
        cursor = connect_bd.cursor()

        if self.mode == 'edit':

            id_row = self.add_window.label_id.text()
            qry = 'UPDATE coffee SET name="' + name
            qry += '", objarka="' + str(obj)
            qry += '", pomol="' + str(pomol)
            qry += '", vkus="' + vkus
            qry += '", price="' + price
            qry += '", objem="' + vol
            qry += '" WHERE ID=' + str(id_row)
            self.mode = ''
        else:
            qry = 'INSERT INTO coffee (name, objarka, pomol, vkus, price, objem) VALUES ("'
            qry += name + '", "' + str(obj) + '", "' + str(
                pomol) + '", "' + vkus + '", "' + price + '", "' + vol +'")'
        cursor.execute(qry)
        connect_bd.commit()
        connect_bd.close()
        self.load_db()

    def del_row(self):
        row = self.table.currentRow()
        id_row = self.table.item(row, 0).text()
        valid = QMessageBox.question(self, '', 'Действительно удалить запись № ' + id_row, QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            connect_bd = sqlite3.connect('data/coffee.db')
            cursor = connect_bd.cursor()
            qry = "DELETE from coffee WHERE ID =" + id_row
            cursor.execute(qry)
            connect_bd.commit()
            connect_bd.close()
            self.load_db()


class Ui_add_edit_form(object):
    def setupUi(self, add_edit_form):
        add_edit_form.setObjectName("add_edit_form")
        add_edit_form.resize(335, 301)
        add_edit_form.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(add_edit_form)
        self.gridLayout.setObjectName("gridLayout")
        self.label_7 = QtWidgets.QLabel(add_edit_form)
        self.label_7.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)
        self.label_id = QtWidgets.QLabel(add_edit_form)
        self.label_id.setObjectName("label_id")
        self.gridLayout.addWidget(self.label_id, 0, 1, 1, 1)
        self.button_ok = QtWidgets.QPushButton(add_edit_form)
        self.button_ok.setObjectName("button_ok")
        self.gridLayout.addWidget(self.button_ok, 0, 3, 2, 1)
        self.label_2 = QtWidgets.QLabel(add_edit_form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 2, 3)
        self.button_cancel = QtWidgets.QPushButton(add_edit_form)
        self.button_cancel.setObjectName("button_cancel")
        self.gridLayout.addWidget(self.button_cancel, 2, 3, 2, 1)
        self.sort = QtWidgets.QLineEdit(add_edit_form)
        self.sort.setObjectName("sort")
        self.gridLayout.addWidget(self.sort, 3, 0, 1, 3)
        self.label_3 = QtWidgets.QLabel(add_edit_form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 2)
        self.label_5 = QtWidgets.QLabel(add_edit_form)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 2, 1, 1)
        self.comboBox_proj = QtWidgets.QComboBox(add_edit_form)
        self.comboBox_proj.setObjectName("comboBox_proj")
        self.gridLayout.addWidget(self.comboBox_proj, 5, 0, 1, 2)
        self.price = QtWidgets.QLineEdit(add_edit_form)
        self.price.setObjectName("price")
        self.gridLayout.addWidget(self.price, 5, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(add_edit_form)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 2)
        self.label_6 = QtWidgets.QLabel(add_edit_form)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 6, 2, 1, 1)
        self.comboBox_pomol = QtWidgets.QComboBox(add_edit_form)
        self.comboBox_pomol.setObjectName("comboBox_pomol")
        self.gridLayout.addWidget(self.comboBox_pomol, 7, 0, 1, 2)
        self.vol = QtWidgets.QLineEdit(add_edit_form)
        self.vol.setObjectName("vol")
        self.gridLayout.addWidget(self.vol, 7, 2, 1, 1)
        self.label = QtWidgets.QLabel(add_edit_form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 8, 0, 1, 2)
        self.vkus = QtWidgets.QTextEdit(add_edit_form)
        self.vkus.setObjectName("vkus")
        self.gridLayout.addWidget(self.vkus, 9, 0, 1, 4)

        self.retranslateUi(add_edit_form)
        QtCore.QMetaObject.connectSlotsByName(add_edit_form)

    def retranslateUi(self, add_edit_form):
        _translate = QtCore.QCoreApplication.translate
        add_edit_form.setWindowTitle(_translate("add_edit_form", "Dialog"))
        self.label_7.setText(_translate("add_edit_form", "ID: "))
        self.label_id.setText(_translate("add_edit_form", "00"))
        self.button_ok.setText(_translate("add_edit_form", "OK"))
        self.label_2.setText(
            _translate("add_edit_form", "Название сорта кофе:"))
        self.button_cancel.setText(_translate("add_edit_form", "Cancel"))
        self.label_3.setText(_translate("add_edit_form", "Степень прожарки:"))
        self.label_5.setText(_translate("add_edit_form", "Цена, руб:"))
        self.label_4.setText(_translate("add_edit_form", "Степень помола:"))
        self.label_6.setText(_translate("add_edit_form", "Вес упаковки, гр:"))
        self.label.setText(_translate("add_edit_form", "Описание вкуса:"))

class Form_add_edit(QDialog, Ui_add_edit_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button_ok.clicked.connect(self.check)
        self.button_cancel.clicked.connect(self.close)

    def check(self):
        if self.sort.text() and self.comboBox_proj.currentIndex() and self.comboBox_pomol.currentIndex() and \
                self.vkus.toPlainText() and self.price.text().isdigit() and self.vol.text().isdigit():
            coffee.update_db()
            self.close()
        else:
            return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    coffee = Coffee()
    coffee.move(350, 30)
    coffee.show()
    sys.exit(app.exec_())
