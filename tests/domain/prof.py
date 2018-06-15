from line_profiler import LineProfiler
import pandas as pd
import sys

sys.path.append("../..")
from twine_theory.domain import twine_theory as tt


df = pd.read_csv("000001.csv")
df.sort_values('date')
profiler = LineProfiler()
s = tt.KSeq('day',[])
lp_wrapper = profiler(tt.KSeq.__init__)
lp_wrapper(s,'day',df)
profiler.print_stats()
