class c1:
    def __init__(self,fac1):
        print('调用了c1的init')
        self.value1 = fac1
        pass
    def f1(self,str):
        print(str)

if __name__ == "__main__":
    a = c1('456')
    print(a)
    a.f1('123')
    print(a.value1)