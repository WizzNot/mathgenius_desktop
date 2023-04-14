import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from gui import Ui_MainWindow
import random
from math import sin, cos, tan, radians
import sqlite3


def roots_of_quadratic_equation(a, b, c): # Функция решения уравнений
    if a == b == c == 0:
        return ["all"]
    elif a == b == 0:
        return ["Нет корней"]
    elif a == c == 0:
        return [0]
    elif b == c == 0:
        return [0]
    elif b == 0:
        return [(-1 * c / a) ** 0.5, -1 * ((-1 * c / a) ** 0.5) if c * a <= 0 else "нету"]
    elif c == 0:
        return [(-1 * b) / a, 0]
    elif a == 0:
        return [c / b * -1]
    else:
        d = (b ** 2) - (4 * a * c)
        if d < 0:
            return ["Нет корней"]
        elif d > 0:
            return [(((-1 * b) - (d ** 0.5)) / (a * 2)), (((-1 * b) + (d ** 0.5))) / (a * 2)]
        else:
            return [(-1 * b) / (a * 2)]


def test(z): # Функция для тестов
    global primer
    global otv
    primer = ""
    otv = 0
    if z == 1:
        count = random.randint(2, 5)
        for i in range(1, count + 1):
            t = random.randrange(-100000, 100000) / 10
            otv += t
            if str(t)[0] != "-":
                primer = primer + "+" + str(t)
            else:
                primer = primer + str(t)
        otv = [float(round(otv, 1))]
    elif z == 2:
        a, b, c = random.randint(-100, 100), random.randint(-100, 100), random.randint(-100, 100)
        while any([i not in range(-1000, 1000)
                   for i in roots_of_quadratic_equation(a, b, c)]) or (
                       b ** 2) - (4 * a * c) < 0:
            a, b, c = random.randint(-100, 100), random.randint(-100, 100), random.randint(-100, 100)
        otv = [float(i) if i != "all" else "all"
               for i in sorted(roots_of_quadratic_equation(a, b, c))]
        if otv == ["all"]:
            otv = ["любой"]
        bplus = "+" if b >= 0 else "-"
        cplus = "+" if c >= 0 else "-"
        primer = str(a) + "x²" + bplus + str(abs(b)) + "x" + cplus + str(abs(c)) + " = 0"
    elif z == 3:
        q = random.choice([False, True])
        if q:
            count = random.randint(2, 5)
            for i in range(1, count + 1):
                t = random.randrange(-100000, 100000) / 10
                otv += t
                if str(t)[0] != "-":
                    primer = primer + "+" + str(t)
                else:
                    primer = primer + str(t)
            primer = primer[1:]
            otv = [float(round(otv, 1))]
        elif not q:
            a, b, c = random.randint(-100, 100), random.randint(-100, 100), random.randint(-100, 100)
            while any([i not in range(-1000, 1000)
                       for i in roots_of_quadratic_equation(a, b, c)]) or (
                           b ** 2) - (4 * a * c) < 0:
                a, b, c = random.randint(-100, 100), random.randint(-100, 100), random.randint(-100, 100)
            otv = [float(i) if i != "all" else "all"
                   for i in sorted(roots_of_quadratic_equation(a, b, c))]
            if otv == ["all"]:
                otv = ["любой"]
            bplus = "+" if b >= 0 else "-"
            cplus = "+" if c >= 0 else "-"
            primer = str(a) + "x²" + bplus + str(abs(b)) + "x" + cplus + str(abs(c)) + " = 0"


def testres(otvet): # Функция для вывода текста в поле тестов
    try:
        a = [float(i) for i in otvet.replace(' ', '').split(',')]
        if all([i in otv for i in a]) and len(otv) == len(a):
            test(3)
            nextword = random.choice(["Молодец!", "Правильно!", "Ты гений!", "Так держать!"])
            return nextword + " Следующий пример: " + primer
        else:
            return 'Неверно! Попробуй еще раз. ' + primer
    except:
        return 'Неверный формат ввода! Ответы разделяйте \
запятой,\nдесятые от целой части - точкой.\n' + primer
    
    
def listres(otvet): # Функция для вывода текста в поле набора чисел
    try:
        a = [float(i) for i in otvet.replace(' ', '').split(',')]
        sr = sum(a) / len(a)
        disp = str(sum([(i - sr) ** 2 for i in a]) / len(a))
        mod_list = []
        moda_count = max([int(a.count(i)) for i in a])
        for i in a:
            if int(a.count(i)) == moda_count and str(i) not in mod_list:
                mod_list.append(str(i))
        moda = ', '.join(mod_list)
        med = sorted(a)[len(a) // 2] if len(a) % 2 != 0 else (sorted(a)[len(a) // 2] +
                                                              sorted(a)[len(a) // 2 - 1]) / 2
        return 'Дисперсия: ' + disp + '\nМода: ' + moda + '\n Медиана: ' + str(med)
    except:
        return 'Что то пошло не так! Вводите набор чисел через запятую'
    
    
def answerme(otvet): # Функция для вывода текста в поле решения примеров
    try:
        q = otvet[0:otvet.find("=")] if "=" in otvet else otvet
        q = q.replace(' ', '').replace('**', '^')
        if 'x' in q.lower():
            if "x^2" not in q:
                a = 0
                b = float(q[0:q.find("x")]) if q[0] != "x" else 1
                c = float(q[q.find("x") + 1:]) if len(q) > q.find("x") else 0
                return "Ответ: " + ", ".join([str(round(i, 5)) for i in roots_of_quadratic_equation(a, b, c)])
            elif "x^2" in q:
                if q.count("x") == 1:
                    a = float(q[0:q.find("x^2")]) if q[0] != "x" else 1
                    b = 0
                    c = float(q[q.find("x^2") + 3:] if len(q) > q.find("x^2") + 2 else 0)
                    return "Ответ: " + ", ".join([str(round(i, 5)) for i in roots_of_quadratic_equation(a, b, c)])
                elif q.count("x") == 2:
                    a = float(q[0:q.find("x^2")]) if q[0] != "x" else 1
                    b = float(q[q.find("x^2") + 3:q.rfind("x")]) if q[q.rfind("x") - 1] != "+" \
                        and q[q.rfind("x") - 1] != "-" else 1
                    c = float(q[q.rfind("x") + 1:]) if len(q) > q.rfind("x") else 0
                    return "Ответ: " + ", ".join([str(round(i, 5))
                                                  for i in roots_of_quadratic_equation(a, b, c)])
                else:
                    return "приведите уравнение в стандартный вид"
        else:
            return "Ответ: " + str(eval(q.replace(":", "/").replace("^", "**").replace(",", ".")))
    except:
        return 'Неверный формат ввода!\nУравнение ввводите в формате\nAx^2 + Bx + C = 0\nДля \
разделения десятичной\nчасти используйте точку'


class Task: # Класс задач в программе
    def __init__(self, starttext, t, button, buttonstart, linein, reswidget, function, *args):
        self.button = button
        self.start = buttonstart
        self.linein = linein
        self.res = reswidget
        self.function = function
        self.hides = []
        self.shows = []
        self.starttext = starttext
        a = [self.button, self.start, self.linein,
             self.res, self.function] + [i for i in args]
        for i in t:
            if i not in a:
                self.hides.append(i)
            else:
                self.shows.append(i)
        self.button.clicked.connect(self.hideshow)
        self.start.clicked.connect(self.result)

    def hideshow(self): # Спрятать ненужные виджеты и показать нужные
        for i in self.hides:
            i.hide()
        for i in self.shows:
            i.show()
        self.res.setText(self.starttext)
            
    def result(self):
        self.res.setText(self.function(self.linein.text()))
        

class Example(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setupUi(self) # подключение интерфейса
        self.all = [self.testin, self.teststartbutton,
                    self.listin, self.answerlabel, self.answerin,
                    self.funcres, self.funcin, self.funclab,
                    self.funcstartbutton, self.answerstartbutton,
                    self.testlabel, self.listlabel, self.answerlabel,
                    self.liststartbutton, self.funclab2, self.funcdiap,
                    self.tasklabel, self.taskin, self.taskstartbutton] # все виджеты
        for i in self.all:
            i.hide()
        self.setWindowTitle('Продвинутый калькулятор')
        test(3)
        startanswertxt = 'Я могу решить уравнения степени не выше\nвторой и примеры. \
Приведите\nуравнение в стандартный вид'
        starttesttxt = 'Для десятичной записи числа используйте ".",\nдля \
ввода нескольких ответов\nвводите через запятую ' + primer
        self.test = Task(starttesttxt, self.all, self.testbutton, # тесты
                         self.teststartbutton, self.testin, self.testlabel, testres)
        self.sinbutton.clicked.connect(self.sinus)
        startlisttxt = 'Введите набор чисел через запятую,\nДесятичную часть отделяйте точкой'
        self.answermee = Task(startanswertxt, self.all, self.answerbutton, # решения примеров
                              self.answerstartbutton, self.answerin, self.answerlabel, answerme)
        self.list = Task(startlisttxt, self.all, self.listbutton, # наборы чисел
                         self.liststartbutton, self.listin, self.listlabel, listres)
        self.funcbutton.clicked.connect(self.funcshow)
        self.funcstartbutton.clicked.connect(self.funcstart)
        self.funcin.setText('x ^ 2')
        self.funcdiap.setText('-10, 10')
        self.taskbutton.clicked.connect(self.taskhideshow)
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        self.db = cur.execute("""SELECT * FROM tasks""").fetchall() # база данных с задачами
        self.taskstartbutton.clicked.connect(self.tasknext)
        
    def taskhideshow(self): # функция для показа виджетов задач
        self.counttask = 0
        self.countcorrect = 0
        for i in self.all:
            if i not in [self.taskin, self.tasklabel, self.taskstartbutton]:
                i.hide()
            else:
                i.show()
        self.tasklabel.setText(self.db[self.counttask][1])
        
    def tasknext(self): # функция задач
        if int(self.taskin.text()) == self.db[self.counttask][2]:
            self.countcorrect += 1
        self.counttask += 1
        if self.counttask == len(self.db):
            self.tasklabel.setText('Тест завершен! Правильных ответов:\n' +
                                   str(self.countcorrect) + ' из ' + str(len(self.db)))
            self.taskin.hide()
            self.taskstartbutton.hide()
        else:
            self.tasklabel.setText(self.db[self.counttask][1])
        self.taskin.setText('')
        
    def funcshow(self): # показ виджетов графиков
        for i in self.all:
            if i not in [self.funcbutton, self.funcstartbutton, self.funcin,
                         self.funcres, self.funclab, self.funclab2, self.funcdiap]:
                i.hide()
            else:
                i.show()
                
    def funcstart(self): # функция графиков функций
        try:
            self.funcres.clear()
            diap = sorted([int(i) for i in self.funcdiap.text().replace(' ', '').split(',')])
            self.funcres.plot([i for i in range(diap[0], diap[1] + 1)], [
                eval(self.funcin.text().replace('^', '**'))
                for x in range(diap[0], diap[1] + 1)], pen='r')
        except:
            self.funcin.setText('Ошибка! Вводите в виде x ** 2')
            self.funcdiap.setText('Вводите через запятую')
        
    def sinus(self): # функция для синусов косинусов и тангенсов
        try:
            answer = 'Sin: ' + str(round(sin(radians(float(self.sinline.text()))), 5))
            answer += '\nCos: ' + str(round(cos(radians(float(self.sinline.text()))), 5))
            answer += '\nTg: ' + str(round(tan(radians(float(self.sinline.text()))), 5))
            self.sinres.setText(answer)
        except:
            self.sinres.setText('Неверный формат ввода.\nДесятичную часть отделяйте\nточкой')


app = QApplication(sys.argv)
ex = Example()
ex.show()
sys.exit(app.exec_())

