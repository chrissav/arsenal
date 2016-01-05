## Animal is-a object (yes, sort of confusing) look at the extra credit
class Animal(object):
  pass

## Dog is-a Animal. has an __init__ function with self and name as parameters which sets the attribute name to the name parameter given
class Dog(Animal):
  def __init__(self, name):
    ## self has-a name
    self.name = name

## Cat is-a animal
class Cat(Animal):
  
  def __init__(self, name):
    ##Cat has-a name
    self.name = name

## Person is-a object
class Person(object):
  def __init__(self, name):
    ##Person has-a name
    self.name = name

    ## person has-a pet of some kind
    self.pet = None

##Employee is-a Person
class Employee(Person):

  def __init__(self, name, salary):
    ##person has-a Employee of itself that calls the __init__ function with the name parameter
    super(Employee, self).__init__(name)
    ##Employee has-a salary
    self.salary = salary

##Fish is-a object:
class Fish(object):
  pass

##Salmon is-a fish
class Salmon(Fish):
  pass

##Halibut is a fish
class Halibut(Fish):
  pass

##rover is a Dog
rover = Dog("Rover")

## satan is a Cat
satan = Cat("Satan")

##mary is a person
mary = Person("Mary")

##mary has-a pet which is the object satan
mary.pet = satan

##frank is-a Employee with the name Frank and salary 120,000
frank = Employee("Frank", 120000)

##frank has a pet which is the object rover
frank.pet = rover

##flipper is-a new Fish object
flipper = Fish()

##crouse is a new Salmon object
crouse = Salmon()

##harry is a new Halibut object
harry = Halibut()
