def cheese_and_crackers(cheese_count, boxes_of_crackers):
  print "You have %d cheeses!" % cheese_count
  print "You have %d boxes of crackers!" % boxes_of_crackers

print "We can just give the function numbers directly"
cheese_and_crackers(20, 30)

print "OR, we can use varialbes in our script:"
amount_of_cheese = 10
boxes_of_crackers = 50

cheese_and_crackers(amount_of_cheese, boxes_of_crackers)

print "Math also"
cheese_and_crackers(10+20, 5+6)

print "Combine variables and math"
cheese_and_crackers(amount_of_cheese + 100, boxes_of_crackers + 10000)

