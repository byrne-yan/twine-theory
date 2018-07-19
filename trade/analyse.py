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

    dlist = [k['time'] for k in seq._seq]
    
    dlist1 = [st.iloc[s['from'][0]].name for s in seq._strokes] + [st.iloc[seq._strokes[-1]['to'][0]].name]
    stroke = pd.DataFrame(data=[s['from'][1] for s in seq._strokes] + [seq._strokes[-1]['to'][1]],index = dlist1,columns=['stroke'])
    stroke.to_csv(stockFile.parent / (stockFile.stem + '_stroke.csv'))

    if len(seq._segment) > 0:
        dlist2 = [st.iloc[s['from'][0]].name for s in seq._segment] + [st.iloc[seq._segment[-1]['to'][0]].name]
        segment = pd.DataFrame(data=[s['from'][1] for s in seq._segment] + [seq._segment[-1]['to'][1]],index = dlist2,columns=['segment'])

        segment.to_csv(stockFile.parent / (stockFile.stem + '_segment.csv'))

##    import pdb;pdb.set_trace()
    b = [ k['low'] for k in seq._seq]
    h = [ k['high']-k['low'] for k in seq._seq]
    
    fig,ax = plt.subplots(figsize = (10,5))
    ax.bar(dlist,height=h,width=0.8,bottom =b,align='center',color='grey')
    ax.plot(stroke,color='b')
    if len(seq._segment) > 0:
        ax.plot(segment,color='r')
    prev = None
    for stk in stroke.itertuples():
        if prev is not None:
            v = 5
            if prev.stroke > stk.stroke:
                v = -15
            ax.annotate(stk.stroke,xy=(stk.Index,stk.stroke),xytext=(0,v),ha='center', textcoords ='offset pixels')
        prev = stk
    plt.savefig(str(stockFile.parent / (stockFile.stem+'_draw.png')))
    if(len(sys.argv)>=3):
        #stroke.join(segment).interpolate(method ='index',limit_area='inside').plot()
        plt.show()
