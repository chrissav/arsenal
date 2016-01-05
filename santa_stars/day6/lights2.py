#!/usr/bin/env python

# From adventofcode.com

# Christmas light decorating contest
# How many lights are turned on?

def lights():
  with open('input.txt', 'r') as f:
    lights = [[0 for x in range(1000)] for x in range(1000)] 
    for line in f:
      l = line.split(' ')
      if l[0] == 'turn':
        action = l[1]
        start = l[2]
      else:
        action = l[0]
        start = l[1]
      end = l[-1]
      for x in range(int(start.split(',')[0]),int(end.split(',')[0])+1):
        for y in range(int(start.split(',')[1]),int(end.split(',')[1])+1):
          if action == 'toggle':
            lights[x][y] += 2
          elif action == 'on':
            lights[x][y] += 1
          else:
            if lights[x][y] > 0:
              lights[x][y] -= 1
    count = 0
    for x in range(0,1000):
      for y in range(0,1000):
        count += lights[x][y]
        print lights[x][y]
    print 'Total light power: ' + str(count)
def main():
  lights()

if __name__ == "__main__":
    main()
