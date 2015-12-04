#!/usr/bin/env python

#Supply a text file with -f with EC2 instance ids.  Each id on it's own line.

import boto
import argparse
import os.path, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import output

region = 'us-west-2'

def getInstances(region, id_file):
    ec2 = boto.connect_ec2()
    ec2 = boto.ec2.connect_to_region(region)

    ids = []
    for line in id_file:
        ids.append(line.strip('\n'))

    print "\nThese are the instances found: \n"

    #Print name, id, and current running status
    reservations = ec2.get_all_instances(ids)
    for res in reservations:
        for inst in res.instances:
            if 'Name' in inst.tags:
                print "%s (%s) [%s]" % (inst.tags['Name'], inst.id, inst.state)
            else:
                print "%s [%s]" % (inst.id, inst.state)

    answer = raw_input("Do you want to continue? (y/n) > ")
    if answer.upper() == "Y":
        return ids
    else:
        print "Exiting.."

def snapshotAndDetachVolumes(ids):
    for i in ids:
        print "\n************** Snapshot and Detaching for %s **************\n" % i
        vols = ec2.get_all_volumes(filters={'attachment.instance-id': i})
        if not vols:
            print "There are no attached volumes"
        else:
            for v in vols:
                snap = ec2.create_snapshot(v.id, "decommission snapshot for %s" % i)
                print "Created snapshot %s for %s" % (snap, v)
                ec2.detach_volume(v.id)
                print "Detached %s" % v

def stopInstances(ids):
    answer = raw_input("\nAre you sure you want to stop all of the above instances? (y/n) > ")
    if answer.upper() =='Y':
        result = ec2.stop_instances(ids, dry_run=True)
        print result

def terminateInstances(ids):
    answer = raw_input("\nAre you sure you want to TERMINATE FOREVER all of the above instances? (y/n) > ")
    if answer.upper() == 'Y':
        result = ec2.terminate_instances(ids, dry_run=True)
        print result

def main():
    def is_valid_file(parser, arg):
        if not os.path.isfile(arg):
            parser.error("The file %s does not exist!" % arg)
        else:
            return open(arg, 'r')
    
    parser = argparse.ArgumentParser(description='Decommission options for ec2 instances')
    parser.add_argument('--file', '-f', dest='filename', required=True,
                        help='The input file of ec2 instances ids', metavar='FILE',
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument(
        '--region', '-r', choices=['us-west-1', 'us-west-2', 'us-east-1'],
        help="Set the region to connect to.  Default is us-west-2 (e.g. us-west-1, us-west-2, us-east-1)"
    )
    parser.add_argument(
        '--terminate',
        help="Terminates the instances, make sure to snapshot first!"
    )

    args = parser.parse_args()

    if args.region:
        global region
        region = args.region

    #Can't do this!
    if args.terminate:
        answer = raw_input("This will terminate the instances, do you want to snapshot the attached volumes and stop the instances first?")
        if answer.upper() == "Y":
            snapshotAndDetachVolumes(getInstances(region, args.filename))
            stopInstances(getInstances(region, args.filename))
            terminateInstances(getInstances(region, args.filename))
        if answer.upper() == "N":
            terminateInstances(getInstances(region, args.filename))
    else:
        snapshotAndDetachVolumes(getInstances(region, args.filename))
        stopInstances(getInstances(region, args.filename))
        terminateInstances(getInstances(region, args.filename))

if __name__ == "__main__":
    main()