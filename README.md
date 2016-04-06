## aws-inventory
Simple boto3 based script to get a list of AWS ec2 instances.

## Setup
    pip3 install -r requirements.txt

Create a `credentials.yml` file and add IAM keys with read only access to EC2 services along with the region. An example file `credentials.default.yml` shows the format to be used for credentials.yml(replace profile1 and profile2 as required and add AWS access and secret keys along with the region). Multiple profiles for separate AWS accounts can be created.

## Usage  
	usage: aws-inventory [-h] [-p PROFILE] [-l]

    optional arguments:
    -h, --help            show this help message and exit
    -p PROFILE, --profile PROFILE
                            enter profile name listed under the credentials.yml file
    -l, --list            print a list of all available profiles
