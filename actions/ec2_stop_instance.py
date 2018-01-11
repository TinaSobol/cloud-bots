import boto3
import json
import os
from botocore.exceptions import ClientError

### Turn off EC2 instance ###
def main(message,event_log):
	#House keeping - set up variables	
	instance = message['Entity']['Id']
	region = message['Entity']['Region']
	region = region.replace("_","-")

	#initialize ec2
	ec2 = boto3.resource('ec2', region_name=region)

	try:
		#Apply the tags
		stop_instance = ec2.stop_instances(InstanceIds=[instance])
		responseCode = stop_instance['ResponseMetadata']['HTTPStatusCode']

		if responseCode >= 400:
			event_log.append("Unexpected error:" + stop_instance + "\n")
		else:
			event_log.append("Instance stopped: " + instance + " \n")
				
	except (ClientError, AttributeError) as e:
		event_log.append("Unexpected error: %s" % e + "\n")
	
	return(event_log)