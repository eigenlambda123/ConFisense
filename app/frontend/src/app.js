import { 
    renderChart, 
    destroyChart, 
    addDatasets, 
    updateChartTitle, 
    clearChartTitle
} from "./charts.js";

import { 
    saveEmergencyFundScenarioToDB,
    getEmergencyFundAISuggestion,
    getEmergencyFundAIExplaination,
    getEmergencyFundAISummary 
} from './emergency-fund.js';

// Global states
let currentScenario = ''; // ID of current selected scenario
let currentScenarioConfig = {}; // Config object of active scenario
let currentScenarioEndpoint = ''; // API endpoint for simulation
let fields = []; // DOM input elements (for current scenario)
let fieldValues = {}; // Store current input values

const field = (id, label, min, step, def, type='number') => ({id, label, min, step, default: def, type});

const scenariosConfig = {
    budget_optimization: {
        label: "Manage My Family's Budget",
        endpoint: "/simulate/budget-optimization",
        fields: [
            // General Parameters
            field("projection_months", "Projection Months", 12, 1, 12),

            // Income Fields
            field("monthly_net_income", "Monthly Net Income (₱)", 0, 1000, 50000),
            field("other_monthly_income", "Other Monthly Income (₱)", 0, 500, 0),

            // Fixed Needs Expenses
            field("rent_mortgage", "Rent / Mortgage (₱)", 0, 1000, 15000),
            field("utilities", "Utilities (₱)", 0, 500, 4000),
            field("loan_payments", "Loan Payments (₱)", 0, 100, 0),
            field("insurance_premiums", "Insurance Premiums (₱)", 0, 100, 0),
            field("tuition_fees", "Tuition & Fees (₱)", 0, 1000, 0),
            field("groceries", "Groceries (₱)", 0, 500, 8000),
            field("transportation", "Transportation (₱)", 0, 500, 3000),
            
            // Variable Needs Expenses
            field("household_supplies", "Household Supplies (₱)", 0, 100, 500),
            field("medical_health", "Medical & Health (₱)", 0, 100, 0),
            field("misc_needs", "Miscellaneous Needs (₱)", 0, 100, 0),

            // Wants & Discretionary Expenses
            field("dining_out", "Dining Out (₱)", 0, 100, 2500),
            field("entertainment_hobbies", "Entertainment & Hobbies (₱)", 0, 100, 1500),
            field("personal_care", "Personal Care (₱)", 0, 100, 0),
            field("shopping_leisure", "Shopping & Leisure (₱)", 0, 100, 0),
            field("travel_vacation", "Travel & Vacation (₱)", 0, 1000, 0),
            field("misc_wants", "Miscellaneous Wants (₱)", 0, 100, 0),

            // Savings Goals Fields
            field("target_monthly_savings", "Target Monthly Savings (₱)", 0, 100, 5000),
            field("emergency_fund_target", "Emergency Fund Target (₱)", 0, 1000, 120000),
        ],
    },
    budgeting: {
        label: "Plan Business Growth & Debt",
        endpoint: "/simulate/",
        fields: [],
    },
    debt_management: {
        label: "Grow My Client's Wealth",
        endpoint: "/simulate/",
        fields: [],
    },
    investing: {
        label: "Plan for the Future",
        endpoint: "/simulate/",
        fields: [],
    },
    education_funding: {
        label: "Manage My Capital",
        endpoint: "/simulate/",
        fields: [],
    },
    major_purchase: {
        label: "Analyze Client Portfolios",
        endpoint: "/simulate/",
        fields: [],
    },
};

// Prepare DOM elements
const home = document.getElementById('home');
const greetingsContainer = document.getElementById(('greetings-container'));
const cardButton = document.getElementsByClassName('card-btn');
const scenarioName = document.getElementsByClassName('scenario-name');
const scenarioDescription = document.getElementsByClassName('scenario-desc');
const scenarioIcon = document.getElementsByClassName('scenario-icon');
const dashboard = document.getElementById('dashboard');
const scenarioTitleElement = document.getElementById('scenario-title');
const exContainer = document.getElementById('explanation');
const suContainer = document.getElementById('suggestions');
const messageBox = document.getElementById('msg-box');
const messageText = document.getElementById('msg-text');

// Helper function to show custom message box
function showMessage(message) {
    messageText.textContent = message;
    messageBox.style.display = 'block';
}

function openDashboard() {
    dashboard.classList.add('active');
    home.classList.add('active');
    greetingsContainer.classList.add('active');

    for (let i=0; i<cardButton.length; i++) {
        cardButton[i].classList.add('active');
        scenarioName[i].classList.add('active');
        scenarioDescription[i].classList.add('active');
        scenarioIcon[i].classList.add('active');
    }
}

function closeDashboard() {
    dashboard.classList.remove('active');
    home.classList.remove('active');
    greetingsContainer.classList.remove('active');

    for (let i=0; i<cardButton.length; i++) {
        cardButton[i].classList.remove('active');
        scenarioName[i].classList.remove('active');
        scenarioDescription[i].classList.remove('active');
        scenarioIcon[i].classList.remove('active');
    }
}

function showDashboard(buttonElement) {
    // Identify which scenario button was clicked
    const scenarioKey = buttonElement.dataset.scenario;
    currentScenario = scenarioKey;

    // Load scenario-specific configuration
    const config = scenariosConfig[scenarioKey];
    currentScenarioConfig = config;
    currentScenarioEndpoint = config.endpoint;

    if (!config) {
        console.error(`Configuration for ${scenarioKey} not found.`);
        return;
    }

    // Display current scenario title in dashboard
    scenarioTitleElement.textContent = currentScenarioConfig.label;

    // Prepare container for form fields (reset old ones if switching scenarios)
    const fieldContainer = document.getElementById('field-container');
    fieldContainer.innerHTML = '';

    // Reset state for fields and values
    fields = [];
    fieldValues = {};

    // Grab reusable field template from DOM (for each input field)
    const fieldTemplate = document.getElementById('field-template');
    if (!fieldTemplate) {
        console.error('Field template not found.');
        return;
    }

    // Dynamically generate input fields based on scenario config
    currentScenarioConfig.fields.forEach(field => {
        // Clone the template's content
        const fieldClone = fieldTemplate.content.cloneNode(true);
        const wrapper = fieldClone.querySelector('div');
        const label = fieldClone.querySelector('label');
        const input = fieldClone.querySelector('input');

        // Set label and input attributes from scenario data
        label.textContent = field.label;
        label.htmlFor = field.id;
        input.type = field.type;
        input.value = field.default;
        input.id = field.id;

        if (field.type !== 'color') {
            input.classList.add('non-color-input');
        }

        if (field.type === 'number') {
            input.min = field.min;
            input.step = field.step;
        }

        // Event listener to input (for API call and formula calculation)
        input.addEventListener('input', function() {
            fieldValues[input.id] = input.type === 'number' ? Number(input.value) : input.value;
        });
      
        // Initialize field state
        fields.push(input);
        fieldValues[input.id] = input.type === 'number' ? Number(input.value) : input.value;

        // Render field into dashboard
        fieldContainer.appendChild(fieldClone);
    });

    // Toggle home to dashboard
    console.log('Opening dashboard...');
    openDashboard();
    clearChartTitle();
    //clearAIResponses();
    renderChart(currentScenario); // Draw scenario-specific chart after form is set up
}

function showHome() {
    // Toggle dashboard to home
    console.log('Closing dashboard...');
    scenarioTitleElement.textContent = '';
    closeDashboard();
    clearChartTitle();
    //clearAIResponses();
    destroyChart();
}

function transformFrontendData(data) {
    const apiBody = {
        scenario_type: data.scenario_type,
        user_type: data.user_type,
        projection_months: data.projection_months,
        income: {
            monthly_net_income: data.monthly_net_income,
            other_monthly_income: data.other_monthly_income,
            income_frequency: "monthly"
        },
        expenses: {
            fixed_needs: {
                rent_mortgage: data.rent_mortgage,
                utilities: data.utilities,
                loan_payments: data.loan_payments,
                insurance_premiums: data.insurance_premiums,
                tuition_fees: data.tuition_fees,
                groceries: data.groceries,
                transportation: data.transportation
            },
            variable_needs: {
                household_supplies: data.household_supplies,
                medical_health: data.medical_health,
                misc_needs: data.misc_needs
            },
            wants_discretionary: {
                dining_out: data.dining_out,
                entertainment_hobbies: data.entertainment_hobbies,
                personal_care: data.personal_care,
                shopping_leisure: data.shopping_leisure,
                travel_vacation: data.travel_vacation,
                misc_wants: data.misc_wants
            }
        },
        savings_goals: {
            target_monthly_savings: data.target_monthly_savings,
            emergency_fund_target: data.emergency_fund_target
        }
    };

    return apiBody;
}

async function runSimulation(endpoint, params) {
    // Prepare request payload (parameters for simulation scenario)
    console.log(params);
    const requestBody = transformFrontendData(params);

    console.log(requestBody); // FOR DEBUGGING

    try {
        console.log('Running simulation...');

        // Send a POST request to the FastAPI backend
        const response = await fetch(`http://127.0.0.1:8000${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Ensure backend interprets body as JSON
            },
            body: JSON.stringify(requestBody) // Pass scenario parameters to backend
        });

        // Throw error if request didn't succeed
        if (!response.ok) throw new Error('Request failed');

        // Parse backend JSON response (contains simulation results)
        const result = await response.json();
        const chartData = result.data.chart_data;
        const inputsReceived = result.data.inputs_received;
        const formulas = result.data.show_my_math;
        
        // FOR DEBUGGING
        console.log('Result: ', result);
        console.log('Chart Data: ', chartData);
        console.log('Inputs Received: ', inputsReceived);
        console.log('Formulas: ', formulas); 

        addDatasets(chartData);
        fetchAndRenderAISummary();

    } catch (err) {
        console.error('Fetch error:', err);
    }
}

async function fetchAndRenderAISummary() {
    try {
        console.log('Fetching AI Summary...');
        const summaryResult = await getEmergencyFundAISummary();
        const ai_summary = summaryResult.summary || "No summary available.";
        updateChartTitle(ai_summary);

    } catch (error) {
        console.error('Error fetching AI summary:', error);
    }
}

async function fetchAndRenderAIExplanation() {
    try {
        console.log('Fetching AI Explanation...');
        const explanationResult = await getEmergencyFundAIExplaination();
        const ai_explanation = explanationResult.ai_explanation || 'No explanation available.';

        // Grab reusable AI response template from DOM (for explanation and suggestions)
        const aiResponseTemplate = document.getElementById('ai-response-template');
        if (!aiResponseTemplate) {
            console.error('AI response template not found.');
            return;
        }

        exContainer.innerHTML = '';

        const explanationNode = aiResponseTemplate.content.cloneNode(true);
        explanationNode.querySelector('p').textContent = ai_explanation;
        exContainer.appendChild(explanationNode);
    }

    catch (error) {
        console.error('Error fetching AI explanation:', error);
    }
}

async function fetchAndRenderAISuggestions() {
    try {
        console.log('Fetching AI Suggestions...');
        const suggestionResult = await getEmergencyFundAISuggestion();
        const ai_suggestions = suggestionResult.ai_suggestions || [];

        // Grab reusable AI response template from DOM (for explanation and suggestions)
        const aiResponseTemplate = document.getElementById('ai-response-template');
        if (!aiResponseTemplate) {
            console.error('AI response template not found.');
            return;
        }

        suContainer.innerHTML = '';

        // AI suggestions
        const suggestionsNode = aiResponseTemplate.content.cloneNode(true);
        suggestionsNode.querySelector('p').textContent = Array.isArray(ai_suggestions) && ai_suggestions.length > 0
            ? ai_suggestions.join('\n\n\n') // Joins array elements with two newlines for readability
            : "No specific suggestions available at this time."; // Fallback if array is empty or not an array
        suContainer.appendChild(suggestionsNode);
    }

    catch (error) {
        console.error('Error fetching AI suggestions:', error);
    }
}

function clearAIResponses() {
    // Clear previous AI responses before injecting new ones
    exContainer.innerHTML = '';
    suContainer.innerHTML = '';
    console.log('AI responses cleared.');
}

// Helper function to check if any input fields are empty
function areInputFieldsEmpty() {
    for (const field of fields) {
        // Trim whitespace for text inputs before checking for emptiness
        if (field.type === 'text' || field.type === 'color') {
            if (field.value.trim() === '') {
                return true;
            }
        } else if (field.value === null || field.value === '') {
            // For number inputs, an empty string or null can indicate emptiness
            return true;
        }
    }
    return false;
}

// Attach click handler to all scenario card buttons at home
document.querySelectorAll('.card-btn').forEach(button => {
    button.addEventListener('click', function() {
        showDashboard(this);
    });
});

// Handle navigation back to home
document.getElementById('back-btn').addEventListener('click', function() {
    showHome();
});

document.getElementById('clear-btn').addEventListener('click', function() {
    // Reset all form fields to empty
    fields.forEach((input) => {
        if (input.type === 'color') input.value = '#000000';
        else input.value = null;
    });
    console.log("Fields cleared.");
})

document.getElementById('simulate-btn').addEventListener('click', async (event) => {
    // Pass chosen scenario and collected input values to backend
    if (areInputFieldsEmpty()) {
        showMessage("Please fill in all input fields before running the simulation.");
        console.warn("Simulation prevented: Some input fields are empty.");
        return; // Stop the function if fields are empty
    }
    runSimulation(currentScenarioEndpoint, fieldValues);
});

document.getElementById('explain-btn').addEventListener('click', async (event) => {
    await fetchAndRenderAIExplanation();
});

document.getElementById('suggest-btn').addEventListener('click', async (event) => {
    await fetchAndRenderAISuggestions();
});

document.getElementById('close-msg-btn').addEventListener('click', function() {
    messageBox.style.display = 'none';
});