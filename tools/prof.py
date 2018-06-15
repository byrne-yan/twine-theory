from line_profiler import LineProfiler
from pyqtgraph.Qt import QtCore, QtGui
import pandas as pd
import stockGUIs as tgui
import sys
sys.path.append("..")
from twine_theory.domain import twine_theory as tt
df = pd.read_csv("000001.csv")
df.sort_values('date')

app = QtGui.QApplication(sys.argv)
w = QtGui.QMainWindow()
w.show()
w.resize(800, 600)

profiler = LineProfiler()
# import pdb;pdb.set_trace()
s = tgui.StickWidget(tt.KSeq('day',[]))
lp_wrapper = profiler(tgui.StickWidget.__init__)
lp_wrapper(s, tt.KSeq('day',df))
profiler.print_stats()
