import numbers as n

nama = "nathan"
umur_5_tahun_lalu = 23
print ("nama saya")
print(nama)
print("sedangkan umur saat ini adalah")
print(umur_5_tahun_lalu + 5)
a=0



tuplea = ("azmi",19,"South Tangerang",True,[1,2,3,4,5,6,7,8,9,10])

for i in tuplea[4]:
    print("yes",end='')
    if i == 7:
        break
print()
def greet(name):
    """
    This function greets to
    the person passed in as
    a parameter
    """
    print("Hello, " + name + ". Good morning!")
    return("???")

greet('Asprak')

print(greet('Asprak'))

print()
class Person:
    def __init__(mysillyobject, name, age):
        mysillyobject.name = name
        mysillyobject.age = age


    def myfunc(abc):
        print("Hello my name is " + abc.name)

p1 = Person("Azmi", 19)
p1.myfunc()

print()

for i in ("Azmi Ganteng"):
    if i == 'z':
        continue
    print(i, end='')


print()
print()
benar = True
benar = not benar

if (benar):
    print("(check not) Benar")
else: 
    print("(check not) Salah")



if (True or False == True):
    print("(check or) benerr")
else:
    print("(check or) salahhh")


def reciprocal(num):
    try:
        r = 1/num
    except:
        print('Exception caught')
        return
    return r
    

print(reciprocal(10))
print(reciprocal(0))



num = 10
x = num
greg = "name"

lista = ["dog"]
listb = [1, "lol", greg]
listc = [[x for x in lista] for y in lista]

tupa = ()
tupb = (2, greg, "kek")

dicta = {}
dictb = {"a": 10, greg: "b", 10: num}

while True:
    break

""" Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Cras ut urna erat. Nam mollis justo turpis, sed egestas nisi gravida
tristique. Nam in tristique lacus. Suspendisse sed metus at lacus
ullamcorper gravida. Nullam dictum quam a volutpat lacinia. Phasellus
volutpat cursus lectus, in suscipit leo efficitur nec. Quisque
vitae commodo lorem. Donec suscipit tellus nec eleifend convallis.
Sed leo metus, convallis eget tortor sed, sollicitudin malesuada
ante. Sed facilisis felis id tortor bibendum, et venenatis massa
fermentum. Maecenas magna ligula, tempor eu ligula eu, dignissim
sagittis purus. Pellentesque a dignissim enim. Sed vestibulum feugiat
dui vitae placerat. Cras sapien arcu, tempor ac pulvinar quis,
mattis eget nulla. Fusce non vehicula eros. In hac habitasse platea
dictumst.
"""


x = -1

if x < 0:
  raise Exception("Sorry, no numbers below zero")







