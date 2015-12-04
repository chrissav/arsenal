#!/usr/bin/env python

#Supply a text file with -f with EC2 instance ids.  Each id on it's own line.

import boto
import argparse
import os.path, sys, time
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import output

@output.ExpHandler(output.boto, (Exception,))
def terminateInstances(region, id_file):
    ec2 = boto.connect_ec2()
    ec2 = boto.ec2.connect_to_region(region)

    ids = []
    for line in id_file:
        ids.append(line.strip('\n'))

    print "\nThese instances will be terminated: \n"

    #Print name, id, and current running status
    count = 0
    reservations = ec2.get_all_instances(ids)
    for res in reservations:
        for inst in res.instances:
            count += 1
            if 'Name' in inst.tags:
                print "%s (%s) [%s]" % (inst.tags['Name'], inst.id, inst.state)
            else:
                print "%s [%s]" % (inst.id, inst.state)
    print "Total: %s instances" % count

    answer = raw_input("\nAre you sure you want to TERMINATE all of the above instances? (y/n) > ")
    if answer.upper() == 'Y':
        #turn off termination protection and terminate
        for i in ids:
            print "\n************** Terminating %s **************\n" % i
            vols = ec2.get_all_volumes(filters={'attachment.instance-id': i})
            if not vols:
                print "There are no attached volumes"
            else:
                for v in vols:
                    ec2.detach_volume(v.id)
                    print "Unattaching %s... this may take a minute" % v
                    #try to detach for 15 seconds and make sure it detaches before deleting
                    start_time = time.time()
                    while v.attachment_state() == 'attached':
                        time.sleep(1)
                        #Query AWS for new volume information
                        v.update()
                        if ((time.time() - start_time) > 30):
                            print "\nDetaching %s is taking too long.  Check the AWS console" % v
                            break
                    #just to make sure
                    time.sleep(3)
                    print "Successfully detached %s" % v
                    try:
                        ec2.delete_volume(v.id)
                        print "Successfully deleted %s" % v
                    except:
                        print "There was a problem deleting %s" %v
            ec2.modify_instance_attribute(i, 'disableApiTermination', False)
            print "Successfully turned off Termination Protection for %s" % i
            ec2.terminate_instances(i)
            print "Successfully terminated the instance %s" % i
    else:
        print "Exiting.."

def main():
    def is_valid_file(parser, arg):
        if not os.path.isfile(arg):
            parser.error("The file %s does not exist!" % arg)
        else:
            return open(arg, 'r')
    
    parser = argparse.ArgumentParser(description='Terminates ec2 instances and deletes their volumes')
    parser.add_argument('--file', '-f', dest='filename', required=True,
                        help='The input file of ec2 instances ids', metavar='FILE',
                        type=lambda x: is_valid_file(parser, x))

    parser.add_argument(
        '--region', '-r', choices=['us-west-1', 'us-west-2', 'us-east-1'],
        help="Set the region to connect to.  Default is us-west-2 (e.g. us-west-1, us-west-2, us-east-1)"
    )

    args = parser.parse_args()

    if args.region:
        terminateInstances(args.region, args.filename)
    else:
        terminateInstances('us-west-2', args.filename)

if __name__ == "__main__":
    main()
