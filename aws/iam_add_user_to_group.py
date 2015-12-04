#!/usr/bin/env python

import boto
import re
import argparse
import output

iam = boto.connect_iam()

username = ""
groups = []
groups_to_add = []

def getUsername(check=True):
	u = raw_input("Enter username:")
	if check:
		return checkUsername(u)
	else:
		return u

def checkUsername(u):
	user_data = iam.get_all_users()
	for user in user_data.users:
		if u == user['user_name']:
			global username
			username = u
			return username
	print("%s does not exist" % u)
	return getUsername()
	

def getGroups():
	group_data = iam.get_all_groups()
	i=0
	print('What group(s) would you like to add %s to? (enter number(s) separated by commas)' % username)
	for group in group_data.groups:
		i += 1
		groups.append(str(group['group_name']))
		print(str(i) + ')' + group['group_name'])

	group_selection = map(int, raw_input("Enter Selection: ").split(','))

	print("%s will be added to " % username)
	for x in group_selection:
		if x > len(groups) or x == 0:
			output.WARNING("You entered an incorrect number")
			getGroups()
		else:
			print(groups[x-1])
			groups_to_add.append(groups[x-1])

	return groups_to_add


def addToGroups(groups_to_add):
	print("Do you want to add %s to the following group(s)?" % username)
	for item in groups_to_add:
		print(item)
	answer = raw_input("y/n to continue:")
	if answer == 'y':
		for x in groups_to_add:
			if re.search(username, str(iam.get_group(x).users)):
				print('%s is already in %s' % (username, x))
			else:
				iam.add_user_to_group(x, username)
				print('added %s to %s' % (username, x) )
	else: 
		print("Terminating...")

def main():
	parser = argparse.ArgumentParser(description='Adds a user to group(s) in AWS IAM')
	parser.add_argument('--user', help="The user to be added to a group(s)")
	parser.add_argument('--group', help='The group(s) to add', nargs='*')

	args = parser.parse_args()
	global groups_to_add

	if args.user:
		global username
		username = args.user
		checkUsername(username)
	else:
		getUsername()

	if args.group:
		groups_to_add = [str(item) for item in args.group]
	else:
		getGroups()

	addToGroups(groups_to_add)

if __name__ == "__main__":
    main()
