#
# task00 : 
#
#
#
#
#


import numpy as np
import pandas as pd
import argparse

#----------------------------------------------------------
def task00(inputFile0, inputFile1, outputFile):

    #current file
    t00 = pd.read_excel(inputFile1, sheetname="원본", header = 2) 

    c00 = t00["원가통계비목"] == "[ 세 부 항 목 소 계 ]"
    c01 = t00["세부사업"] == "[ 총      계 ]"
    t01 = t00[c00 | c01]

    a00 = (t00["세부사업"]    != "[ 단 위 사 업 합 계 ]") & (t00["세부사업"] != "[ 정 책 사 업 합 계 ]")   
    a01 = (t00["세부항목"]    != "[ 세 부 사 업 소 계 ]")
    a02 = (t00["원가통계비목"] != "[ 세 부 항 목 소 계 ]")
    t04 = t00[(a00 & a01 & a02)]

    #t02
    t02 = t01[["세부사업", "세부항목","예산현액(A)", "지급액(C)","집행률(C/A)"]]
    t02["예산현액(A)"] = [ np.int(np.ceil(x/1000)) for x in t02["예산현액(A)"]]
    t02["지급액(C)"] = [ np.int(np.ceil(x/1000)) for x in t02["지급액(C)"]]
    avg = t02[c01]["집행률(C/A)"]
    
    #previous file
    p00 = pd.read_excel(inputFile0, sheetname="원본", header = 2) 

    c00 = p00["원가통계비목"] == "[ 세 부 항 목 소 계 ]"
    c01 = p00["세부사업"] == "[ 총      계 ]"
    p01 = p00[c00 | c01]

    p02 = p01[["세부사업", "세부항목","예산현액(A)", "지급액(C)","집행률(C/A)"]]
    p02["예산현액(A)"] = [ np.int(np.ceil(x/1000)) for x in p02["예산현액(A)"]]
    p02["지급액(C)"]   = [ np.int(np.ceil(x/1000)) for x in p02["지급액(C)"]]

    t02["지급액(C+)"]   =  np.array(t02["지급액(C)"])   - np.array(p02["지급액(C)"])
    t02["집행률(C/A+)"] =  np.array(t02["집행률(C/A)"]) -  np.array(p02["집행률(C/A)"])

    t03 = t02[t02["집행률(C/A)"] <= np.float(avg) ]

    with pd.ExcelWriter(outputFile, mode='w', engine='openpyxl') as writer:
        t01.to_excel(writer, sheet_name="세부사업정리", header=True, index=False)
        t02.to_excel(writer, sheet_name="천원단위", header=True, index=False)
        t03.to_excel(writer, sheet_name="집행률이하", header=True, index=False)
        t04.to_excel(writer, sheet_name="DATA0", header=True, index=False)

#----------------------------------------------------------
def do_task00(args):
    task00(args.prev, args.curr, args.next)

#----------------------------------------------------------
def init_command():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    hello_parser = subparsers.add_parser('task00')
    hello_parser.add_argument('--prev', default="p.xlsx")
    hello_parser.add_argument('--curr', default="c.xlsx") 
    hello_parser.add_argument('--next', default="result.xlsx")
    hello_parser.set_defaults(func=do_task00)  # set the default function to hello

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    init_command()