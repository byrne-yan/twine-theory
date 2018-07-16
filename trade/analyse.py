import sys
import pandas as pd
from pathlib import Path

sys.path.append("..")
from twine_theory.domain import twine_theory as tt
import matplotlib.pyplot as plt

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage:analyse stock_file [show]")
        exit()
    stock = sys.argv[1]
    stockFile = Path(stock)
    if not stockFile.is_file():
        print("File %s not exists" % stock)
        exit()
    st = pd.read_csv(stock,parse_dates=['date'],dtype={'code':str},index_col='date')
    seq = tt.KSeq('day', st)

    dlist = [st.iloc[s['from'][0]].name for s in seq._bi] + [st.iloc[seq._bi[0]['to'][0]].name]

    stroke = pd.DataFrame(data=[s['from'][1] for s in seq._bi] + [seq._bi[-1]['to'][1]],index = dlist,columns=['storke'])

    dlist2 = [st.iloc[s['from'][0]].name for s in seq._segment] + [st.iloc[seq._segment[0]['to'][0]].name]
    segment = pd.DataFrame(data=[s['from'][1] for s in seq._segment] + [seq._segment[-1]['to'][1]],index = dlist2,columns=['sgement'])

    stroke.to_csv(stockFile.parent / (stockFile.stem + '_stroke.csv'),index=False)
    segment.to_csv(stockFile.parent / (stockFile.stem + '_segment.csv'),index=False)

    if(len(sys.argv)>=3):
        stroke.join(segment).interpolate(method ='index',limit_area='inside').plot()
        plt.show()
