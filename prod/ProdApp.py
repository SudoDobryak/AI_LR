from PyQt5 import QtCore, QtGui, QtWidgets
import MainWindowDesign # Это наш конвертированный файл дизайна
import re # Для запросов
import os # Для БД
import json # Для БД
import pymorphy2 # Для Нормальной Формы

morph = pymorphy2.MorphAnalyzer()

DB_RULES_PATH = os.path.join(os.path.dirname(__file__), 'db', 'rules.json')
DB_PREDS_PATH = os.path.join(os.path.dirname(__file__), 'db', 'preds.json')

class ProdApp(QtWidgets.QWidget, MainWindowDesign.Ui_Form):
	def __init__(self):
		# Это здесь нужно для доступа к переменным, методам
		# и т.д. в файле design.py
		super().__init__()
		self.setupUi(self)  # Это нужно для инициализации нашего дизайна

		# Search Layout
		self.search_btn.clicked.connect(self.searchAnswer)

		"""
		Признаки
		"""
		self._preds = set()
		# Edit Pred Layout
		self.pred_add_btn.clicked.connect(self.addPred)
		self.pred_delete_btn.clicked.connect(self.delPred)
		# Load Save Pred Layout
		self.pred_save_btn.clicked.connect(self.savePredToDb)
		# self.pred_load_btn.clicked.connect(self.loadPredFromDb)
		self.loadPredFromDb()

		"""
		Правила
		"""
		self._rules = {} # Глобальная база данных
		
		# Edit Rule Layout
		self.rule_add_btn.clicked.connect(self.addRule)
		self.rule_delete_btn.clicked.connect(self.deleteRule)
		
		# Load Save Rule Layout
		self.rule_save_btn.clicked.connect(self.saveRuleToDb)
		self.loadRuleFromDb()
		# self.rule_load_btn.clicked.connect(self.loadRuleFromDb)

		# Для масштабирования виджета таблицы
		header = self.rules_table.horizontalHeader()
		header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

	def searchAnswer(self):
		"""
		Поиск ответа
		"""
		question = self.search_line.text()
		terms = self.offerToTerms(question)
		
		for rule_if, rule_then in self._rules.items():
			rule_terms = self.offerToTerms(rule_if)

			if self.checkRule(terms, rule_terms):
				self.showMessage("Рекомендуемая профессия: " + rule_then, str(rule_if))
				return

		self.showMessage("Ответ на заданный вопрос отсутствует в Базе Знаний!", str(terms))
		
	def showMessage(self, info, details):
		"""
		Выведение сообщения на экран
		"""
		msg = QtWidgets.QMessageBox()
		msg.setText(info)
		msg.setWindowTitle("Экспертное заключение")
		msg.setDetailedText(details)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		msg.exec_()

# ПРИЗНАКИ

	def addPred(self):
		text = self.getNormal(self.pred_line.text())
		if(text not in self._preds):
			self._preds.add(text)
			self.pred_list.addItem(text)
		else:
			self.showMessage('Ошибка! Такой признак уже присутствует в Базе Признаков', str())

	def delPred(self):
		row = self.pred_list.currentRow()
		if(self.pred_list.selectedItems()):
			item = self.pred_list.takeItem(row)
			self._preds.remove(item.text())

	def savePredToDb(self):
		"""
		Сохранение в базу данных (файл формата JSON)
		"""
		data = list(self._preds)
		preds_path = DB_PREDS_PATH

		with open(preds_path, 'w') as outfile:
			json.dump(data, outfile, indent=1, ensure_ascii=False)

		self.showMessage('Атрибуты "{}" сохранены в {}\n'.format(self._preds, preds_path), str())
		self.loadPredFromDb()

	def loadPredFromDb(self):
		"""
		Загрузка правил из Базы Данных (файл формата JSON)
		"""
		preds_path = DB_PREDS_PATH
		self.pred_list.clear()
		with open(preds_path, 'r') as infile:
			data = json.load(infile)
		self._preds = set(data)
		for pred in self._preds:
			self.pred_list.addItem(pred)
		# self.showMessage('Признаки "{}" загружены из {}'.format(self._preds, preds_path), str())

# ПРАВИЛА

	def addRule(self):
		"""
		Добавление правила
		"""
		text_if = self.getNormal(self.rule_if_line.text())
		text_then = self.getNormal(self.rule_then_line.text())

		if text_if not in self._rules and self.checkIf(text_if):
			i = self.rules_table.rowCount()
			self._rules[text_if] = text_then
			self.rules_table.setRowCount(i + 1)

			new_if = QtWidgets.QTableWidgetItem(text_if)
			self.rules_table.setItem(i, 0, new_if)
			text_then = self.rule_then_line.text()

			new_then = QtWidgets.QTableWidgetItem(text_then)
			self.rules_table.setItem(i, 1, QtWidgets.QTableWidgetItem(new_then))

	def deleteRule(self):
		"""
		Удаление правила
		"""
		if self.rules_table.selectedItems():
			rule_item = self.rules_table.selectedItems()[0]
			row = self.rules_table.row(rule_item)
			if_item = self.rules_table.item(row, 0)
			if_text = if_item.text()
			del self._rules[if_text]
			self.rules_table.removeRow(row)

	def checkRule(self, terms, rule_terms):
		"""
		Проверка правила
		"""
		for or_term in terms:
			for or_rule_term in rule_terms:
				if(len(or_rule_term) > len(or_term)):
					continue
				is_right = True

				for and_term in or_term:
					if(and_term not in or_rule_term):
						is_right = False
						break

				if is_right:
					return True

		return False

	def getNormal(self, offer):
		offer = offer.lower()
		words = offer.split()
		new_offer = ""
		for word in words:
			p = morph.parse(word)[0]
			if(new_offer != ""):
				new_offer += " "
			new_offer += p.normal_form
		return new_offer

	def checkIf(self, text):
		or_terms = self.offerToTerms(text)
		for and_terms in or_terms:
			for term in and_terms:
				if(term not in self._preds):
					self.showMessage('Признак \' '+term+' \' отсутствует в Базе Признаков', str())
					return False
		return True

	def offerToTerms(self, offer):
		"""
		Создание правил из предложений
		"""
		offer = self.getNormal(offer)

		or_terms = []
		or_strings = self.splitOr(offer)

		for or_str in or_strings:
			and_terms = self.splitAnd(or_str)
			or_terms.append(and_terms)
		return or_terms

	def splitAnd(self,offer):
		str_and = re.split(r" и ", offer)
		return self.listToDict(str_and)
	
	def splitOr(self,offer):
		str_or = re.split(r" или ", offer)
		return str_or

	def listToDict(self, list):
		dict = set()
		for str in list:
			dict.add(str)
		return dict

	def loadRuleFromDb(self):
		"""
		Загрузка правил из базы данных (файл формата JSON)
		"""
		rules_path = DB_RULES_PATH

		with open(rules_path, 'r') as infile:
			data = json.load(infile)
		self._rules = data
		self.rules_table.setRowCount(len(data))
		i = 0
		for rule_key, rule_value in data.items():
			self.rules_table.setItem(i, 0, QtWidgets.QTableWidgetItem(rule_key))
			self.rules_table.setItem(i, 1, QtWidgets.QTableWidgetItem(rule_value))
			i += 1
		# self.showMessage('Правила "{}" загружены из {}'.format(self._rules, rules_path), str())

	def saveRuleToDb(self):
		"""
		Сохранение в Базу Данных (файл формата JSON)
		"""
		data = self._rules
		rules_path = DB_RULES_PATH

		with open(rules_path, 'w') as outfile:
			json.dump(data, outfile, indent=1, ensure_ascii=False)
		
		self.showMessage('Правила "{}" сохранены в {}'.format(self._rules, rules_path), str())