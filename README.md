# Setup Notifications for OOM ECS Task Killed

This setup used if we need to get notified if any of the ECS task of our production application got killed due to OOM so that we gets notified if killed task due to OOM creating downtime for our application so that we can take a look and resolve such issues to not happen in future

### Step 1: Create SNS Topic

1.  Go to Amazon SNS and create a new Topic of type Standard.
2. For the Subscriptions we dont need to configure any for now as it will automatically gets configured during next steps.

### Step 2: Configure Aws Chatbot.
    
1. Go to AWS Chatbot and Configure a new Slack client , configure a new channel in which you want to receive notifications.
2. Give the configuration name as per the slack channel name , get the slack channel ID and paste it under Channel type.
3. For the Role Name use AWSChatbot-Role and every other setting should be same as default.
4. For the SNS topic choose the topic name we created at Step No.1 
5. Click on Configure. After configuring you can see that the SNS topic we created at Step 1 should have the subscription got created.

### Step 3: Create Lambda Function.

 1. Create a New Lambda python Function.
 2. Lambda Code used in lambda.py file , only need to change the SNS Topic ARN in Lambda code which we created in Step 1. 

### Create AWS EventBridge Rule.
  1. Go to AWS Eventbridge and create a rule of type Rule with an event pattern.
  2. Use default settings for every option but for Creation method select Custom  pattern (JSON editor) and paste below code and change account and cluster id:

```
{
  "source": ["aws.ecs"],
  "detail-type": ["ECS Task State Change"],
  "detail": {
    "clusterArn": [“arn:aws:ecs:us-east-1:ACCOUNT_ID:cluster/CLUSTER-ID“],
    "lastStatus": ["STOPPED"]
  }
}
```

  3. For the Target 1 choose the Lambda function ARN we created at Step 3. And Create the Eventbridge Rule.


### Summary: 
Now you will receive notifications in Slack channel whenever any ECS task got killed due to Out Of Memory status. 
