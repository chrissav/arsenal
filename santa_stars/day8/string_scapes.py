#!/usr/bin/env python

# From adventofcode.com

def string_scapes():
  char_count = 0
  mem_count = 0
  with open('input.txt', 'r') as f:
    for l in f:
      line = l.strip()
      char_count += len(line)
      i = 0
      while i < len(line):
        if line[i] != "\\":
          mem_count += 1
          i += 1
        else:
          if line[i+1] == 'x':
            i += 1
            try:
              int(line[i+1], 16)
              i += 1
              try:
                int(str(line[i])+str(line[i+1]),16)
                i += 1
              except:
                pass
            except:
              pass
          else:
            mem_count += 1
            i += 2
      mem_count -= 2
  print (char_count-mem_count)

def string_scapes_to_string():
  char_count = 0
  expanded_count = 0
  with open('input.txt', 'r') as f:
    for l in f:
      new_string = ""
      new_string += '"'
      line = l.strip()
      char_count += len(line)
      i = 0
      while i < len(line):
        if line[i] == '"' or line[i] == '\\':
          new_string += '\\' + line[i]
          i += 1
        else:
          new_string += line[i]
          i += 1
      new_string += '"'
      expanded_count += len(new_string)
  print (expanded_count-char_count)

def main():
  string_scapes_to_string()

if __name__ == "__main__":
    main()
