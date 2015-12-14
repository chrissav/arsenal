#!/usr/bin/env python

# From adventofcode.com

# How many presents does Santa deliver?

# Moves are always exactly one house to the
#  north (^), south (v), east (>), or west (<)
#  After each move, he delivers another present 
#  to the house at his new location.

def deliveries():
  houses = {}
  houses[0,0]=1
  robox, roboy = 0,0
  santax ,santay = 0,0
  santa_turn = True
  with open('input.txt', 'r') as f:
    for line in f:
      for c in line:
        if santa_turn == True:
          santa_turn = False
          if c == '^':
            santax += 1
          elif c == 'v':
            santax -= 1
          elif c == '<':
            santay -= 1
          elif c == '>':
            santay += 1
          houses[santax,santay] = 1
        else:
          santa_turn = True
          if c == '^':
            robox += 1
          elif c == 'v':
            robox -= 1
          elif c == '<':
            roboy -= 1
          elif c == '>':
            roboy += 1
          houses[robox,roboy] = 1
    print 'houses with at least one present: ' + str(len(houses))


def main():
  deliveries()

if __name__ == "__main__":
    main()
