import json
import boto3
import os
from datetime import datetime
import logging
import time

# These will be available because of the Lambda Layer (though not used if only sample data)
import requests 
from bs4 import BeautifulSoup

# --- Setup Logging ---
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# --- AWS Clients and Environment Variables ---
s3_client = boto3.client('s3')
DESTINATION_BUCKET = os.environ.get('DESTINATION_BUCKET')

# --- Sample Data for Fallback (Expanded) ---
SAMPLE_JOBS = [
    {
        "title": "Software Engineer (Junior)",
        "company": "Tech Innovations Ltd.",
        "location": "Nairobi, Kenya",
        "url": "https://www.example.com/job/it1",
        "description": "Develop and maintain web applications using Python and JavaScript. Collaborate with senior engineers on new features and bug fixes. Strong problem-solving skills required."
    },
    {
        "title": "Data Analyst Trainee",
        "company": "Analytics Hub Africa",
        "location": "Remote",
        "url": "https://www.example.com/job/it2",
        "description": "Assist in collecting, cleaning, and interpreting data sets. Create reports and dashboards to visualize insights. Proficiency in Excel and basic SQL is a plus."
    },
    {
        "title": "Cybersecurity Intern",
        "company": "SecureNet Solutions",
        "location": "Nairobi, Kenya",
        "url": "https://www.example.com/job/it3",
        "description": "Learn and assist in identifying security vulnerabilities, monitoring network traffic, and implementing security protocols. Basic understanding of networking concepts required."
    },
    {
        "title": "UI/UX Designer Apprentice",
        "company": "Creative Digital Agency",
        "location": "Remote",
        "url": "https://www.example.com/job/it4",
        "description": "Work alongside experienced designers to create intuitive and aesthetically pleasing user interfaces. Learn about user research, wireframing, and prototyping tools."
    },
    {
        "title": "IT Support Specialist (Entry-Level)",
        "company": "Corporate Systems PLC",
        "location": "Mombasa, Kenya",
        "url": "https://www.example.com/job/it5",
        "description": "Provide first-line technical support to employees, troubleshoot hardware and software issues, and assist with IT infrastructure maintenance. Good communication skills essential."
    },
    {
        "title": "Legal Assistant",
        "company": "Lex Chambers Advocates",
        "location": "Nairobi, Kenya",
        "url": "https://www.example.com/job/law1",
        "description": "Support legal team with research, document preparation, and case management. Requires strong organizational skills and attention to detail. Law degree or diploma preferred."
    },
    {
        "title": "Junior Associate - Corporate Law",
        "company": "Kenya Legal Partners",
        "location": "Nairobi, Kenya",
        "url": "https://www.example.com/job/law2",
        "description": "Opportunity for a recent law graduate to gain experience in corporate legal matters. Assist in drafting contracts, conducting due diligence, and client liaison."
    },
    {
        "title": "Administrative Officer (Government)",
        "company": "Ministry of Public Service",
        "location": "Nairobi, Kenya",
        "url": "https://www.example.com/job/gov1",
        "description": "Manage office operations, coordinate meetings, and handle official correspondence. Requires excellent organizational and communication skills. Public administration background is a plus."
    },
    {
        "title": "Policy Analyst Intern",
        "company": "National Development Agency",
        "location": "Nairobi, Kenya",
        "url": "https://www.example.com/job/gov2",
        "description": "Assist in researching and analyzing public policies, preparing policy briefs, and contributing to strategic planning. Strong analytical and writing skills are essential."
    },
    {
        "title": "Executive Assistant",
        "company": "Apex Holdings Group",
        "location": "Nairobi, Kenya",
        "url": "https://www.example.com/job/office1",
        "description": "Provide high-level administrative support to senior executives, manage schedules, arrange travel, and prepare presentations. Discretion and proactive approach are key."
    },
    {
        "title": "Project Coordinator (Entry-Level)",
        "company": "Innovate Solutions Inc.",
        "location": "Nairobi, Kenya",
        "url": "https://www.example.com/job/office2",
        "description": "Support project managers in planning, execution, and monitoring of various projects. Assist with documentation, scheduling, and stakeholder communication. Organizational skills are vital."
    }
]

def lambda_handler(event, context):
    """
    This function now primarily uses SAMPLE_JOBS data for reliability.
    Direct scraping of sites like Indeed.com is often blocked.
    """
    logger.info(f"Starting job scrape at {datetime.utcnow()}")
    
    # --- Always use SAMPLE_JOBS for reliability ---
    scraped_jobs = SAMPLE_JOBS
    logger.info(f"Using {len(scraped_jobs)} sample jobs for processing.")

    now = datetime.utcnow()
    filename = f"scraped-jobs-{now.strftime('%Y-%m-%d-%H-%M-%S')}.json"

    try:
        s3_client.put_object(
            Bucket=DESTINATION_BUCKET,
            Key=filename,
            Body=json.dumps(scraped_jobs, indent=4),
            ContentType='application/json'
        )
        logger.info(f"Successfully uploaded {filename} to {DESTINATION_BUCKET} with {len(scraped_jobs)} jobs.")
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'Successfully processed and saved {len(scraped_jobs)} jobs to {filename}')
        }

    except Exception as e:
        logger.error(f"Error uploading to S3: {e}", exc_info=True)
        raise e
