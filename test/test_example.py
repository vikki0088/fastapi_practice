import pytest

def test_equal_or_not():
    assert 3 == 3


def test_is_instance():
    assert isinstance("hello",str)


# validate bool
def test_boolean():
    validate = True
    assert validate is True
    assert ("hello" == "world") is False

def test_type():
    assert type('hello' is str)
    assert type('world' is not int)

class Student:
    def __init__(self,name,age,stream):
        self.name = name
        self.age = age
        self.stream = stream

@pytest.fixture()
def default_student():
    return Student("vishnu", 25, "cse")



def test_student(default_student):
    assert default_student.name == 'vishnu'
    assert default_student.age == 25