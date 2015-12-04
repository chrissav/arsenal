#!/usr/bin/env python

# From adventofcode.com/day/1

# How much wrapping paper is needed?

# find the surface area of the box, which is 2*l*w + 2*w*h + 2*h*l.
# The elves also need a little extra paper for each present: the area of the smallest side.
# Example:
# A present with dimensions 2x3x4 requires 2*6 + 2*12 + 2*8 = 52 square
# feet of wrapping paper plus 6 square feet of slack, for a total of 58 square feet.

import heapq

def wrappingPaper():
  sq_ft = 0
  ribbon_sq_ft = 0
  with open('input.txt', 'r') as f:
    for line in f:
      length, width, height = map(int, line.split('x'))
      # Print the equations:
      # print "(2*" + str(length) + '*' + str(width)+ ')+(2*' + str(width) + '*' + str(height) + ')+(2*' + str(height) + '*' + str(length)+ ')+(' + str(heapq.nsmallest(2, [length,width,height])[0]) + '*' + str(heapq.nsmallest(2,[length,width,height])[1]) + ')'
      first_smallest, second_smallest = heapq.nsmallest(2, [length,width,height])
      ribbon_sq_ft += (length*width*height)+(first_smallest+first_smallest+second_smallest+second_smallest)
      sq_ft += (2*length*width)+(2*width*height)+(2*height*length)+(first_smallest*second_smallest)
  print "Santa needs: " + str(sq_ft) + " sq ft. of wrapping paper and " + str(ribbon_sq_ft) + " ft. of ribbon"


def main():
  wrappingPaper()

if __name__ == "__main__":
    main()