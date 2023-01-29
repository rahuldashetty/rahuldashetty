import boto3

def lambda_handler(event, context):
    # Get the S3 bucket name and object name from the event
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    object_key = event["Records"][0]["s3"]["object"]["key"]
    
    # Get the file format from the object key
    file_format = object_key.split(".")[-1]
    
    # Check if the object was uploaded to the specific SNS bucket
    if bucket_name == "specific-sns-bucket":
        # Send SNS message if object was uploaded to specific SNS bucket
        sns = boto3.client("sns")
        message = f"An object was uploaded to the {bucket_name} bucket with the file format: {file_format}"
        sns.publish(TopicArn="arn:aws:sns:<REGION>:<ACCOUNT_ID>:<TOPIC_NAME>", Message=message)

    return {
        "statusCode": 200,
        "body": "SNS message sent successfully"
    }
