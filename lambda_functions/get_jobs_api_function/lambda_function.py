import json
import boto3
import logging
from decimal import Decimal # Import Decimal type

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("AjiraChapchapJobs")

# Custom JSON encoder to handle Decimal objects
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            # Check if it's an integer or float
            if obj % 1 == 0:
                return int(obj) # Convert to integer if it has no fractional part
            else:
                return float(obj) # Convert to float otherwise
        # Let the base class default method raise the TypeError for other types
        return json.JSONEncoder.default(self, obj)

def lambda_handler(event, context):
    """
    Queries DynamoDB using the GSI to fetch active jobs, sorted by date.
    """
    logger.info("Received request for jobs API")
    try:
        response = table.query(
            IndexName='status-postedDate-index',
            KeyConditionExpression=boto3.dynamodb.conditions.Key('status').eq('ACTIVE'),
            ScanIndexForward=False
        )

        logger.info(f"Successfully retrieved {len(response['Items'])} jobs from DynamoDB")

        # Return the response with CORS headers
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET'
            },
            # Use the custom DecimalEncoder for json.dumps
            'body': json.dumps(response['Items'], cls=DecimalEncoder)
        }

    except Exception as e:
        logger.error(f"Error querying DynamoDB: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'error': 'Could not retrieve jobs.'})
        }