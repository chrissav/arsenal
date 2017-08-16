#!/usr/bin/env python

"""Mostly a direct translation of the update.sh script

Changes:
  - adds/removes users listed in groups/[group-name]/users.txt
    to the IAM group
  - a dryrun option is available
  - removes policies found that aren't managed here
  - searches the "resources" directory for all IAM resources.
"""

import boto
import argparse
import os
from blessings import Terminal

iam = boto.connect_iam()
t = Terminal()

def check_for_dryrun(func):
  """Decorator to handle boto calls when --dryrun is passed."""
  def dryrun_func(*args, **kwargs):
    global dryrun
    if dryrun:
      print t.green("Dryrun: %s %s" % (func.__name__, " ".join(args)))
    else:
      return func(*args, **kwargs)
  return dryrun_func

@check_for_dryrun
def create_item(item, name):
  """Calls boto's iam.create_* function for whichever item is passed"""
  try:
    eval("iam.create_%s('%s')" %(item,name))
    print t.green("Success: Created %s: %s" %(item,name))
  except Exception, e:
    if e.status == 409:
      pass
    else:
      print t.red("Failure: %s:%s" %(name,e.message))

def find_and_add_policies(item, name, path):
  """Finds the policies in the item's directory and calls add_policies."""
  policies_in_list = []

  if item == 'group':
    function = 'get_all_group_policies'
  else:
    function = 'list_role_policies'
  try:
    policies_in_iam = eval("iam.%s('%s')['list_%s_policies_response']['list_%s_policies_result']['policy_names']" %(function,name,item,item))
  except:
    policies_in_iam = []

  root, dirs, files = os.walk(path).next()
  for file in files:
    if file.endswith('.json'):
      policies_in_list.append(file.rsplit('.',1)[0])
      add_policy(item, name, file, root)

  for policy in find_complement(policies_in_iam, policies_in_list):
    remove_policy(item,name,policy)

@check_for_dryrun
def add_policy(item,name,file,root):
  """Adds policies to a group or role."""
  try:
    eval("iam.put_%s_policy('%s', file.rsplit('.',1)[0], open(os.path.join(root,file)).read())" %(item,name))
    print t.green("Success: Added %s to %s" %(file, name))
  except Exception, e:
    print t.red("Failure: %s:%s" %(file, e.message))

@check_for_dryrun
def remove_policy(item,name,policy):
  """Removes policies from a group or role."""
  try:
    eval("iam.delete_%s_policy(name, policy.rsplit('.',1)[0])" %(item))
    print t.yellow("Warning: Removed %s from %s" %(policy, name))
  except Exception, e:
    print t.red("Failure: %s:%s" %(name, e.message))

@check_for_dryrun
def add_user_to_group(group, user):
  """Adds user to group."""
  try:
    iam.add_user_to_group(group, user.rstrip())
    t.green("Success: Added %s to %s" %(user, group))
  except Exception, e:
    print t.red("Failure: %s:%s" %(group, e.message))

@check_for_dryrun
def remove_user_from_group(group, user):
  """Removes user from group."""
  try:
    iam.remove_user_from_group(group, user.rstrip())
    t.green("Success: Removed %s from %s" %(user, group))
  except Exception, e:
    print t.red("Failure: %s:%s" %(group, e.message))

@check_for_dryrun
def update_trust_policy(role, trust_policy):
  """Updates the trust policy for a group or role."""
  try:
    iam.update_assume_role_policy(role, trust_policy)
    print t.green("Success: Updated trust policy")
  except Exception, e:
    print t.red("Failure: %s:trust policy - %s" %(role, e.message))

@check_for_dryrun
def create_instance_profile(profile):
  """Creates and attaches an instance profile to a role."""
  try:
    iam.create_instance_profile(profile)
    iam.add_role_to_instance_profile(profile, profile)
    print t.green("Success: Created and attached Instance Profile: %s" %profile)
  except Exception, e:
    if e.status == 409:
      pass
    else:
      print t.red("Failure: %s:%s" %(profile,e.message))

def find_complement(a, b):
  return list(set(a) - set(b))

def update_groups(group_path):
  """Updates a group's policies and users."""
  group = group_path.split('/')[-1]

  print t.bold("\nUpdating Group: %s" %group)

  create_item('group', group)
  find_and_add_policies('group', group, group_path)

  # compare user lists in file and IAM, and remove/add as necessary
  try:
    user_list = iam.get_group(group)['get_group_response']['get_group_result']['users']
  except:
    user_list = []
  users_in_iam = []
  for user in user_list:
    users_in_iam.append(user['user_name'])

  users_in_list = []
  if os.path.exists(os.path.join(group_path,'users.txt')):
    with open(os.path.join(group_path, 'users.txt')) as user_file:
      for user in user_file:
        users_in_list.append(user.rstrip())
    for user in find_complement(users_in_list, users_in_iam):
      add_user_to_group(group, user.rstrip())
    for user in find_complement(users_in_iam, users_in_list):
      remove_user_from_group(group, user.rstrip())
  else:
    print t.yellow("Warning: No users file was found for group: %s" %group)

def update_roles(role_path):
  """Updates a role's policies and users."""

  role = role_path.split('/')[-1]
  trust_policy = open("%s/trust/trust.json" %role_path).read()

  print t.bold("\nUpdating Role: %s" %role)

  create_item('role', role)
  find_and_add_policies('role', role, role_path)
  update_trust_policy(role, trust_policy)

def update_profiles(profile_path):
  """Updates an instance profile's policies and users."""

  profile = profile_path.split('/')[-1]
  trust_policy = open("%s/trust/trust.json" %profile_path).read()

  print t.bold("\nUpdating Profile: %s" %profile)

  create_item('role', profile)
  find_and_add_policies('role', profile, profile_path)
  create_instance_profile(profile)
  update_trust_policy(profile, trust_policy)

def update_all():
  """ Updates all resources found in the relative path "./resources/*"."""
  for item in os.listdir('./resources/'):
    root, dirs, files = os.walk("./resources/%s" %item ).next()
    for resource in dirs:
      if "_%s" %item in resource:
        inner_root, inner_dirs, inner_files = os.walk(os.path.join(root,resource)).next()
        for resource in inner_dirs:
          eval("update_%s('%s')" %(item, os.path.join(inner_root,resource)))
      else:
        eval("update_%s('%s')" %(item, os.path.join(root,resource)))

def main():
  parser = argparse.ArgumentParser(description='Updates IAM resources')
  parser.add_argument('--dryrun',
    help="Pass this flag to see what would be updated.",
    action='store_true')

  args = parser.parse_args()
  global dryrun
  dryrun = args.dryrun

  if not os.path.exists("./resources/"):
    exit("The directory './resources/ was not found.")

  update_all()

if __name__ == "__main__":
    main()
