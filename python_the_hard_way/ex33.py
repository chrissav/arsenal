i = 0
numbers = []

def loopItGood(num):
  i = 0
  numbers = []
  while i < num:
    print "At the top i is %d" % i
    numbers.append(i)

    i = i + 1
    print "Numbers now: ", numbers
    print "At the bottom i is %d" % i

  print "The numbers: "

  for num in numbers:
    print num

loopItGood(7)
