import json
import boto3
import os
import uuid
from datetime import datetime
import logging
import urllib.parse

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
bedrock_runtime = boto3.client('bedrock-runtime')

TABLE_NAME = "AjiraChapchapJobs"
table = dynamodb.Table(TABLE_NAME)

def generate_prompt(job_description_text):
    """
    Generates the prompt for the Amazon Titan Text Express model,
    now including instructions for categorization.
    """
    return f"""You are an AI assistant designed to analyze job descriptions and provide structured output.
Your response MUST be a valid JSON object. Do NOT include any introductory or concluding text,
conversational filler, or any characters outside of the JSON itself.
The output MUST NOT be wrapped in markdown code blocks (e.g., ```json or ```).

Analyze the following job description from a Kenyan job board. Provide a concise summary (max 80 words) suitable for a young audience. Then, evaluate it for legitimacy. Finally, assign a single, relevant category from the following list:
["IT & Software", "Marketing", "Sales", "Healthcare", "Education", "Finance & Accounting", "Admin & HR", "Customer Service", "Hospitality", "Manufacturing", "Logistics & Supply Chain", "Construction", "Agriculture", "Creative Arts", "Legal", "Engineering", "Science & Research", "Trades & Manual Labor", "Other"]
If no category perfectly fits, use "Other". **Always provide the most relevant category from the list, even if the job has red flags or is a potential scam.**

Return a JSON object with four keys:
- 'summary': A concise summary (max 80 words) of the job.
- 'verificationScore': An integer from 0-100 (where 100 is completely legitimate).
- 'flags': An array of strings, listing reasons for the score (e.g., 'requests payment', 'vague job details', 'unprofessional language', 'clear application process', 'no red flags'). If there are no specific red flags, include "no red flags".
- 'category': The chosen category from the provided list.

Job Description:
---
{job_description_text}
---

Output only the JSON object:
"""

def lambda_handler(event, context):
    """
    This function is triggered by an S3 event, processes the job data
    using Amazon Bedrock (Titan Text Express), and stores it in DynamoDB.
    """
    try:
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        s3_object_key_encoded = event['Records'][0]['s3']['object']['key']
        key = urllib.parse.unquote_plus(s3_object_key_encoded)

        logger.info(f"Processing file {key} from bucket {bucket_name}")

        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        scraped_jobs = json.loads(response['Body'].read().decode('utf-8'))
        logger.info(f"Successfully read {len(scraped_jobs)} jobs from S3 object {key}")

        for job in scraped_jobs:
            job_title = job.get("title", "N/A")
            job_company = job.get("company", "N/A")
            job_description = job.get("description", "")
            logger.info(f"Processing job: {job_title} at {job_company}")

            prompt_text = generate_prompt(job_description)

            bedrock_request_body = {
                "inputText": prompt_text,
                "textGenerationConfig": {
                    "maxTokenCount": 1000,
                    "temperature": 0.1,
                    "stopSequences": []
                }
            }

            bedrock_response = bedrock_runtime.invoke_model(
                body=json.dumps(bedrock_request_body),
                modelId='amazon.titan-text-express-v1',
                accept='application/json',
                contentType='application/json'
            )

            response_body_str = bedrock_response['body'].read().decode('utf-8')
            ai_response_json_from_bedrock = json.loads(response_body_str)
            ai_generated_text = ""

            if 'results' in ai_response_json_from_bedrock and len(ai_response_json_from_bedrock['results']) > 0:
                ai_generated_text = ai_response_json_from_bedrock['results'][0].get('outputText', '').strip()
            else:
                logger.error("No valid 'results' or outputText found in Titan Bedrock response.")

            analysis_result = {}
            if ai_generated_text:
                json_start = ai_generated_text.find('{')
                json_end = ai_generated_text.rfind('}')

                if json_start != -1 and json_end != -1 and json_end > json_start:
                    json_string = ai_generated_text[json_start : json_end + 1].strip()
                    try:
                        analysis_result = json.loads(json_string)
                    except json.JSONDecodeError as e:
                        logger.error(f"JSONDecodeError (after extraction): Failed to parse extracted JSON: {e}. Extracted string: '{json_string}'")
                        analysis_result = {}
                else:
                    logger.error(f"Failed to find complete JSON object in AI response. Raw AI response: '{ai_generated_text}'")
                    analysis_result = {}
            else:
                logger.error("No AI generated text to parse for JSON.")

            logger.info(f"Bedrock analysis complete for job: {job_title}")

            job_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{job_title}{job.get('url', '')}"))

            item_to_save = {
                'jobId': job_id,
                'title': job_title,
                'company': job_company,
                'originalUrl': job.get('url', 'N/A'),
                'description': job_description,
                'summary': analysis_result.get('summary', 'N/A'),
                'isVerified': analysis_result.get('verificationScore', 0) > 60,
                'scamAnalysis': {
                    'score': analysis_result.get('verificationScore', 0),
                    'flags': analysis_result.get('flags', [])
                },
                'category': analysis_result.get('category', 'Other'), # NEW: Add category
                'postedDate': datetime.utcnow().strftime('%Y-%m-%d'),
                'status': 'ACTIVE'
            }

            table.put_item(Item=item_to_save)
            logger.info(f"Successfully processed and saved job: {job_id}")

        return {'statusCode': 200, 'body': json.dumps('Processing complete!')}

    except KeyError as e:
        logger.error(f"KeyError: Missing expected key in event: {e}. Ensure your S3 trigger is configured correctly and the test event matches an S3 Put event structure.")
        logger.error(f"Full event received: {json.dumps(event, indent=2)}")
        return {
            'statusCode': 400,
            'body': json.dumps(f"Error: Malformed event. Missing key: {e}. Check S3 trigger configuration.")
        }
    except Exception as e:
        logger.error(f"An unexpected error occurred during processing: {e}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps(f"An internal server error occurred: {str(e)}")
        }
# This code processes job data from an S3 bucket, analyzes it using Amazon Bedrock's Titan Text Express model,
# and stores the results in a DynamoDB table. It includes error handling for common issues like missing keys
# in the event data and unexpected errors during processing.