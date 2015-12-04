#!/usr/bin/env python

import boto

qa_elb = "corp-tech-pa-qa-42038617.us-west-2.elb.amazonaws.com"

qa_urls = [
'au-mba-pa-sb01-qa.2u.com',
'au-mba-pa-sb02-qa.2u.com',
'au-mba-pa-sb03-qa.2u.com',
'au-mba-pa-stg.2u.com',
'au-mir-pa-sb01-qa.2u.com',
'au-mir-pa-sb02-qa.2u.com',
'au-mir-pa-sb03-qa.2u.com',
'au-mir-pa-stg.2u.com',
'gwu-mha-pa-sb01-qa.2u.com',
'gwu-mha-pa-sb02-qa.2u.com',
'gwu-mha-pa-sb03-qa.2u.com',
'gwu-mha-pa-stg.2u.com',
'gwu-mph-pa-sb01-qa.2u.com',
'gwu-mph-pa-sb02-qa.2u.com',
'gwu-mph-pa-sb03-qa.2u.com',
'gwu-mph-pa-stg.2u.com',
'nu-mac-pa-sb01-qa.2u.com',
'nu-mac-pa-sb02-qa.2u.com',
'nu-mac-pa-sb03-qa.2u.com',
'nu-mac-pa-stg.2u.com',
'sc-ent-pa-sb01-qa.2u.com',
'sc-ent-pa-sb02-qa.2u.com',
'sc-ent-pa-sb03-qa.2u.com',
'sc-ent-pa-stg.2u.com',
'smu-mds-pa-sb01-qa.2u.com',
'smu-mds-pa-sb02-qa.2u.com',
'smu-mds-pa-sb03-qa.2u.com',
'smu-mds-pa-stg.2u.com',
'syr-mac-pa-sb01-qa.2u.com',
'syr-mac-pa-sb02-qa.2u.com',
'syr-mac-pa-sb03-qa.2u.com',
'syr-mac-pa-stg.2u.com',
'ucb-mids-pa-sb01-qa.2u.com',
'ucb-mids-pa-sb02-qa.2u.com',
'ucb-mids-pa-sb03-qa.2u.com',
'ucb-mids-pa-stg.2u.com',
'unc-mpa-pa-sb01-qa.2u.com',
'unc-mpa-pa-sb02-qa.2u.com',
'unc-mpa-pa-sb03-qa.2u.com',
'unc-mpa-pa-stg.2u.com',
'yu-med-pa-sb01-qa.2u.com',
'yu-med-pa-sb02-qa.2u.com',
'yu-med-pa-sb03-qa.2u.com',
'yu-med-pa-stg.2u.com'
]

prod_elb = "corp-tech-pa-prod-482947080.us-west-2.elb.amazonaws.com."
prod_urls = [
'au-mba-pa-prod.2u.com',
'au-mir-pa-prod.2u.com',
'gwu-mha-pa-prod.2u.com',
'gwu-mph-pa-prod.2u.com',
'nu-mac-pa-prod.2u.com',
'sc-ent-pa-prod.2u.com',
'smu-mds-pa-prod.2u.com',
'syr-mac-pa-prod.2u.com',
'ucb-mids-pa-prod.2u.com',
'unc-mpa-pa-prod.2u.com',
'yu-med-pa-prod.2u.com',
]

r53 = boto.connect_route53()
zone = r53.get_zone("2u.com")

for i in qa_urls:
  print "\n----------Attempting to add " + i + "----------\n"
  try:
    status = zone.add_cname(i, qa_elb, 600, identifier=None, comment='')
    print "Successfully added " + i
  except Exception,e:
    print e.__class__.__name__, ':', e.message

for i in prod_urls:
  print "\n----------Attempting to add " + i + "----------\n"
  try:
    status = zone.add_cname(i, prod_elb, 600, identifier=None, comment='')
    print "Successfully added " + i
  except Exception,e:
    print e.__class__.__name__, ':', e.message