#!/usr/bin/env python

# From adventofcode.com

# Find the lowest integer that combines with the input string
# that will produce a md5 hash starting with five or six zeroes

import md5

def mine(s):
  h = md5.new(s)
  good_hash = 0
  while not h.hexdigest().startswith('000000'):
    good_hash += 1
    h = md5.new(s+str(good_hash))
  print 'md5 hash: ' + str(h.hexdigest())
  print 'answer: ' + str(good_hash)

def main():
  mine('iwrupvqb')

if __name__ == "__main__":
    main()