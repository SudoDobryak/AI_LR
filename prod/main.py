import sys	# sys нужен для передачи argv в QApplication
import MainWindowDesign	# Это наш конвертированный файл дизайна
from PyQt5 import QtWidgets
from ProdApp import ProdApp

def main():
	app = QtWidgets.QApplication(sys.argv)	# Новый экземпляр QApplication
	window = ProdApp()	# Создаём объект класса ProdApp
	window.show()	# Показываем окно
	app.exec_()	# и запускаем приложение

if __name__ == '__main__':	# Если мы запускаем файл напрямую, а не импортируем
	main()	# то запускаем функцию main()