#!/usr/bin/env python

# From adventofcode.com/day/1

# Find what floor Santa is on

# An opening parenthesis, (, means he should go up one floor,
# and a closing parenthesis, ), means he should go down one floor.

def findFloor():
  floor = 0
  count = 0
  with open('input.txt', 'r') as f:
    for line in f:
      for c in line:
        # print "floor: " + str(floor)
        count += 1
        if floor == -1:
          print "Santa's in the basement at position " + str(count-1) 
        if c == '(':
          floor += 1
        else:
          floor -= 1
  print "Sanata's floor: " + str(floor)
  print "Total floors traversed: " + str(count)

def main():
  findFloor()

if __name__ == "__main__":
    main()