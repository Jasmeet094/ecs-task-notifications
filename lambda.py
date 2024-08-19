import json
import boto3
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns_client = boto3.client('sns')
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:317659955577:slack-notifications-devops-alert-slack'

def lambda_handler(event, context):
    logger.info("Received event: " + json.dumps(event))

    # Check if 'detail' key exists
    if 'detail' not in event:
        logger.error("'detail' key not found in the event")
        return {
            'statusCode': 400,
            'body': json.dumps("'detail' key not found in the event")
        }

    stopped_reason = event['detail'].get('stoppedReason', '')
    if stopped_reason == 'Essential container in task exited':
        for container in event['detail'].get('containers', []):
            if 'reason' in container and 'OutOfMemoryError' in container['reason']:
                task_arn = event['detail'].get('taskArn', 'Unknown')
                cluster_arn = event['detail'].get('clusterArn', 'Unknown')
                container_name = container.get('name', 'Unknown')
                reason = container.get('reason', 'Unknown')

                message = {
                    "version": "1.0",
                    "source": "custom",
                    "content": {
                        "textType": "client-markdown",
                        "title": "ECS Task OOM Error",
                        "description": (
                            ":warning: ECS Task OOM Error\n"
                            f"Cluster ARN: `{cluster_arn}`\n"
                            f"Task ARN: `{task_arn}`\n"
                            f"Container: `{container_name}`\n"
                            f"Reason: `{reason}`"
                        )
                    }
                }

                sns_client.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Message=json.dumps(message),
                    Subject='ECS Task OOM Error'
                )
                logger.info(f"Notification sent to SNS topic: {SNS_TOPIC_ARN} with message: {json.dumps(message)}")
                break
    return {
        'statusCode': 200,
        'body': json.dumps('Processed')
    }
