import GlobalTest2
import ConfigTest

def main():
    foo = GlobalTest2.Foo()
    print("outside loop, test_var = " + str(ConfigTest.test_var))
    x = 0
    while x < 5:
        foo.update_variable()
        print("loop " + str(x) + ", test_var = " + str(ConfigTest.test_var))
        x += 1


if __name__ == '__main__':
    main()
    '''GlobalTest2.test = 2
    print("in main, test = " + str(GlobalTest2.test))

    foo = GlobalTest2.Foo()
    foo.print_variable()'''
