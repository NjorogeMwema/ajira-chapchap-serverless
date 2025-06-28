

# Ajira Chapchap: Serverless Job Verification Platform
=====================================================

A serverless application for verifying and categorizing entry-level job listings for Kenyan youth using AWS Lambda and Amazon Bedrock.

## Overview
-----------

Ajira Chapchap is a serverless web application designed to empower Kenyan youth by providing **verified and categorized entry-level job listings**, combating the rise of online job scams. This project leverages the power of AWS Lambda and Amazon Bedrock to automate the entire process from job discovery to intelligent analysis and presentation.

## Features
--------

* **Automated Job Scraping:** Regularly collects job postings from various online sources.
* **AI-Powered Verification:** Utilizes **Amazon Bedrock (Titan Text Express)** to analyze job descriptions for legitimacy, assigning a `verificationScore` and identifying `flags` (potential scam indicators).
* **Intelligent Categorization:** AI automatically categorizes jobs into relevant fields (e.g., "IT & Software", "Legal", "Government", "Admin & HR") for easy filtering.
* **User-Friendly Interface:** A clean, responsive single-page application (SPA) built with HTML, CSS (Tailwind CSS), and JavaScript.

## Detailed Component Breakdown
-----------------------------

### scrapeJobsFunction (AWS Lambda)

* **Role:** The data acquisition agent.
* **Trigger:** Scheduled daily by Amazon EventBridge.
* **Action:** Collects raw job data. For demonstration and reliability in a hackathon environment, it uses a rich, diverse set of sample job data (IT, Law, Government, Office roles). In a production scenario, this would involve web scraping (e.g., using requests and BeautifulSoup).
* **Output:** Stores raw JSON job data files in an Amazon S3 Bucket (ajira-chapchap-raw-jobs-YOURNAME-UNIQUEID).

### processJobsFunction (AWS Lambda)

* **Role:** The AI intelligence hub.
* **Trigger:** Automatically invoked by an S3 Event Notification whenever a new raw job file is uploaded.
* **Action:**
	+ Reads the raw job data from S3.
	+ Sends each job description to Amazon Bedrock (using the amazon.titan-text-express-v1 Foundation Model).
	+ Bedrock analyzes the text and returns a structured JSON output containing:
		- `summary`: A concise, youth-friendly job summary.
		- `verificationScore`: A legitimacy score (0-100).
		- `flags`: Specific reasons for the score (e.g., "requests payment", "vague details").
		- `category`: An AI-assigned job category (e.g., "IT & Software", "Legal", "Other").
	+ Parses Bedrock's response and enriches the job data.
* **Output:** Stores the fully processed and AI-enriched job data in Amazon DynamoDB (AjiraChapchapJobs table).

### getJobsApiFunction (AWS Lambda)

* **Role:** The data delivery service.
* **Trigger:** An HTTP GET request from the frontend via Amazon API Gateway.
* **Action:** Queries the AjiraChapchapJobs DynamoDB table to retrieve all verified and categorized job listings.
* **Output:** Returns the job data as a JSON response back through API Gateway to the frontend.

### Amazon S3 (Frontend Hosting)

* **Role:** Static website hosting.
* **Function:** Hosts the index.html, style.css, and script.js files that make up the user interface. Configured for static website hosting.

### Amazon API Gateway

* **Role:** Secure and scalable entry point for the frontend to access backend data.
* **Function:** Exposes a REST API endpoint (/jobs) that triggers the getJobsApiFunction Lambda.

### Amazon Bedrock

* **Role:** Provides access to powerful Foundation Models.
* **Function:** Used by processJobsFunction for the core AI analysis (summarization, verification, categorization) with the Titan Text Express model.

### Amazon DynamoDB

* **Role:** Fast, flexible NoSQL database.
* **Function:** Stores all the processed, AI-enriched job listings, ready for quick retrieval by the API.

#### DynamoDB Table Schema

| Attribute        | Type    | Description                                                      |
|------------------|---------|------------------------------------------------------------------|
| jobId            | String  | Unique identifier for each job listing (Partition Key).          |
| title            | String  | Job title.                                                       |
| company          | String  | Name of the hiring company.                                      |
| description      | String  | Full job description text.                                       |
| summary          | String  | AI-generated concise summary of the job.                         |
| verificationScore| Number  | AI-assigned legitimacy score (0-100).                            |
| flags            | List    | List of potential scam indicators flagged by AI.                 |
| category         | String  | AI-assigned job category (e.g., "IT & Software", "Legal