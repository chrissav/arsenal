#!/usr/bin/env python

# From adventofcode.com

# Christmas light decorating contest
# How many lights are turned on?

signals = {}

def makeCircuit(commands):
  while commands:
    for cmd in commands:
      delete_commands = []
      s = cmd.split('->')[0]
      signal = s.split(' ')
      #remove last item bc it's empty
      signal.pop()
      end_wire = cmd.split('->')[1].strip('\n').strip(' ')
      # no op - single assignment
      if len(signal) == 1:
        if signal[0].isdigit():
          signals[end_wire] = signal[0]
          delete_commands.append(cmd)
        elif signal[0] in signals:
          signals[end_wire] = signals[signal[0]]
          delete_commands.append(cmd)
      # not operator
      elif len(signal) == 2:
        if signal[1].isdigit():
          signals[end_wire] = ~signal[1]
          delete_commands.append(cmd)
        elif signal[1] in signals:
          signals[end_wire] = ~int(signals[signal[1]])& 0xFFFF
          delete_commands.append(cmd)
      # all other ops
      else:
        left_op = ''
        right_op = ''
        if signal[0].isdigit():
          left_op = int(signal[0])
        elif signal[0] in signals:
          left_op = int(signals[signal[0]])
        if signal[2].isdigit():
          right_op = int(signal[2])
        elif signal[2] in signals:
          right_op = int(signals[signal[2]])
        if left_op != '' and right_op != '':
          if signal[1] == 'AND':
            signals[end_wire] = left_op & right_op
            delete_commands.append(cmd)
          elif signal[1] == 'OR':
            signals[end_wire] = left_op | right_op
            delete_commands.append(cmd)
          elif signal[1] == 'LSHIFT':
            signals[end_wire] = left_op << right_op
            delete_commands.append(cmd)
          elif signal[1] == 'RSHIFT':
            signals[end_wire] = left_op >> right_op
            delete_commands.append(cmd)
      for x in commands[:]:
        if x in delete_commands:
          commands.remove(x)
  print 'the signal on wire a is: ' + str(signals['a'])
    

def getCommands():
  commands = []
  with open('input.txt', 'r') as f:
    for line in f:
      commands.append(line)
  return commands

def main():
  makeCircuit(getCommands())

if __name__ == "__main__":
    main()
