#!/usr/bin/env python

import argparse

def answer(str):
	for i in str:
		print i

def main():
	parser = argparse.ArgumentParser(description='Description of script')
	parser.add_argument('s', '--string', help="string")
	args = parser.parse_args()

	answer(args.string)

if __name__ == "__main__":
    main()
