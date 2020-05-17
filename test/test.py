import datetime
import random

class test():

    def __init__(self):
        pass

    def test_func(self):
        foo = ['a', 'b', 'c', 'd', 'e']
        print(random.choice(foo))

        print(type('1585198800000'))
        timestrampL = float('1585198800000')/1000
        print(timestrampL)
        print(datetime.datetime.fromtimestamp(timestrampL).strftime('%Y-%m-%d %H:%M:%S'))


        str = ' ss  s '
        print(str.strip())
        # print(datetime.datetime.now().strftime("%Y%m%d"))
        liveTime = "2020-03-26 12:23:22"
        ddd = datetime.datetime.strptime(liveTime, '%Y-%m-%d %H:%M:%S')
        print(type(ddd))
        print(ddd.strftime('%Y%m%d'))

        pre_dte_str = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y%m%d')

        live_dte_str = datetime.datetime.strptime('2020-03-25 12:33:22', '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')

        print(pre_dte_str == live_dte_str)

if __name__ == '__main__':
    test = test()
    test.test_func()