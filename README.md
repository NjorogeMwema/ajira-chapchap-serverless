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

## 💡 About the Project

### Inspiration

The inspiration for Ajira Chapchap stemmed from a critical observation of the job market for young people in Kenya. While there's a significant demand for entry-level talent, the online landscape is unfortunately riddled with fraudulent job postings and scams. These scams not only waste job seekers' time and resources but can also lead to financial exploitation. We envisioned a platform that could cut through the noise, providing a trusted and efficient way for Kenyan youth to find legitimate opportunities, empowering them to build their careers safely.

### How We Built It

We adopted a **serverless-first approach** on AWS to ensure scalability, cost-efficiency, and minimal operational overhead. The core of our solution revolves around three interconnected AWS Lambda functions, orchestrating the entire job verification pipeline:

1.  **Data Acquisition:** We initially explored web scraping live job boards using Python's `requests` and `BeautifulSoup`. While challenging due to anti-bot measures, this phase taught us the intricacies of HTML parsing and polite scraping practices. For robust demonstration, we pivoted to using a rich, pre-curated sample dataset within our `scrapeJobsFunction`.
2.  **AI-Powered Analysis:** This is where the magic happens. We integrated **Amazon Bedrock** and its **Titan Text Express** Foundation Model. By crafting precise prompts, we trained the model to perform complex tasks: summarizing job descriptions, assessing legitimacy (assigning a `verificationScore` and `flags`), and categorizing jobs into relevant industry sectors. This AI layer is crucial for transforming raw, unstructured data into valuable, actionable insights.
3.  **Data Persistence & Delivery:** Processed job data is stored in **Amazon DynamoDB**, a high-performance NoSQL database. This data is then exposed via **Amazon API Gateway**, which triggers another Lambda function to serve the jobs to our frontend.
4.  **User Interface:** The frontend is a responsive Single-Page Application built with HTML, Tailwind CSS, and JavaScript, hosted on **Amazon S3**. It provides a clean interface for users to browse, search, filter, and save jobs.

### What We Learned

Building Ajira Chapchap was an invaluable learning experience:

* **Serverless Architecture:** Deepened our understanding of AWS Lambda, S3, DynamoDB, API Gateway, and EventBridge, and how they seamlessly integrate to form a powerful, event-driven system.
* **Prompt Engineering:** Gained hands-on experience in crafting effective prompts for Large Language Models (LLMs) on Amazon Bedrock to achieve specific, structured outputs (JSON formatting, categorization, sentiment analysis).
* **Web Scraping Challenges:** Understood the complexities and ethical considerations of web scraping, including handling anti-bot measures and adapting to dynamic website structures.
* **Data Pipeline Design:** Learned to design a robust data pipeline that handles data ingestion, processing, storage, and delivery in an automated and scalable manner.
* **UI/UX for Data:** Focused on presenting complex AI-generated data (like verification scores and flags) in an easily digestible and trustworthy manner on the frontend.

### Challenges Faced

Our journey wasn't without its hurdles:

* **Web Scraping Robustness:** Reliably scraping dynamic job boards proved challenging due to frequent HTML changes and aggressive anti-bot mechanisms (e.g., `403 Forbidden` errors from Indeed.com). This led us to implement a robust fallback to sample data for consistent demonstration.
* **LLM Consistency:** Ensuring the Amazon Titan Text Express model consistently returned perfectly formatted JSON and adhered strictly to the predefined category list required iterative prompt refinement. Sometimes, the model would omit keys or provide slightly off-list categories, necessitating careful parsing and default handling.
* **Lambda Timeouts:** Initial Bedrock API calls within Lambda functions sometimes exceeded default timeouts, requiring us to carefully monitor logs and adjust Lambda configurations.
* **Frontend-Backend Integration:** Ensuring seamless data flow from DynamoDB through API Gateway to the frontend, including client-side filtering and state management, required meticulous debugging and testing.

Despite these challenges, overcoming them provided immense satisfaction and solidified our understanding of building intelligent, scalable cloud applications.

---

## 🚀 Live Demo

Experience Ajira Chapchap live!
[**Explore Ajira Chapchap Jobs Here!**](http://ajira-chapchap-webapp-2026.s3-website.eu-central-1.amazonaws.com/)
*(**IMPORTANT:** Replace this URL with your actual S3 static website endpoint or CloudFront URL)*

---

## 💡 How It Works: The Serverless Pipeline

Ajira Chapchap operates on a robust, event-driven serverless architecture on AWS. Each component plays a crucial role in delivering verified job opportunities.

### High-Level Architecture Diagram

*(For a visual diagram, we recommend creating an image using a tool like draw.io, Lucidchart, or any diagramming software, and then embedding it here. Example: `![Ajira Chapchap Architecture](images/architecture_diagram.png)`)*

```text
+---------------------+     +--------------------------+     +-----------------------+
|  EventBridge        |     |  Amazon S3               |     |  Amazon API Gateway   |
|  (Scheduler)        | --> |  (Raw Jobs Bucket)       | --> |  (REST API)           |
+---------------------+     +--------------------------+     +-----------------------+
          |                               |                               |
          |                               |                               |
          v                               v                               v
+---------------------+     +--------------------------+     +-----------------------+
|  Lambda             |     |  Lambda                  |     |  Lambda               |
|  (scrapeJobsFunction)|     |  (processJobsFunction)   |     |  (getJobsApiFunction) |
+---------------------+     +--------------------------+     +-----------------------+
          |                               |                               |
          |                               |                               |
          v                               v                               v
+---------------------+     +--------------------------+     +-----------------------+
|  (Raw Data)         |     |  Amazon Bedrock          |     |  Amazon DynamoDB      |
|                     |     |  (Titan Text Express)    | <-> |  (AjiraChapchapJobs)  |
+---------------------+     +--------------------------+     +-----------------------+
          |                               |                               |
          |                               |                               v
          |                               |                   +-----------------------+
          |                               |                   |  Amazon S3            |
          |                               |                   |  (Frontend Hosting)   |
          +---------------------------------------------------+-----------------------+
                                                              |
                                                              v
                                                  +-----------------------+
                                                  |  User's Web Browser   |
                                                  |  (Ajira Chapchap UI)  |
                                                  +-----------------------+

### 🧩 Detailed Component Breakdown

| Component                | Role/Function                          | Trigger/Event                                   | Action/Description                                                                                                                                                                                                                                                                      |
|--------------------------|----------------------------------------|-------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **scrapeJobsFunction**   | Data acquisition agent (AWS Lambda)    | Scheduled daily by Amazon EventBridge            | Collects raw job data (uses sample data for demo; in production, would scrape job boards). Stores raw JSON files in an S3 bucket (`ajira-chapchap-raw-jobs-YOURNAME-UNIQUEID`).                                                                                                         |
| **processJobsFunction**  | AI intelligence hub (AWS Lambda)       | S3 Event Notification (new raw job file upload)  | Reads raw job data from S3, sends descriptions to Amazon Bedrock (Titan Text Express), receives structured JSON (summary, verificationScore, flags, category), enriches data, and stores processed jobs in DynamoDB (`AjiraChapchapJobs` table).                                         |
| **getJobsApiFunction**   | Data delivery service (AWS Lambda)     | HTTP GET request via API Gateway                 | Queries DynamoDB for all verified and categorized job listings, returns job data as JSON through API Gateway to the frontend.                                                                                                                    |
| **Amazon S3**            | Static website hosting                 | N/A                                             | Hosts frontend files (`index.html`, `style.css`, `script.js`) for static website hosting.                                                                                                                                                        |
| **Amazon API Gateway**   | Secure API entry point                 | HTTP requests from frontend                      | Exposes REST API endpoint (`/jobs`) that triggers `getJobsApiFunction` Lambda.                                                                                                                                                                   |
| **Amazon Bedrock**       | Foundation Model provider              | Invoked by `processJobsFunction`                 | Performs AI analysis (summarization, verification, categorization) using Titan Text Express.                                                                                                                                                     |
| **Amazon DynamoDB**      | NoSQL database                         | Invoked by `processJobsFunction` and API calls   | Stores all processed, AI-enriched job listings for fast retrieval by the API.                                                                                                                                                                    |
| **Amazon EventBridge**   | Serverless event scheduler             | N/A                                             | Schedules `scrapeJobsFunction` to run periodically (e.g., daily) to keep job listings up-to-date.                                                                                                                                                |
| **Amazon CloudFront**    | Content Delivery Network (optional)    | N/A                                             | Speeds up frontend content delivery and adds security for static website hosting.                                                                                                                                                                |


🛠️ Technologies Used
Backend:

- **AWS Lambda** (Python 3.9)
- **Amazon Bedrock** (Titan Text Express)
- **Amazon S3**
- **Amazon DynamoDB**
- **Amazon API Gateway**
- **Amazon EventBridge**
- **Boto3** (AWS SDK for Python)

Frontend:

- **HTML5**
- **CSS3** (Tailwind CSS)
- **JavaScript**
- **Chart.js** (for data visualization in the infographic)

⚙️ Setup and Deployment (High-Level)
This project is deployed entirely on AWS. Here's a high-level overview of the setup:

AWS Account: Ensure you have an active AWS account.

IAM Permissions: Create an IAM user or role with necessary permissions for Lambda, S3, DynamoDB, API Gateway, EventBridge, and Bedrock (including access to amazon.titan-text-express-v1).

S3 Buckets:

- **Raw Jobs S3 Bucket:**  
    Stores raw job data files and triggers the `processJobsFunction` Lambda when new data is uploaded.

- **Frontend S3 Bucket:**  
    Hosts the static website files (HTML, CSS, JS) for the user interface.

DynamoDB Table: Create a table named AjiraChapchapJobs with jobId as the Partition Key and a Global Secondary Index on status and postedDate.

Lambda Functions:

- **Deploy Lambda Functions:**  
    - Deploy `scrapeJobsFunction`, `processJobsFunction`, and `getJobsApiFunction` using the Python 3.9 runtime.
- **IAM Roles & Layers:**  
    - Attach necessary IAM roles with permissions for S3, DynamoDB, Bedrock, and other required AWS services.
    - Add Lambda layers for dependencies such as `requests` and `BeautifulSoup4`.
- **Environment Variables:**  
    - Configure required environment variables (e.g., `DESTINATION_BUCKET`).
- **Lambda Timeouts:**  
    - Adjust Lambda timeouts, especially for `processJobsFunction`, to accommodate Bedrock API calls.
- **API Gateway:**  
    - Create a REST API endpoint and integrate it with `getJobsApiFunction`.
- **EventBridge:**  
    - Set up a scheduled rule to trigger `scrapeJobsFunction` periodically.
- **Bedrock Model Access:**  
    - Ensure access to the Titan Text Express model is enabled in your AWS region (`eu-central-1`).

Frontend Deployment: Upload index.html, style.css, and script.js to your frontend S3 bucket and enable static website hosting. Update the API_ENDPOINT in script.js to your deployed API Gateway URL.

(For detailed deployment instructions, refer to the project's internal documentation or a more extensive setup guide if available.)


🤝 Contributing
Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please open an issue or submit a pull request.

📄 License
This project is licensed under the MIT License.