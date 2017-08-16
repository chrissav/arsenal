
#!/usr/bin/env python

import argparse

def countBack():
    a = [[11, 2, 4], [4, 5, 6], [10, 8, -12]]
    for i in range(len(a), -1, -1):
        print(i)

def main():
    parser = argparse.ArgumentParser(description="say what you see")
    parser.add_argument('--string', help='Add for dry run', nargs='*')
    args = parser.parse_args()

    countBack()

if __name__ == "__main__":
    main()
