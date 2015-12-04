#!/usr/bin/env python

import argparse

def answer(str):
	for i in str:
		print i

def main():
	parser = argparse.ArgumentParser(description='Adds a user to group(s) in AWS IAM')
	parser.add_argument('--string', help="string")
	args = parser.parse_args()

	answer(args.string)

if __name__ == "__main__":
    main()