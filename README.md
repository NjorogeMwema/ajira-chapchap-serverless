# Ajira Chapchap: Serverless Job Verification Platform

![Ajira Chapchap Logo/Banner](https://placehold.co/1200x400/3944F2/FFFFFF?text=Ajira+Chapchap+Verified+Jobs)
<sub>*(Replace the placeholder image with your project banner or logo)*</sub>

Ajira Chapchap is a **serverless web application** built to empower Kenyan youth by providing **verified, categorized entry-level job listings**—helping combat the rise of online job scams. Leveraging AWS Lambda and Amazon Bedrock, the platform automates job discovery, verification, and presentation.

---

## 🚀 Features

- **Automated Job Scraping:** Gathers job postings from multiple online sources.
- **AI-Powered Verification:** Uses **Amazon Bedrock (Titan Text Express)** to analyze job descriptions, assign a `verificationScore`, and flag potential scams.
- **Intelligent Categorization:** Automatically classifies jobs into fields like "IT & Software", "Legal", "Government", and "Admin & HR".
- **User-Friendly Interface:** Responsive SPA built with HTML, Tailwind CSS, and JavaScript.
- **Search & Filter:** Search by title/company and filter by AI-assigned categories.
- **Save Jobs:** Save interesting listings locally in your browser.
- **Fully Serverless:** Cost-effective, scalable, and highly available AWS architecture.

---

## 💡 Project Overview

### Why Ajira Chapchap?

Kenyan youth face a flood of fraudulent online job postings. Ajira Chapchap was created to cut through the noise, offering a trusted, efficient way to find legitimate opportunities and build careers safely.

### How It Works

Ajira Chapchap follows a **serverless-first approach** on AWS for scalability and low operational overhead. The core pipeline:

1. **Data Acquisition:**  
    - Scrapes job boards (or uses curated sample data for demos) via Python (`requests`, `BeautifulSoup`).
2. **AI Analysis:**  
    - Sends job descriptions to **Amazon Bedrock** (Titan Text Express) for summarization, legitimacy scoring, flagging, and categorization.
3. **Data Persistence & Delivery:**  
    - Stores processed jobs in **Amazon DynamoDB**.
    - Exposes data via **API Gateway** and Lambda for frontend consumption.
4. **Frontend:**  
    - SPA hosted on **Amazon S3**, enabling users to browse, search, filter, and save jobs.

---

## 🧠 Key Learnings

- **Serverless Architecture:** Deepened expertise in AWS Lambda, S3, DynamoDB, API Gateway, and EventBridge.
- **Prompt Engineering:** Crafted effective prompts for LLMs to ensure structured, actionable outputs.
- **Web Scraping:** Navigated anti-bot measures and dynamic site structures.
- **Data Pipeline Design:** Built a robust, automated pipeline for data ingestion, processing, and delivery.
- **UI/UX for AI Data:** Focused on clear presentation of AI-generated insights.

---

## 🏆 Challenges Overcome

- **Web Scraping Robustness:** Adapted to dynamic HTML and anti-bot mechanisms; used sample data for reliability.
- **LLM Consistency:** Refined prompts for consistent, structured JSON outputs.
- **Lambda Timeouts:** Tuned configurations for longer Bedrock API calls.
- **Frontend-Backend Integration:** Ensured seamless data flow and client-side state management.

---

## 🌐 Live Demo

[**Explore Ajira Chapchap Jobs Here!**](http://ajira-chapchap-webapp-2026.s3-website.eu-central-1.amazonaws.com/)  
<sub>*(Replace with your actual S3 or CloudFront endpoint)*</sub>

---

## 🛠️ Architecture Overview

Ajira Chapchap runs on an event-driven, serverless AWS architecture:

```text
+---------------------+     +--------------------------+     +-----------------------+
|  EventBridge        | --> |  Lambda: scrapeJobs      | --> |  S3: Raw Jobs Bucket  |
+---------------------+     +--------------------------+     +-----------------------+
             |                               |                               |
             v                               v                               v
+---------------------+     +--------------------------+     +-----------------------+
|  Lambda: processJobs| --> |  Amazon Bedrock (Titan)  | --> |  DynamoDB: Jobs Table |
+---------------------+     +--------------------------+     +-----------------------+
             |                               |                               |
             v                               v                               v
+---------------------+     +--------------------------+     +-----------------------+
|  API Gateway        | --> |  Lambda: getJobsApi      | --> |  S3: Frontend Hosting |
+---------------------+     +--------------------------+     +-----------------------+
                                                                                  |
                                                                                  v
                                                                  +-----------------------+
                                                                  |  User's Web Browser   |
                                                                  +-----------------------+
```

### Component Breakdown

| Component                | Role/Function                          | Trigger/Event                                   | Description                                                                                                    |
|--------------------------|----------------------------------------|-------------------------------------------------|----------------------------------------------------------------------------------------------------------------|
| **scrapeJobsFunction**   | Data acquisition (Lambda)              | Scheduled by EventBridge                        | Collects raw job data (sample or scraped), stores JSON in S3.                                                  |
| **processJobsFunction**  | AI analysis (Lambda)                   | S3 Event Notification                           | Reads raw jobs, sends to Bedrock, enriches data, stores in DynamoDB.                                           |
| **getJobsApiFunction**   | Data delivery (Lambda)                 | HTTP GET via API Gateway                        | Fetches verified jobs from DynamoDB, returns JSON to frontend.                                                 |
| **Amazon S3**            | Static website hosting                 | N/A                                             | Hosts frontend files (`index.html`, `style.css`, `script.js`).                                                 |
| **Amazon API Gateway**   | API entry point                        | HTTP requests from frontend                     | Exposes REST API endpoint for job data.                                                                        |
| **Amazon Bedrock**       | AI model provider                      | Invoked by processJobsFunction                  | Summarizes, verifies, and categorizes jobs using Titan Text Express.                                           |
| **Amazon DynamoDB**      | NoSQL database                         | Invoked by processJobsFunction and API calls    | Stores processed, AI-enriched job listings.                                                                    |
| **Amazon EventBridge**   | Event scheduler                        | N/A                                             | Schedules scraping jobs periodically.                                                                          |
| **Amazon CloudFront**    | CDN (optional)                         | N/A                                             | Accelerates frontend delivery and adds security.                                                               |

---

## 🧰 Technologies Used

**Backend:**
- AWS Lambda (Python 3.9)
- Amazon Bedrock (Titan Text Express)
- Amazon S3
- Amazon DynamoDB
- Amazon API Gateway
- Amazon EventBridge
- Boto3 (AWS SDK for Python)

**Frontend:**
- HTML5
- CSS3 (Tailwind CSS)
- JavaScript
- Chart.js (for data visualization)

---

## ⚙️ Setup & Deployment (High-Level)

1. **AWS Account:** Ensure you have an active AWS account.
2. **IAM Permissions:** Create a user/role with permissions for Lambda, S3, DynamoDB, API Gateway, EventBridge, and Bedrock.
3. **S3 Buckets:**  
    - Raw Jobs: Stores raw job data, triggers processing Lambda.
    - Frontend: Hosts static website files.
4. **DynamoDB Table:**  
    - Table: `AjiraChapchapJobs` (Partition Key: `jobId`, GSI on `status` and `postedDate`).
5. **Lambda Functions:**  
    - Deploy `scrapeJobsFunction`, `processJobsFunction`, `getJobsApiFunction` (Python 3.9).
    - Attach IAM roles, add Lambda layers for dependencies.
    - Set environment variables (e.g., `DESTINATION_BUCKET`).
    - Adjust timeouts for Bedrock calls.
6. **API Gateway:**  
    - Create REST API, integrate with `getJobsApiFunction`.
7. **EventBridge:**  
    - Schedule `scrapeJobsFunction` to run periodically.
8. **Bedrock Model Access:**  
    - Enable Titan Text Express in your AWS region.
9. **Frontend Deployment:**  
    - Upload SPA files to S3, enable static website hosting.
    - Update API endpoint in `script.js`.

*For detailed deployment, see internal docs or setup guides.*

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for improvements, features, or bug fixes.

---

## 📄 License

This project is licensed under the MIT License.
