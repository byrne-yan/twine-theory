from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import stockGUIs as tgui
import pandas as pd
import sys

sys.path.append("..")
from twine_theory.domain import twine_theory as tt

def createWidget(nks):
    return tgui.StickWidget(tt.KSeq('day', nks))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = QtGui.QMainWindow()
    w.show()
    w.resize(800,600)
    w.setWindowTitle('stock: stick graph')

    view = pg.GraphicsLayoutWidget()
    w.setCentralWidget(view)

    if len(sys.argv) >= 2:
        ks = pd.read_csv(sys.argv[1],parse_dates=['date'],index_col='date',dtype={"code":str})
        #倒置
##        ks = ks.sort_values('date')
        view.addItem(createWidget(ks))
        view.setBackground('w')

        app.exec_()
    else:
        print("missing data file")


