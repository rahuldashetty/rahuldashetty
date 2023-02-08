import boto3
import json


def lambda_handler(event, context):
    cloudwatch = boto3.client('cloudwatch')
    ec2 = boto3.client('ec2')
    
    # Get the instance ID from the CloudWatch event
    instance_id = event['detail']['instance-id']
    
    # Get the CPU utilization metric for the instance
    utilization = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'm1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/EC2',
                        'MetricName': 'CPUUtilization',
                        'Dimensions': [
                            {
                                'Name': 'InstanceId',
                                'Value': instance_id
                            },
                        ]
                    },
                    'Period': 300,
                    'Stat': 'Average'
                },
                'ReturnData': True
            },
        ],
        StartTime='2022-01-28T00:00:00Z',
        EndTime='2022-01-28T01:00:00Z'
    )
    
    # Check if the instance has been terminated
    instance_state = ec2.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]['State']['Name']
    
    if instance_state == 'terminated':
        # Send termination notification
        send_notification('Instance terminated: ' + instance_id)
    elif utilization['MetricDataResults'][0]['Values'][0] > 80.0:
        # Send high utilization notification
        send_notification('Instance utilization exceeds 80%: ' + instance_id)
        
def send_notification(message):
    sns = boto3.client('sns')
    sns.publish(TopicArn='arn:aws:sns:us-west-2:123456789012:my-topic', Message=message)
