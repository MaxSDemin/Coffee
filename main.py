import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QWidget, QDialog, QMessageBox
import sqlite3


class Coffee(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
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
        connect_bd = sqlite3.connect('coffee.db')
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
        connect_bd = sqlite3.connect('coffee.db')
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
        connect_bd = sqlite3.connect('coffee.db')
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
            connect_bd = sqlite3.connect('coffee.db')
            cursor = connect_bd.cursor()
            qry = "DELETE from coffee WHERE ID =" + id_row
            cursor.execute(qry)
            connect_bd.commit()
            connect_bd.close()
            self.load_db()

class Form_add_edit(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
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
