#!/usr/bin/env python

# From adventofcode.com

def shortest_route():
  locations = {}
  with open('input.txt', 'r') as f:
    for l in f:
      items = l.split(' ')
      if items[0] in locations:
        locations[items[0]].append(items[2])
      else:
        locations[items[0]] = [items[2]]
    print locations
    for i in locations:
      for j in locations:
        print i
        print find_shortest_path(locations, i, j)
    # print find_shortest_path(locations, 'London', 'Belfast')

def find_shortest_path(graph, start, end, path=[]):
  path = path + [start]
  if start == end:
      return path
  if not graph.has_key(start):
      return None
  shortest = None
  for node in graph[start]:
      if node not in path:
          newpath = find_shortest_path(graph, node, end, path)
          if newpath:
              if not shortest or len(newpath) < len(shortest):
                  shortest = newpath
  return shortest

def main():
  shortest_route()

if __name__ == "__main__":
    main()
