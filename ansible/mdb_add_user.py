#!/usr/bin/env python

import subprocess
import argparse
import sys
import set_bastion_user


def writePlaybook():
    print("Writing playbook...")
    playbook = open("playbook_mdb_add_user.yaml", "w+")
    playbook.write('%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n' %
                   (
                       '- name: Create MDB and User',
                       '  hosts: ~tag_Environment_' + args.env + ':&tag_Component_mongo:&tag_stack_' + args.stack,
                       '  gather_facts: False',
                       '  tasks:',
                       '    - name: Install pymongo',
                       '      pip: name=pymongo',
                       '      sudo: yes',
                       '    - name: Create DB and User',
                       '      mongodb_user: database=' + args.program.replace('-', '_') + '_' + args.app + '_' + args.env + ' replica_set=mt_' + args.env + ' user=' + args.user + ' password=' + args.password + ' roles="readWrite" state=' + state,
                       '    - name: Uninstall pymongo',
                       '      pip: name=pymongo state=absent',
                       '      sudo: yes'))


class Parser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser = Parser(description='Adds a user and password to a MDB')
parser.add_argument(
    '-env', choices=['test', 'stg', 'prod'],
    help="Set the environment to use (e.g. test, stg, prod)",
    required=True
)
parser.add_argument('-program', help="The program in which to add the user", required=True)
parser.add_argument('-user', help="User to be added to the database", required=True)
parser.add_argument('-password', help="Password for new user", required=True)
parser.add_argument('-stack', help="e.g. mt01, test", required=True)
parser.add_argument('-app', help="e.g. oars, api", required=True)
parser.add_argument('-local', help="Add this flag if you are running the script locally and not on Jenkins", action='store_true')
parser.add_argument('-C', help="Add this flag for a dry run", action='store_true')
parser.add_argument('-remove', help="Add this flag to remove the user", action='store_true')
args = parser.parse_args()

if args.local:
  set_bastion_user.main(args.env)

if args.remove:
  state='absent'
else:
  state='present'

writePlaybook()

if args.C:
  subprocess.call(["ansible-playbook", "../mdb/playbook_mdb_add_user.yaml",
                   "-i", "plugins/inventory/ec2.py", "-T", "30", "-C"],
                  cwd='../ansible')
else:
    subprocess.call(["ansible-playbook", "../mdb/playbook_mdb_add_user.yaml",
                   "-i", "plugins/inventory/ec2.py", "-T", "30"],
                  cwd='../ansible')
