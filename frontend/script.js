// --- CONFIGURATION ---
// IMPORTANT: Replace this with your actual API Gateway invoke URL
// This URL should point to the endpoint that returns job listings in JSON format.
const API_ENDPOINT = 'https://jppvlwvuy8.execute-api.eu-central-1.amazonaws.com/prod/jobs'; 

// --- DOM ELEMENTS ---
const jobListings = document.getElementById('job-listings');
const searchBar = document.getElementById('search-bar');
const loader = document.getElementById('loader');
const errorMessage = document.getElementById('error-message');
const noJobsMessage = document.getElementById('no-jobs-message');
const allJobsTab = document.getElementById('all-jobs-tab');
const savedJobsTab = document.getElementById('saved-jobs-tab');
const savedCountBadge = document.getElementById('saved-count');
const categoryFilter = document.getElementById('category-filter');

// --- STATE MANAGEMENT ---
let allJobs = [];
let savedJobIds = new Set(JSON.parse(localStorage.getItem('ajiraChapchapSavedJobs') || '[]'));
let currentView = 'all'; // Can be 'all' or 'saved'
let currentCategory = 'all'; // Default category filter

// --- CORE FUNCTIONS ---

/**
 * Fetches job data from the API Gateway endpoint.
 * This is an asynchronous function that uses the Fetch API.
 */
async function fetchJobs() {
    // Show loader while fetching
    loader.style.display = 'flex';
    errorMessage.style.display = 'none';
    jobListings.style.display = 'none';
    noJobsMessage.style.display = 'none';
    
    // A basic check to prevent a failed request if the placeholder URL is not replaced.
    if (API_ENDPOINT.includes('YOUR_API_GATEWAY_INVOKE_URL_HERE')) {
        console.error("API Endpoint not configured. Please update the `API_ENDPOINT` variable.");
        loader.style.display = 'none';
        errorMessage.querySelector('p').textContent = 'API endpoint is not configured.';
        errorMessage.querySelector('.text-sm').textContent = 'Please update the JavaScript code with your API Gateway URL.';
        errorMessage.style.display = 'block';
        return;
    }

    try {
        const response = await fetch(API_ENDPOINT);
        if (!response.ok) {
            throw new Error(`API request failed with status: ${response.status}`);
        }
        const jobs = await response.json();
        allJobs = jobs;
        populateCategories(allJobs);
        applyFiltersAndRender();
    } catch (error) {
        console.error("Error fetching jobs:", error);
        loader.style.display = 'none';
        errorMessage.style.display = 'block';
    }
}

/**
 * Renders job cards into the DOM based on the current view and applied filters.
 */
function applyFiltersAndRender() {
    loader.style.display = 'none';
    jobListings.innerHTML = ''; // Clear previous listings

    const searchTerm = searchBar.value.toLowerCase();
    let jobsToDisplay = [];

    if (currentView === 'all') {
        jobsToDisplay = allJobs;
    } else { // 'saved' view
        jobsToDisplay = allJobs.filter(job => savedJobIds.has(job.jobId));
    }
    
    // Apply search filter
    jobsToDisplay = jobsToDisplay.filter(job => 
        (job.title && job.title.toLowerCase().includes(searchTerm)) ||
        (job.company && job.company.toLowerCase().includes(searchTerm))
    );

    // Apply category filter
    if (currentCategory !== 'all') {
        jobsToDisplay = jobsToDisplay.filter(job =>
            (job.category && job.category.toLowerCase() === currentCategory.toLowerCase())
        );
    }

    jobListings.style.display = 'grid';

    if (jobsToDisplay.length === 0) {
        noJobsMessage.style.display = 'block';
        return;
    }
    noJobsMessage.style.display = 'none';

    jobsToDisplay.forEach(job => {
        const card = createJobCard(job);
        jobListings.appendChild(card);
    });
}

/**
 * Populates the category filter dropdown with unique categories from fetched jobs.
 * @param {Array} jobs - The list of all jobs to extract categories from.
 */
function populateCategories(jobs) {
    const categories = new Set();
    jobs.forEach(job => {
        if (job.category) {
            categories.add(job.category);
        }
    });

    categoryFilter.innerHTML = '<option value="all">All Categories</option>';
    Array.from(categories).sort().forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = category;
        categoryFilter.appendChild(option);
    });

    categoryFilter.value = currentCategory;
}

/**
 * Creates a single job card HTML element.
 * @param {object} job - The job data object.
 * @returns {HTMLElement} - The created card element.
 */
function createJobCard(job) {
    const card = document.createElement('div');
    card.className = 'job-card bg-white rounded-xl shadow-lg p-6 flex flex-col'; /* Updated shadow and rounded */
    
    const verificationScore = job.scamAnalysis.score;
    const scoreColor = getScoreColor(verificationScore);
    const isSaved = savedJobIds.has(job.jobId);
    const scamFlags = job.scamAnalysis.flags.length > 0 ? job.scamAnalysis.flags.join(', ') : 'No specific flags identified.'; /* Improved message */
    const category = job.category || 'Uncategorized';

    card.innerHTML = `
        <div class="flex-grow">
            <div class="flex justify-between items-start mb-3">
                <h3 class="text-xl font-bold text-gray-900 leading-tight pr-2">${job.title}</h3>
                <div class="tooltip flex-shrink-0 ml-2">
                     <div class="text-base font-bold py-1 px-3 rounded-full text-white ${scoreColor} shadow-md">
                         ${verificationScore}%
                     </div>
                     <span class="tooltiptext">${scamFlags}</span>
                </div>
            </div>
            <p class="text-lg text-gray-700 font-semibold mb-2">${job.company}</p>
            <p class="text-sm text-gray-500 mb-1">Category: <span class="font-medium text-indigo-700">${category}</span></p>
            <p class="text-sm text-gray-500">Posted: ${new Date(job.postedDate).toLocaleDateString()}</p>
            <p class="text-gray-700 mt-4 text-base leading-relaxed line-clamp-4">${job.summary}</p>
        </div>
        <div class="mt-6 pt-4 border-t border-gray-200 flex justify-between items-center">
            <a href="${job.originalUrl}" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 hover:underline text-base font-semibold flex items-center transition-colors">
                View Original Post 
                <svg class="ml-1 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
            </a>
            <button class="save-button text-3xl transition-transform transform hover:scale-110 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50" data-job-id="${job.jobId}" title="${isSaved ? 'Unsave job' : 'Save job'}">
                ${isSaved ? '❤️' : '🤍'}
            </button>
        </div>
    `;
    return card;
}

function handleSaveToggle(event) {
    const button = event.target.closest('.save-button');
    if (!button) return;

    const jobId = button.dataset.jobId;
    if (savedJobIds.has(jobId)) {
        savedJobIds.delete(jobId);
        button.innerHTML = '🤍';
        button.title = 'Save job';
    } else {
        savedJobIds.add(jobId);
        button.innerHTML = '❤️';
        button.title = 'Unsave job';
    }
    
    updateSavedStateAndBadge();
    
    if (currentView === 'saved') {
        applyFiltersAndRender();
    }
}

function updateSavedStateAndBadge() {
    localStorage.setItem('ajiraChapchapSavedJobs', JSON.stringify(Array.from(savedJobIds)));
    savedCountBadge.textContent = savedJobIds.size;
}

function switchView(view) {
    currentView = view;
    if (view === 'all') {
        allJobsTab.classList.add('bg-blue-600', 'text-white', 'shadow-md', 'ring-2', 'ring-indigo-300');
        allJobsTab.classList.remove('bg-gray-200', 'text-gray-700', 'hover:bg-gray-300');
        
        savedJobsTab.classList.remove('bg-blue-600', 'text-white', 'shadow-md', 'ring-2', 'ring-indigo-300');
        savedJobsTab.classList.add('bg-indigo-500', 'text-white', 'hover:bg-indigo-600'); /* Adjusted saved tab style */
        
        searchBar.parentElement.style.display = 'flex';
    } else { // 'saved' view
        savedJobsTab.classList.add('bg-blue-600', 'text-white', 'shadow-md', 'ring-2', 'ring-indigo-300');
        savedJobsTab.classList.remove('bg-indigo-500', 'text-white', 'hover:bg-indigo-600'); /* Adjusted saved tab style */
        
        allJobsTab.classList.remove('bg-blue-600', 'text-white', 'shadow-md', 'ring-2', 'ring-indigo-300');
        allJobsTab.classList.add('bg-gray-200', 'text-gray-700', 'hover:bg-gray-300');
        
        searchBar.parentElement.style.display = 'none';
    }
    applyFiltersAndRender();
}

function getScoreColor(score) {
    if (score > 85) return 'bg-green-600'; /* Slightly darker green */
    if (score >= 60) return 'bg-yellow-500';
    return 'bg-red-600'; /* Slightly darker red */
}

// --- EVENT LISTENERS ---
searchBar.addEventListener('input', applyFiltersAndRender);
categoryFilter.addEventListener('change', () => {
    currentCategory = categoryFilter.value;
    applyFiltersAndRender();
});
jobListings.addEventListener('click', handleSaveToggle);
allJobsTab.addEventListener('click', () => switchView('all'));
savedJobsTab.addEventListener('click', () => switchView('saved'));

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    fetchJobs();
    updateSavedStateAndBadge();
    // Set current year in footer
    document.getElementById('current-year').textContent = new Date().getFullYear();
});