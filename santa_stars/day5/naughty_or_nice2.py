#!/usr/bin/env python

# From adventofcode.com

# Who is naughty or nice

# A nice string is one with all of the following properties:

# Now, a nice string is one with all of the following properties:

# - It contains a pair of any two letters that appears at least twice in
#   the string without overlapping, like xyxy (xy) or aabcdefgaa (aa), 
#   but not like aaa (aa, but it overlaps).
# - It contains at least one letter which repeats with exactly one letter 
#   between them, like xyx, abcdefeghi (efe), or even aaa.

def isNice():
  with open('input.txt', 'r') as f:
    nice_list = []
    count = 0
    for l in f:
      criteria1 = False
      criteria2 = False
      match1 = ''
      match2 = ''
      for i in range(0,len(l)-2):
        if l[i] == l[i+2]:
          criteria1 = True
          match1 = l[i]+l[i+1]+l[i+2]
      for i in range(0, len(l)-1):
        for j in range(i+2, len(l)-1):
          if str(l[i]+l[i+1]) == str(l[j]+l[j+1]):
            criteria2 = True
            match2 = l[i]+l[i+1]
      if criteria1 == True and criteria2 == True:
        nice_list.append(l)
    print 'number of nice words: ' + str(len(nice_list))

def main():
  isNice()

if __name__ == "__main__":
    main()
