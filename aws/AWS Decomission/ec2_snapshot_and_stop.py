#!/usr/bin/env python

#Supply a text file with -f with EC2 instance ids.  Each id on its own line.

import boto
import argparse
import os.path, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import output

@output.ExpHandler(output.boto, (Exception,))
def snapAndStop(region, id_file):
    ec2 = boto.connect_ec2()
    ec2 = boto.ec2.connect_to_region(region)

    ids = []
    for line in id_file:
        ids.append(line.strip('\n'))

    print "\nThese instances will snapshotted and stopped: \n"

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

    answer = raw_input("\nAre you sure you want to snapshot and stop all of the above instances? (y/n) > ")
    if answer.upper() == 'Y':
        for i in ids:
            print "\n************** Stopping %s **************\n" % i
            ec2.stop_instances(i)
            print "Successfully stopped the instance %s" % i
            vols = ec2.get_all_volumes(filters={'attachment.instance-id': i})
            if not vols:
                print "There are no attached volumes"
            else:
                for v in vols:
                    snap = ec2.create_snapshot(v.id, "decommission snapshot for %s" % i)
                    print "Creating %s for %s" % (snap, v)

    else:
        print "Exiting..."

def main():
    def is_valid_file(parser, arg):
        if not os.path.isfile(arg):
            parser.error("The file %s does not exist!" % arg)
        else:
            return open(arg, 'r')
    
    parser = argparse.ArgumentParser(description='Snapshots all attached volumes and stops the instances given')
    parser.add_argument('--file', '-f', dest='filename', required=True,
                        help='The input file of ec2 instances ids', metavar='FILE',
                        type=lambda x: is_valid_file(parser, x))

    parser.add_argument(
        '--region', '-r', choices=['us-west-1', 'us-west-2', 'us-east-1'],
        help="Set the region to connect to.  Default is us-west-2 (e.g. us-west-1, us-west-2, us-east-1)"
    )

    args = parser.parse_args()

    if args.region:
        snapAndStop(args.region, args.filename)
    else:
        snapAndStop('us-west-2', args.filename)

if __name__ == "__main__":
    main()
