import simpleStat as sStat

l=[100,34,22,9,7,56,99,144]
#l=[100,34]
avg=sStat.AvgCleanList(l)
med=sStat.MedianList(l)

if avg[0]==0:
    print("gemiddelde van lijst is ",avg[1])
else:
    print("fout - kan gemiddelde niet berekenen")

l=[100,34,22,9,7,56,99,144]
if med[0]==0:
    print("mediaan van lijst is ",med[1])
else:
    print("fout - kan mediaan niet berekenen")
