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
        start = 0
        end = len(ks)
        if len(sys.argv)>=3:
            start = int(sys.argv[2])
        if len(sys.argv)>=4:
            end = int(sys.argv[3])
        print("Total: %d" % (end-start))
        view.addItem(createWidget(ks[start:end]))
        view.setBackground('w')

        app.exec_()
    else:
        print("missing data file")


