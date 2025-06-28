# ajira-chapchap-serverless
A serverless application for verifying and categorizing entry-level job listings for Kenyan youth using AWS Lambda and Amazon Bedrock.
# Ajira Chapchap: Serverless Job Verification Platform

![Ajira Chapchap Logo/Banner](https://placehold.co/1200x400/3944F2/FFFFFF?text=Ajira+Chapchap+Verified+Jobs)
*(Replace the placeholder image URL with an actual project banner or logo if you create one)*

A serverless web application designed to empower Kenyan youth by providing **verified and categorized entry-level job listings**, combating the rise of online job scams. This project leverages the power of AWS Lambda and Amazon Bedrock to automate the entire process from job discovery to intelligent analysis and presentation.

---

## ✨ Features

* **Automated Job Scraping:** Regularly collects job postings from various online sources.
* **AI-Powered Verification:** Utilizes **Amazon Bedrock (Titan Text Express)** to analyze job descriptions for legitimacy, assigning a `verificationScore` and identifying `flags` (potential scam indicators).
* **Intelligent Categorization:** AI automatically categorizes jobs into relevant fields (e.g., "IT & Software", "Legal", "Government", "Admin & HR") for easy filtering.
* **User-Friendly Interface:** A clean, responsive single-page application (SPA) built with HTML, CSS (Tailwind CSS), and JavaScript.
* **Search & Filter:** Users can search by title/company and filter jobs by AI-assigned categories.
* **Save Jobs:** Users can save interesting job listings locally in their browser.
* **Fully Serverless:** Cost-effective, scalable, and highly available architecture on AWS.

---

## 🚀 Live Demo

Experience Ajira Chapchap live!
[**Explore Ajira Chapchap Jobs Here!**](http://ajira-chapchap-webapp-2026.s3-website.eu-central-1.amazonaws.com/)
*(**IMPORTANT:** Replace this URL with your actual S3 static website endpoint or CloudFront URL)*

---

## 💡 How It Works: The Serverless Pipeline

Ajira Chapchap operates on a robust, event-driven serverless architecture on AWS. Each component plays a crucial role in delivering verified job opportunities.

### High-Level Architecture Diagram

```mermaid
graph TD
    A[EventBridge Scheduler] -->|Triggers Daily| B(Lambda: scrapeJobsFunction)
    B -->|Uploads Raw Data| C(Amazon S3: Raw Jobs Bucket)
    C -->|New Object Event| D(Lambda: processJobsFunction)
    D -->|Invokes LLM| E(Amazon Bedrock: Titan Text Express)
    E -->|Returns Analysis| D
    D -->|Stores Enriched Data| F(Amazon DynamoDB: AjiraChapchapJobs)
    G[Frontend UI (S3 Hosted)] -->|API Request| H(Amazon API Gateway)
    H -->|Triggers| I(Lambda: getJobsApiFunction)
    I -->|Queries Data| F
    F -->|Returns Jobs| I
    I -->|Sends Response| H
    H -->|Delivers Data| G



Detailed Component Breakdown
scrapeJobsFunction (AWS Lambda)

Role: The data acquisition agent.

Trigger: Scheduled daily by Amazon EventBridge.

Action: Collects raw job data. For demonstration and reliability in a hackathon environment, it uses a rich, diverse set of sample job data (IT, Law, Government, Office roles). In a production scenario, this would involve web scraping (e.g., using requests and BeautifulSoup).

Output: Stores raw JSON job data files in an Amazon S3 Bucket (ajira-chapchap-raw-jobs-YOURNAME-UNIQUEID).

processJobsFunction (AWS Lambda)

Role: The AI intelligence hub.

Trigger: Automatically invoked by an S3 Event Notification whenever a new raw job file is uploaded.

Action:

Reads the raw job data from S3.

Sends each job description to Amazon Bedrock (using the amazon.titan-text-express-v1 Foundation Model).

Bedrock analyzes the text and returns a structured JSON output containing:

summary: A concise, youth-friendly job summary.

verificationScore: A legitimacy score (0-100).

flags: Specific reasons for the score (e.g., "requests payment", "vague details").

category: An AI-assigned job category (e.g., "IT & Software", "Legal", "Other").

Parses Bedrock's response and enriches the job data.

Output: Stores the fully processed and AI-enriched job data in Amazon DynamoDB (AjiraChapchapJobs table).

getJobsApiFunction (AWS Lambda)

Role: The data delivery service.

Trigger: An HTTP GET request from the frontend via Amazon API Gateway.

Action: Queries the AjiraChapchapJobs DynamoDB table to retrieve all verified and categorized job listings.

Output: Returns the job data as a JSON response back through API Gateway to the frontend.

Amazon S3 (Frontend Hosting)

Role: Static website hosting.

Function: Hosts the index.html, style.css, and script.js files that make up the user interface. Configured for static website hosting.

Amazon API Gateway

Role: Secure and scalable entry point for the frontend to access backend data.

Function: Exposes a REST API endpoint (/jobs) that triggers the getJobsApiFunction Lambda.

Amazon Bedrock

Role: Provides access to powerful Foundation Models.

Function: Used by processJobsFunction for the core AI analysis (summarization, verification, categorization) with the Titan Text Express model.

Amazon DynamoDB

Role: Fast, flexible NoSQL database.

Function: Stores all the processed, AI-enriched job listings, ready for quick retrieval by the API.

Amazon EventBridge

Role: Serverless event bus for scheduling.

Function: Schedules the scrapeJobsFunction to run periodically (e.g., daily) to keep job listings up-to-date.

Amazon CloudFront (Optional/Recommended)

Role: Content Delivery Network (CDN).

Function: Speeds up content delivery for the frontend and adds an extra layer of security.

🛠️ Technologies Used
Backend:

AWS Lambda (Python 3.9)

Amazon Bedrock (Titan Text Express)

Amazon S3

Amazon DynamoDB

Amazon API Gateway

Amazon EventBridge

Boto3 (AWS SDK for Python)

Frontend:

HTML5

CSS3 (Tailwind CSS)

JavaScript

Chart.js (for data visualization in the infographic)

⚙️ Setup and Deployment (High-Level)
This project is deployed entirely on AWS. Here's a high-level overview of the setup:

AWS Account: Ensure you have an active AWS account.

IAM Permissions: Create an IAM user or role with necessary permissions for Lambda, S3, DynamoDB, API Gateway, EventBridge, and Bedrock (including access to amazon.titan-text-express-v1).

S3 Buckets:

One S3 bucket for raw job data (trigger for processJobsFunction).

One S3 bucket for static website hosting (frontend).

DynamoDB Table: Create a table named AjiraChapchapJobs with jobId as the Partition Key and a Global Secondary Index on status and postedDate.

Lambda Functions:

Deploy scrapeJobsFunction, processJobsFunction, and getJobsApiFunction using Python 3.9 runtime.

Attach necessary IAM roles and layers (e.g., requests, BeautifulSoup4).

Configure environment variables (e.g., DESTINATION_BUCKET).

Adjust Lambda timeouts (especially for processJobsFunction to allow for Bedrock calls).

API Gateway: Create a REST API endpoint that integrates with getJobsApiFunction.

EventBridge: Set up a scheduled rule to trigger scrapeJobsFunction.

Bedrock Model Access: Ensure Titan Text Express model access is granted in your AWS region (eu-central-1).

Frontend Deployment: Upload index.html, style.css, and script.js to your frontend S3 bucket and enable static website hosting. Update the API_ENDPOINT in script.js to your deployed API Gateway URL.

(For detailed deployment instructions, refer to the project's internal documentation or a more extensive setup guide if available.)

📸 Screenshots
(Add screenshots of your live application here to make your README visually appealing. Include shots of:)

The main job listings page.

A job card showing the verification score and category.

The category filter dropdown in action.

The "Saved Jobs" tab.

Perhaps a screenshot of the infographic presentation itself.

🤝 Contributing
Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please open an issue or submit a pull request.

📄 License
This project is licensed under the MIT License.