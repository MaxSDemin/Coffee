import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QWidget
import sqlite3


class Coffee(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.header = (
        'Назвение сорта', 'Степень обжарки', 'Степень помола', 'Описание вкуса', 'Цена, руб.', 'Объем упаковки г.')
        self.load_db()

    def load_db(self):
        connect_bd = sqlite3.connect('coffee.db')
        cursor = connect_bd.cursor()
        res = cursor.execute('''select name, objar, pom, vkus, price, objem  from coffee, obj, pomol 
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    coffee = Coffee()
    coffee.move(350, 30)
    coffee.show()
    sys.exit(app.exec_())
