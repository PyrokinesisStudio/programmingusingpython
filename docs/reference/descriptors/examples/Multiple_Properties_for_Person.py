from collections import OrderedDict

########
 
class Property(object):
    def __init__(self, name, description):
        self._name = name
        self._description = description

    def __set__(self, inst, value):
        if inst is None:
            return self
        
        props = inst.__dict__.setdefault('_props', OrderedDict())
        props[self._name] = value

    def __get__(self, inst, cls):
        if inst is None:
            return self
        
        props = inst.__dict__.setdefault('_props', OrderedDict())
        
        return props.get(self._name, None) or self._default

    
    def resetValue(self, inst):
        props = inst.__dict__.get('_props', None)
        
        if not props:
            raise ValueError("No properties have been ever initialized")
        
        if not props.get(self._name, None):
            raise ValueError("Property has never been initialized")
        
        if not isinstance(self, PropertyHasDefaultValue):
            raise ValueError("Property cannot have a default value, so cannot reset to default")
        
        props[self._name] = self._default

print Property

########

class PropertyHasDefaultValue(object):
    def __init__(self, default):
        self._default = default

print PropertyHasDefaultValue

########

class IntProperty(Property, PropertyHasDefaultValue):
    def __init__(self, name, description, default):
        super(IntProperty, self).__init__(name, description)
        PropertyHasDefaultValue.__init__(self, default)

print IntProperty

########


class StringProperty(Property):
    def __init__(self, name, description):
        super(StringProperty, self).__init__(name, description)

print StringProperty

########

class PropertiesBasedMixin():
    def resetToDefaults(self):
        print "\nResetting person's properties to default values\n"

        instance_properties = self.__dict__['_props']

        for prop_name in instance_properties:
            prop = self.__class__.__dict__[prop_name]
            print prop._name, instance_properties[prop_name]
            try:
                prop.resetValue(self)
            except ValueError as e:
                print "\t", e
            else:
                print "\t", prop._name, instance_properties[prop_name]

print PropertiesBasedMixin

########

class Person(object, PropertiesBasedMixin):
    name = StringProperty("name", "Name of the person")
    age = IntProperty('age', "Age of the person", -1)
    degrees = IntProperty('degrees', "Number of degrees held by this person", 0)
    
    def __init__(self, name):
        self.name = name

print Person

########

print Person.name._description
print Person.age._name
print Person.age._description

#########

person1 = Person("Bugs Bunny")

print person1.__dict__

person1.age = 30
person1.degrees = 10000L

print person1.__dict__

########

person2 = Person("Daffy Duck")

print person2.__dict__

try:
    Person.name.resetValue(person2)
except ValueError as e:
    print e

print person2.name
print person2.age
print person2.degrees

person2.age = 35
person2.degrees = 2

print person2.__dict__

person2.resetToDefaults()

print person2.__dict__

########

"""

>>> (executing line 1 of "Person.py")

>>> (executing lines 4 to 40 of "Person.py")
<class '__main__.Property'>

>>> (executing lines 43 to 48 of "Person.py")
<class '__main__.PropertyHasDefaultValue'>

>>> (executing lines 51 to 57 of "Person.py")
<class '__main__.IntProperty'>

>>> (executing lines 60 to 66 of "Person.py")
<class '__main__.StringProperty'>

>>> (executing lines 69 to 86 of "Person.py")
__main__.PropertiesBasedMixin

>>> (executing lines 89 to 98 of "Person.py")
<class '__main__.Person'>

>>> (executing lines 101 to 104 of "Person.py")
Name of the person
age
Age of the person

>>> (executing lines 107 to 115 of "Person.py")
{'_props': OrderedDict([('name', 'Bugs Bunny')])}
{'_props': OrderedDict([('name', 'Bugs Bunny'), ('age', 30), ('degrees', 10000L)])}

>>> (executing lines 118 to 139 of "Person.py")
{'_props': OrderedDict([('name', 'Daffy Duck')])}
Property cannot have a default value, so cannot reset to default
Daffy Duck
-1
0
{'_props': OrderedDict([('name', 'Daffy Duck'), ('age', 35), ('degrees', 2)])}

Resetting person's properties to default values

name Daffy Duck
	Property cannot have a default value, so cannot reset to default
age 35
	age -1
degrees 2
	degrees 0
{'_props': OrderedDict([('name', 'Daffy Duck'), ('age', -1), ('degrees', 0)])}

>>> 
"""
