from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import stockGUIs as ds
import sys

sys.path.append("..")
from twine_theory.domain import twine_theory as tt

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = QtGui.QMainWindow()
    w.show()
    w.resize(400,600)
    w.setWindowTitle('stock: stick graph')

    view = pg.GraphicsLayoutWidget()
    w.setCentralWidget(view)


    p = view.addPlot()


    ks = [
    ('2018/1/2',13.35,13.93,13.7,13.32,2081592.5)
    ,('2018/1/3',13.73,13.86,13.33,13.2,2962498.25)
    ,('2018/1/4',13.32,13.37,13.25,13.13,1854509.5)
    ,('2018/1/5',13.21,13.35,13.3,13.15,1210312.75)
    ,('2018/1/8',13.25,13.29,12.96,12.86,2158620.75)
    ,('2018/1/9',12.96,13.2,13.08,12.92,1344345.12)
    ,('2018/1/10',13.04,13.49,13.47,12.92,2403277.5)
    ,('2018/1/11',13.41,13.59,13.4,13.27,1443877.75)
    ,('2018/1/12',13.45,13.68,13.55,13.41,1353991.38)
    ,('2018/1/15',13.51,14.33,14.2,13.5,3122394.5)
    ,('2018/1/16',14.17,14.38,14.2,14.02,2444549)
    ,('2018/1/17',14.33,14.8,14.23,14.2,2656294)
    ,('2018/1/18',14.4,14.72,14.72,14.28,2148027)
    ,('2018/1/19',14.8,15.13,14.8,14.68,2571146.75)
    ,('2018/1/22',14.6,14.94,14.44,14.43,2073867.25)
    ,('2018/1/23',14.36,14.9,14.65,14.33,2388791.75)
    ,('2018/1/24',14.66,15.08,14.64,14.5,2591292.25)
    ,('2018/1/25',14.45,14.47,14.2,14,2369984.75)
    ,('2018/1/26',14.18,14.34,14.05,14.02,2032988.62)
    ,('2018/1/29',14.05,14.25,13.74,13.6,2090546.75)
    ,('2018/1/30',13.7,13.84,13.65,13.55,1094739.88)
    ,('2018/1/31',13.6,14.05,14.05,13.53,1747729.12)
    ,('2018/2/1',13.95,14.3,14.03,13.84,2005614.75)
    ,('2018/2/2',13.91,14.1,14.05,13.63,1176512.75)
    ,('2018/2/5',13.8,14.57,14.55,13.73,2331998)
    ,('2018/2/6',14.23,14.33,14,13.93,2582872)
    ,('2018/2/7',14.22,14.3,12.92,12.76,3345717)
    ,('2018/2/8',12.83,12.92,12.54,12.53,2137815)
    ,('2018/2/9',12.08,12.08,11.69,11.38,2824949.75)
    ,('2018/2/12',11.78,11.84,11.72,11.56,1228782.38)
    ,('2018/2/13',11.87,12.21,11.94,11.84,1298178.75)
    ,('2018/2/14',11.96,12.03,12,11.76,864190.25)
    ,('2018/2/22',12.25,12.53,12.46,12.25,1268406.12)
    ,('2018/2/23',12.58,12.79,12.61,12.45,1013663.19)
    ,('2018/2/26',12.77,12.85,12.63,12.45,1045758.75)
    ,('2018/2/27',12.64,12.7,12.28,12.19,1285869)
    ,('2018/2/28',12.1,12.19,12.05,11.93,1214145.62)
    ,('2018/3/1',11.92,12.15,12.04,11.9,886957.19)
    ,('2018/3/2',11.92,12.04,11.95,11.85,663124.19)
    ,('2018/3/5',11.93,12.08,11.86,11.8,754183.12)
    ,('2018/3/6',11.95,12.11,12.1,11.77,1150162.5)
    ,('2018/3/7',12.15,12.34,12.05,12.04,1427570.25)
    ,('2018/3/8',12.05,12.15,12.11,11.95,689755.06)
    ,('2018/3/9',12.15,12.2,12.09,11.98,943876.94)
    ,('2018/3/12',12.15,12.17,12.03,11.95,1268701.25)
    ,('2018/3/13',12.04,12.22,12.02,12,1082267.38)
    ,('2018/3/14',11.98,12,11.92,11.83,635594.12)
    ,('2018/3/15',11.79,11.85,11.71,11.66,1155694.75)
    ,('2018/3/16',11.72,11.85,11.64,11.64,962983.38)
    ,('2018/3/19',11.66,11.84,11.83,11.61,808538.75)
    ,('2018/3/20',11.74,11.88,11.82,11.72,776150)
    ,('2018/3/21',11.95,12.12,11.9,11.85,1445109.5)
    ,('2018/3/22',11.9,11.97,11.66,11.62,984278.38)
    ,('2018/3/23',11.25,11.35,11.34,10.92,1825690.75)
    ,('2018/3/26',11.15,11.2,10.93,10.86,1383598.5)
    ,('2018/3/27',11.1,11.17,10.94,10.86,1103933.62)
    ,('2018/3/28',10.85,11.14,10.89,10.79,1099023.38)
    ,('2018/3/29',10.92,11.17,11.05,10.55,1330602.38)
    ,('2018/3/30',11.04,11.05,10.9,10.88,752173.69)
    ,('2018/4/2',10.87,10.99,10.71,10.7,1109316.38)
    ,('2018/4/3',10.6,10.67,10.56,10.51,890745.69)
    ,('2018/4/4',10.68,11.01,10.87,10.6,1602488.75)
    ,('2018/4/9',10.8,11.1,11.02,10.73,1074795.75)
    ,('2018/4/10',11.02,11.46,11.42,10.97,1390950.75)
    ,('2018/4/11',11.39,11.92,11.83,11.38,2095970.38)
    ,('2018/4/12',11.8,11.83,11.52,11.42,1173128.12)
    ,('2018/4/13',11.64,11.79,11.57,11.45,1300256)
    ,('2018/4/16',11.47,11.47,11.1,11.03,1427072.75)
    ,('2018/4/17',11.12,11.45,11.21,11.11,1301891.62)
    ,('2018/4/18',11.45,11.61,11.5,11.28,1475845.25)
    ,('2018/4/19',11.52,11.69,11.47,11.42,849131.81)
    ,('2018/4/20',11.51,11.58,11.35,11.2,958690.62)
    ,('2018/4/23',11.3,11.61,11.57,11.26,1070289.38)
    ,('2018/4/24',11.63,11.94,11.86,11.58,1461098.88)
    ,('2018/4/25',11.76,11.81,11.68,11.63,730286.5)
    ,('2018/4/26',11.66,11.69,11.42,11.31,874235.94)
    ,('2018/4/27',11.49,11.51,10.85,10.63,2709795.75)
    ,('2018/5/2',10.97,11.03,10.88,10.8,1190523.25)
    ,('2018/5/3',10.86,10.88,10.75,10.57,1281355.62)
    ,('2018/5/4',10.73,10.83,10.68,10.66,710509.5)
    ,('2018/5/7',10.7,10.83,10.81,10.64,974309.69)
    ,('2018/5/8',10.83,11.15,11.01,10.8,1373305.62)
    ,('2018/5/9',10.98,11.03,10.97,10.88,627656.12)
    ,('2018/5/10',11.03,11.09,11.01,10.91,552735.88)
    ,('2018/5/11',11.04,11.13,11.01,10.96,772369.69)
    ,('2018/5/14',11.09,11.23,11.18,11.03,1039297.12)
    ,('2018/5/15',11.18,11.19,11.12,11.02,669261.44)
    ,('2018/5/16',11.07,11.07,10.9,10.89,714362.06)
    ,('2018/5/17',10.91,10.94,10.82,10.78,586494.38)
    ,('2018/5/18',10.81,10.97,10.96,10.76,578384.75)
    ,('2018/5/21',11.07,11.11,10.95,10.93,763533.62)
    ]
        
    kks = [];
    for k in ks : kks.append(tt.K(k[0],k[1],k[2],k[3],k[4],k[5]));
    #import pdb; pdb.set_trace()
    ds.StickWidget(p,kks,fill=False)

    #uc = norm.NormalizeUseCase(kks)    
    #res = uc.execute()
    
    
    app.exec_()
