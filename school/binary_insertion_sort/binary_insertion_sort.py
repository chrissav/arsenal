#!/usr/bin/env python

import argparse
import math

students = []

def binaryInsertionSort(unsorted_list):
  for i in xrange(1, len(unsorted_list)):
    if unsorted_list[i] > unsorted_list[i-1]:
      continue
    else:
      minIndex, maxIndex = 0, i
      while minIndex < maxIndex:
        pivot = minIndex + int(math.floor(((maxIndex-minIndex) / 2)))
        if unsorted_list[i] > unsorted_list[pivot]:
          minIndex = pivot + 1
        else:
          maxIndex = pivot
      unsorted_list.insert(minIndex, unsorted_list.pop(i))
  return unsorted_list

def getStudents():
  ids = []
  print "Unsorted Student List: "
  with open('students.txt', 'r') as f:
    for line in f:
      print line.strip('\n')
      students.append(line)
      ids.append(line.split(',')[0])
  ids = map(int,ids)
  print "Unsorted ID list: " + str(ids)
  return ids

def printSortedList(sorted_ids):
  f = open('sorted_students.txt', 'w+')
  f.write("Sorted Student List\n")
  print "\nSorted Student List"
  for i in sorted_ids:
    for s in students:
      if i == int(s.split(',')[0]):
        print s.strip('\n')
        f.write(s)
  f.close()
  print "Sorted ID list: " + str(sorted_ids)

def main():
  parser = argparse.ArgumentParser(description='Sorts a list with binary insertion sort algorithm.  If an array is provided as a command line arguement it will sort that array.  If not, it will sort items listed in a file called students.txt')
  parser.add_argument('-l', '--list', nargs='+', help='<Required> Set flag')
  args = parser.parse_args()

  if args.list:
    ids = map(int,args.list)
    print binaryInsertionSort(ids)
  else:
    printSortedList(binaryInsertionSort(getStudents()))

if __name__ == "__main__":
    main()