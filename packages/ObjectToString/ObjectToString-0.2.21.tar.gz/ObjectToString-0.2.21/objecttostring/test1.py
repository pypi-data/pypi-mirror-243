# -*- coding: GBK -*-
import  sys
import time
import pglib


class a:
    def __init__(self):
        #self.con = psycopg2.connect(dbname='pds', user='postgres', password='123456', host='127.0.0.1')
        #self.cur = self.con.cursor()
        pass
    def getcon(self):
        #return self.con
        pass
    def run(self):
        return 6666
        pass
#print( demo.add( 1, 2 ) )
th=[]
thradnum=1
for i in range(thradnum):
    cc1=pglib.pglibconn("127.0.0.1",5432,'pds', 'postgres', '123456',i)
    print(cc1)
    while 1:
        if pglib.getthreadstatus(cc1)==-3:
            print(str(pglib.getMessage(cc1)))
        elif pglib.getthreadstatus(cc1)>0:
             break
        time.sleep(1)
    if cc1!=-1:
        th.append(i)


for i in th:
    print(pglib.pglibselect("SELECT * FROM \"public\".\"test\" LIMIT 10",i))
l=[]
thradnum_real=len(th)
for i in range(5000):
    l.append("insert into  test (tt,bb) values(1,'你好')")
    l.append("insert into  test (tt,bb) values(1,'你好')")

for i in th:
    if i!=-1:
        print(pglib.pglibinsert(l,i))
#print(pglib.pglibselect("SELECT * FROM \"public\".\"test\" LIMIT 1",cc))
print(666)
while 1:
    time.sleep(1)
    lex = []
    for tt in th:
        print(666)
        #print("status :%d" % pglib.getthreadstatus(tt))
        if pglib.getthreadstatus(tt)==2:
            lex.append(tt)
        print(666)
    if lex.__len__()==thradnum_real:
        break

for i in th:
    pglib.pglibclose(i)

for i in range(thradnum):
    cc1 = pglib.pglibconinsert("127.0.0.1", 5432, 'pds', 'postgres', '123456',l,i)
    print(cc1)
    while 1:
        if pglib.getthreadstatus(cc1) == -3:
            print(str(pglib.getMessage(cc1)))
        elif pglib.getthreadstatus(cc1) > 0:
            break
        time.sleep(1)
    if cc1 != -1:
        th.append(i)

#b=a()
#a1=demo.startthread( "3",a, thread=progress)
#print(a1)
'''
for i in range(2):
    #(demo.thread_lock())
    #dddd=demo.get_threadstatus(a1)
    #print(dddd)
    print(99999999)
    time.sleep(1)
    pass
    #(demo.thread_unlock())
print(111)

'''