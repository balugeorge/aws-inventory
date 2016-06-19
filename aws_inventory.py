#!/usr/bin/env python3
import sys
import argparse
import yaml
import boto3
import csv
import os
parser = argparse.ArgumentParser()


class Connect:

    def __init__(self, access_key=None, secret_key=None, region=None, profile=None, output_type=None):
        self.profile = args.profile if profile is None else profile
        self.output_type = args.output_type if output_type is None else output_type
        if not os.path.isfile('credentials.yml'):
            raise FileNotFoundError("Create a credentials.yml using the example file credentials.default.yml")
        streams = open('credentials.yml', 'r')
        self.data = [out for out in yaml.load_all(streams)]
        # To-do: output error message if profile name is not present in credentials.yml file
        if self.profile is not None:
            for line in self.data:
                self.access_key = line.get(self.profile, {}).get('AWS_ACCESS_KEY_ID')
                self.secret_key = line.get(self.profile, {}).get('AWS_SECRET_ACCESS_KEY')
                self.region = line.get(self.profile, {}).get('AWS_DEFAULT_REGION')
                if access_key or secret_key or region is not None:
                    print(access_key, secret_key, region)
                    break
            self.session = boto3.session.Session(
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region)
            self.ec2 = self.session.resource('ec2')
        streams.close()

    def profiles(self):
        print("Available profiles are:")
        for line in self.data:
            for profile in line:
                print(profile)

    def inventory(self):
        instances = self.ec2.instances.all()
        if self.output_type in {None, "stdout"}:
            print('{0:20}{1:20}{2:20}{3:20}{4:20}'.format(
                "instance_id",
                "instance_type",
                "instance_state",
                "public_ip",
                "private_ip"))

            for instance in instances:
                print('{0!s:20}{1!s:20}{2!s:20}{3!s:20}{4!s:20}'.format(
                    instance.id,
                    instance.instance_type,
                    instance.state['Name'],
                    instance.public_ip_address,
                    instance.private_ip_address))

        if self.output_type == "file":
            output_file = "inventory_" + self.profile + ".csv"
            open(output_file, 'w').close()
            with open(output_file, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(["instance_id", "instance_type", "instance_state", "public_ip", "private_ip"])
                for instance in instances:
                    writer.writerow(
                        [instance.id,
                         instance.instance_type,
                         instance.state['Name'],
                         instance.public_ip_address,
                         instance.private_ip_address])

if __name__ == '__main__':
    parser.add_argument('-p', '--profile',
                        help='PROFILE should be the profile name listed under credentials.yml file')
    parser.add_argument('-l', '--list', help='print a list of all available profiles', action='store_true')
    parser.add_argument('-t', '--output_type',
                        help='''OUTPUT_TYPE should be file for writing inventory list to a csv file,
                        use stdout to print inventory to terminal''')
    args = parser.parse_args()
    connect = Connect()
    if len(sys.argv) == 1:
        parser.print_help()
    elif args.list:
        connect.profiles()
    else:
        try:
            connect.inventory()
        except Exception as e:
            print(str(e))
