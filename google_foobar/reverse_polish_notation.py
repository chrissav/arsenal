#!/usr/bin/env python

import argparse

def answer(str):
  op = []
  output = []
  for i in str:
    if i.isdigit():
      output.append(i)
    elif i == '*' or i == '+':
      op.insert(0, i)
      op2 = []
      length = len(op)
      for j in range(0, length):
        if isGreater(i, op[j]) or i == op[j]:
          pass
        else:
          output.append(op[j])
          op2.append(op[j])
      for x in op[:]:
        if x in op2:
          op.remove(x)
    else:
      print('enter a correct string')
      exit(1)
  for o in op:
    output.append(o)

  print "".join(output)

def isGreater(i, j):
  if j == "":
    return True
  elif i == "*" and j =="+":
    return True
  else:
    return False

def main():
  parser = argparse.ArgumentParser(description='string')
  parser.add_argument('--string', help="string")
  args = parser.parse_args()

  answer(args.string)

if __name__ == "__main__":
    main()