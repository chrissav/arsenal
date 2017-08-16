#!/usr/bin/env python
#requires pip install requests
#pip install requests[security]

import boto
import boto3
import argparse
import requests
import iam_add_user_to_group
import output

iam = boto.connect_iam()
iam3 = boto3.client('iam')

username = ""
pd_api_access_key=''
pd_subdomain=''
users = []

@output.ExpHandler(output.boto, (Exception,))
def removeAWSUser(user_name):
  try:
    #boto doesn't handle get_login_profiles() the same as other functions
    #will throw an exception instead of storing an empty result
    login_profile = iam.get_login_profiles(user_name)
    for login in login_profile.get_login_profile_result:
      iam.delete_login_profile(user_name)
      output.SUCCESS("Removed login profile for %s" %(user_name))
  except:
    pass
  mfa_device = iam.get_all_mfa_devices(user_name)
  for mfa in mfa_device.mfa_devices:
    iam.deactivate_mfa_device(user_name, mfa['serial_number'])
    output.SUCCESS("Removed MFA (%s) from %s " %(mfa['serial_number'], user_name))
  user_policies = iam.get_all_user_policies(user_name)
  for policy in user_policies.list_user_policies_result['policy_names']:
    iam.delete_user_policy(user_name, policy)
    output.SUCCESS("Removed policy (%s) from %s " %(policy, user_name))
  groups_for_user = iam.get_groups_for_user(user_name)
  for group in groups_for_user.groups:
    iam.remove_user_from_group(group['group_name'], user_name)
    output.SUCCESS("Removed %s from %s " %(user_name, group['group_name']))
  access_keys = iam.get_all_access_keys(user_name)
  for key in access_keys.access_key_metadata:
    iam.delete_access_key(key['access_key_id'], user_name)
    output.SUCCESS("Deleted access key %s for user %s" %(key['access_key_id'], user_name))
  #Managed Policies? only supported in boto3
  acctdetails = iam3.get_account_authorization_details(Filter=['User'])
  users = acctdetails['UserDetailList']
  user = (item for item in users if item['UserName'] == user_name).next()
  for policy in user['AttachedManagedPolicies']:
    iam3.detach_user_policy(UserName=user_name, PolicyArn=policy['PolicyArn'])
    output.SUCCESS("Removed managed policy: %s for %s" %(policy['PolicyName'],user_name))
  iam.delete_user(iam_add_user_to_group.checkUsername(user_name))
  output.SUCCESS("%s has been removed from AWS IAM." % user_name)

@output.ExpHandler(output.HTTP,(Exception,))
def getPDUserID(user_name):
    headers = {
        'Authorization': 'Token token={0}'.format(pd_api_access_key),
        'Content-type': 'application/json',
    }
    payload = {
        'query': user_name,
    }
    r = requests.get(
                    'https://{0}.pagerduty.com/api/v1/users'.format(pd_subdomain),
                    headers=headers,
                    params=payload,
    )
    r.raise_for_status()

    users = r.json()['users']
    for i in users:
      id = i['id']

  output.SUCCESS('Completed')
  return id

@output.ExpHandler(output.HTTP,(Exception,))
def removePDUser(user_id, username):
    headers = {
        'Authorization': 'Token token={0}'.format(pd_api_access_key),
        'Content-type': 'application/json',
    }

    r = requests.delete(
                    'https://{0}.pagerduty.com/api/v1/users/{1}'.format(pd_subdomain, user_id),
                    headers=headers,
    )
    r.raise_for_status()
    output.SUCCESS('%s has been removed from Pager Duty' % username)

def main():
  parser = argparse.ArgumentParser(description='Removes a user from AWS IAM')
  parser.add_argument('--user', help="The user to be removed", nargs="*")

  args = parser.parse_args()

  global users
  if args.user:
    users = [str(item) for item in args.user]
  else:
    users.append(iam_add_user_to_group.getUsername(False))

  for username in users:
    print("Do you want to remove the user '%s' ?" %username)
    answer = raw_input("Enter y/n:")
    if answer == "y":
       removeAWSUser(username)
       removePDUser(getPDUserID(username), username)
       #any others to
    else:
      output.EXIT()

if __name__ == "__main__":
    main()
