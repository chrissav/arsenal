#!/usr/bin/env python

import boto
import getpass
import argparse

tags = ""


def getUsername():
    username = str(getpass.getuser())
    return username

def setTest():
    environment = 'test'
    bastion = '2u-test-bast-test.2u.com'
    return bastion

def setStg():
    environment = "stg"
    bastion = "mt01-bast-stg.2u.com"
    return bastion

def setProd():
    environment = "prod"
    bastion = "mt01-bast-prod.2u.com"
    return bastion

def writeConfig(username, bastion):
    print("Writing ansible.cfg file...")
    ansible_cfg = open("../ansible/ansible.cfg", "w+")
    ansible_cfg.write('%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n' %
                      (
                          '[defaults]',
                          'fork=15',
                          'host_key_checking=False',
                          'record_host_keys=False',
                          '[ssh_connection]',
                          'ssh_args = -o ControlPersist=yes -F ssh.config -q',
                          'scp_if_ssh = True',
                          'control_path = ~/ansible/mux-%%r@%%h:%%p'))

    print("Writing ssh_config file...")
    ssh_config = open("../ansible/ssh.config", "w+")
    ssh_config.write('%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n' %
                     ('Host Bastion',
                      'User                   ' + username,
                      'HostName               ' + bastion,
                      'ProxyCommand           none',
                      'IdentityFile           ~/.ssh/id_rsa',
                      'BatchMode              yes',
                      'PasswordAuthentication no',
                      '\n',
                      'Host *',
                      'ServerAliveInterval    60',
                      'TCPKeepAlive           yes',
                      'ProxyCommand           ssh -q -A ' + username + '@' + bastion + ' nc %h %p',
                      'ControlMaster          auto',
                      'ControlPath            ~/.ssh/mux-%r@%h:%p',
                      'ControlPersist         yes',
                      'User                   ' + username,
                      'IdentityFile           ~/.ssh/id_rsa'))


def main(env):

    options = {
        'test': setTest,
        'stg': setStg,
        'prod': setProd,
    }

    writeConfig(getUsername(), options[env]())
