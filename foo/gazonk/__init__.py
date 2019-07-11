import random
from datetime import datetime
import sys
import urllib.request

from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget)
from PySide2.QtCore import Slot, Qt

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

def get_armda_expenses():
    expenses = [
        Expense("Imperialer leicheter Träger", 26.55, datetime(2019, 7, 4),
                "https://www.fantasywelt.de/media/image/product/59162/md/star-wars-armada-imperialer-leichter-traeger-wave-6-de.jpg"),
        Expense("Rebellentransporter", 18.44, datetime(2019, 2, 8),
                "https://www.fantasywelt.de/media/image/product/51925/md/star-wars-armada-rebellentransporter-wave-3-de.jpg"),
        Expense("Imperialer Angriffsträger", 18.44, datetime(2019, 2, 8),
                "https://www.fantasywelt.de/media/image/product/51924/md/star-wars-armada-imperialer-angriffstraeger-wave-3-de.jpg"),
        Expense("Space Sector 7 6x3 Gaming Mat", 59.95, datetime(2019, 1, 13),
                "https://www.fantasywelt.de/media/image/product/49422/md/space-sector-7-6x3-gaming-mat.jpg")
    ]
    return expenses


class Expense(object):

    def __init__(self, title, price, date, image_url):
        self.title = title
        self.price = price
        self.date = date
        self.image_url = image_url
        self.image = None

    def prepare_rendering(self):
        if self.image:
            return
        response = urllib.request.urlopen(self.image_url)
        image_data = response.read()  # a `bytes` object
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        self.image = pixmap


class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.expenses = get_armda_expenses()
        # sort the expenses by date
        self.expenses.sort(key=lambda k: k.date)
        self.num_expenses = len(self.expenses)
        self.current_expense = -1

        ##plotting
        # a figure instance to plot on
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)
        ##end plotting

        self.plot_button = QPushButton("plot")
        self.next_button = QPushButton("next")
        self.text = QLabel("Armada Expenses")
        self.text.setAlignment(Qt.AlignCenter)

        self.text1 = QLabel("")
        self.text1.setAlignment(Qt.AlignCenter)
        self.text2 = QLabel("")
        self.text2.setAlignment(Qt.AlignCenter)
        self.text3 = QLabel("")
        self.text3.setAlignment(Qt.AlignCenter)
        self.image = QLabel()
        self.image.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.text1)
        self.layout.addWidget(self.text2)
        self.layout.addWidget(self.text3)
        self.layout.addWidget(self.image)
        self.layout.addWidget(self.plot_button)
        self.layout.addWidget(self.next_button)
        self.setLayout(self.layout)

        # Connecting the signal
        self.plot_button.clicked.connect(self.plot)
        self.next_button.clicked.connect(self.next)


    @Slot()
    def plot(self):
        ''' plot some random stuff '''
        data = [i.price for i in self.expenses]

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.clear()

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()

    @Slot()
    def next(self):
        if self.current_expense < self.num_expenses -1:
            self.current_expense += 1
        else:
            self.current_expense = 0
        expense = self.expenses[self.current_expense]
        expense.prepare_rendering()
        display_date = "{0:%Y-%m-%d}".format(expense.date)
        self.text1.setText(display_date)
        self.text2.setText(expense.title)
        self.text3.setText("{} Euro".format(expense.price))
        self.image.setPixmap(expense.image)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())
