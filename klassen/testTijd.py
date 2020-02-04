from tijd import localTime

lt = localTime(+1, False)

res = lt.startInternetTime()

if res[0] == 0:
    print('locale tijd is %s'%lt.getLocalTime()[1])