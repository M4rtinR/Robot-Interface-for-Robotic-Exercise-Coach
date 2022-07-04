import ConfigTest

class Foo:
    def __init__(self):
        print("Initialising Foo")

    def update_variable(self):
        ConfigTest.test_var += 1
        print("In Foo update_variable, test_var = " + str(ConfigTest.test_var))

    def print_variable(self):
        print("In Foo, test = " + str(ConfigTest.test_var))
