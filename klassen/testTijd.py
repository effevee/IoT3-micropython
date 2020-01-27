from tijd import localTime

lt = localTime(+1, True)

res = lt.startInternetTime()

if res[0] == 0:
    print('locale tijd is %s'%lt.getLocalTime()[1])