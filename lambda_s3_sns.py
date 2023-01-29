import boto3

def lambda_handler(event, context):
    #creating connection b/w lambda and s3
    s3 = boto3.client("s3")
    #creating connection b/w lambda and sns
    sns = boto3.client("sns")
    
    # Get the name of the S3 bucket
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    
    # Check if the bucket name matches the desired bucket, in place of "my-desired-bucket" please enter your bucket name
    if bucket_name == "my-desired-bucket":
        object_key = event["Records"][0]["s3"]["object"]["key"]
        #the above line is used to take the object name that has been recently uploaded
        message = "A new object was uploaded to the '{}' S3 bucket. Object key: '{}'".format(bucket_name, object_key)
        sns.publish(TopicArn="arn:aws:sns:<REGION>:<ACCOUNT_ID>:<TOPIC_NAME>", Message=message)
    
    return "Done"
