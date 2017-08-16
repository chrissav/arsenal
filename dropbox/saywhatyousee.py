
#!/usr/bin/env python

import argparse

def say_what_you_see(input_strings):
    for s in input_strings:
        for i in range(0, len(s)):
            count = 1
            while s[i] == s[i+1]:
                count += 1
                i += 1
            print str(count) + str(s[i])

def findSubsets(lst):
    # the power set of the empty set has one element, the empty set
    result = [[]]
    for x in lst:
        result.extend([subset + [x] for subset in result])
    # get rid of empty subsets
    return result

def findMin(lst):
    min = lst[0]
    max = lst[0]
    max_sum = 0
    min_sum = 100
    for x in lst:
        if len(x) == 3:
            sum = 0
            for j in x:
                sum += int(j)
            if sum < min_sum:
                min = x
                min_sum = sum
            if sum > max_sum:
                max = x
                max_sum = sum
    print min
    print max

def main():
    parser = argparse.ArgumentParser(description="say what you see")
    parser.add_argument('--string', help='Add for dry run', nargs='*')
    args = parser.parse_args()

    findMin(findSubsets(args.string))

if __name__ == "__main__":
    main()
