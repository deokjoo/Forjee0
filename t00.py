import numpy  as np
import pandas as pd


####

fileI = "원본.xlsx"
fileO = "t01.xlsx"

t00 = pd.read_excel(fileI, sheetname="원본", header = 2) 

c00 = t00["원가통계비목"] == "[ 세 부 항 목 소 계 ]"
c01 = t00["세부사업"] == "[ 총      계 ]"
t01 = t00[c00 | c01]

t02 = t01[["세부사업", "세부항목","예산현액(A)", "지급액(C)","집행률(C/A)"]]
t02["예산현액(A)"] = [ np.int(np.ceil(x/1000)) for x in t02["예산현액(A)"]]
t02["지급액(C)"] = [ np.int(np.ceil(x/1000)) for x in t02["지급액(C)"]]

avg = t02[c01]["집행률(C/A)"]
t03 = t02[t02["집행률(C/A)"] < np.float(avg) ]


with pd.ExcelWriter(fileO, mode='a', engine='openpyxl') as writer:
  t01.to_excel(writer, sheet_name="세부사업정리", header=True, index=False)
  t02.to_excel(writer, sheet_name="천원단위", header=True, index=False)
  t03.to_excel(writer, sheet_name="집행률이하", header=True, index=False)
