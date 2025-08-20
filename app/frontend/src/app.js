import { renderChart, destroyChart, createDataset } from "./charts.js";
import { saveEmergencyFundScenarioToDB } from './emergency-fund.js';


// Global states
let currentScenario = ''; // ID of current selected scenario
let currentScenarioConfig = {}; // Config object of active scenario
let currentScenarioEndpoint = ''; // API endpoint for simulation
let fields = []; // DOM input elements (for current scenario)
let fieldValues = {}; // Store current input values

const field = (id, label, min, step, def, type='number') => ({ id, label, min, step, default: def, type});

const scenariosConfig = {
    emergency_fund: {
        label: "Building an Emergency Fund",
        endpoint: "/simulate/emergency-fund",
        fields: [
            field("monthly_expenses", "Monthly Expenses (₱)", 0, 1000, 10000),
            field("months_of_expenses", "Desired Months to Cover", 0, 1, 3),
            field("current_emergency_savings", "Current Emergency Savings (₱)", 0, 500, 5000),
            field("monthly_savings", "Monthly Savings Contribution (₱)", 0, 500, 500),
            field("annual_interest_rate_percent", "Annual Interest Rate (%)", 0, 1, 0),
            field("scenario_title", "What If Scenario Title", null, null, "My Current Situation", 'text'),
            field("scenario_color", "Scenario Color", null, null, "#007bff", 'color'),
        ],
    },
    budgeting: {
        label: "Effective Budgeting and Expense Tracking",
        endpoint: "/simulate/budgeting",
        fields: [
            field("income", "Monthly Income (₱)", 0, 1000, 40000),
            field("fixed_expenses", "Fixed Monthly Expenses (₱)", 0, 500, 15000),
            field("target_savings", "Target Monthly Savings (₱)", 0, 1000, 5000),
            field("discretionary_pct", "Discretionary Spending (% of Income)", 0, 1, 20),
            field("scenario_title", "What If Scenario Title", null, null, "My Current Situation", 'text'),
        ],
    },
    debt_management: {
        label: "Managing and Reducing Debt",
        endpoint: "/simulate/debt-management",
        fields: [
            field("debt", "Total Debt Amount (₱)", 0, 10000, 200000),
            field("interest_rate", "Annual Interest Rate (%)", 0, 0.5, 10),
            field("monthly_payment", "Current Monthly Debt Payment (₱)", 0, 1000, 5000),
            field("extra_payment", "Additional Monthly Payment (₱)", 0, 500, 2000),
            field("scenario_title", "What If Scenario Title", null, null, "My Current Situation", 'text'),
        ],
    },
    investing: {
        label: "Starting to Save and Invest for the Future",
        endpoint: "/simulate/investing",
        fields: [
            field("initial", "Current Investment/Savings Amount (₱)", 0, 10000, 100000),
            field("years", "Investment Horizon (Years)", 0, 1, 10),
            field("monthly", "Monthly Contribution (₱)", 0, 500, 5000),
            field("return_rate", "Expected Annual Return (%)", 0, 0.1, 6),
            field("scenario_title", "What If Scenario Title", null, null, "My Current Situation", 'text'),
        ],
    },
    education_funding: {
        label: "Education Funding",
        endpoint: "/simulate/education-fund",
        fields: [
            field("today_cost", "Target Education Cost (Today) (₱)", 0, 50000, 1000000),
            field("years", "Years Until Enrollment", 0, 1, 5),
            field("current_savings", "Current Education Savings (₱)", 0, 10000, 100000),
            field("inflation_rate", "Annual Education Inflation Rate (%)", 0, 0.1, 4),
            field("monthly_contrib", "Monthly Savings Contribution (₱)", 0, 500, 3000),
            field("return_rate", "Expected Annual Investment Return (%)", 0, 0.1, 5),
            field("scenario_title", "What If Scenario Title", null, null, "My Current Situation", 'text'),
        ],
    },
    major_purchase: {
        label: "Major Purchase Planning",
        endpoint: "/simulate/major-purchase",
        fields: [
            field("price", "Target Purchase Price (₱)", 0, 100000, 3000000),
            field("down_pct", "Desired Down Payment (%)", 0, 1, 20),
            field("years_to_save", "Years to Save for Down Payment", 0, 1, 3),
            field("current_savings", "Current Savings (₱)", 0, 10000, 200000),
            field("loan_rate", "Loan Interest Rate (Annual %)", 0, 0.1, 8),
            field("monthly_contrib", "Monthly Savings Contribution (₱)", 0, 1000, 10000),
            field("savings_return", "Expected Annual Savings Return (%)", 0, 0.1, 3),
            field("loan_term", "Loan Term (Years)", 0, 1, 15),
            field("scenario_title", "What If Scenario Title", null, null, "My Current Situation", 'text'),
        ],
    },
};

const home = document.getElementById('home');
// const homeGreetings = document.getElementById('greetings');
const dashboard = document.getElementById('dashboard');
const scenarioTitleElement = document.getElementById('scenario-title');

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
    dashboard.style.width = '100%';
    home.style.width = '0';

    renderChart(currentScenario); // Draw scenario-specific chart after form is set up
}

function showHome() {
    // Toggle dashboard to home
    console.log('Closing dashboard...');

    dashboard.style.width = '0';
    home.style.width = '100%';
    scenarioTitleElement.textContent = '';

    destroyChart();
}

async function runSimulation(endpoint, params) {
    // Prepare request payload (parameters for simulation scenario)
    const requestBody = params;

    // Extract scenario-specific details fo visualization
    const scenarioTitle = requestBody.scenario_title;
    const scenarioColor = requestBody.scenario_color;

    try {
        console.log('Running simulation...');

        // Send a POST request to the FastAPI backend
        // Using localhost (127.0.0.1:8000) since backend is served by uvicorn
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

        // Extract what inputs the backend received (for debugging & validation)
        const inputsReceived = result.inputs_received;
        console.log('Inputs Received: ', inputsReceived);

        // Extract simulation outputs for frontend
        const data = result.data.projection_data.balance_history;
        const labels = result.data.projection_data.months_labels;
        const summary = result.data.summary;

        // Save the Emergency Fund scenario to the db
        const savedScenario = await saveEmergencyFundScenarioToDB(params);

        // Feed proceessed data into chart layer
        // Each new scenario gets a unique color + title for comparison
        createDataset(scenarioTitle, scenarioColor, data, labels, summary, savedScenario.id);

    } catch (err) {
        console.error('Fetch error:', err);
    }
}

function renderAIResponses(ai_explanation, ai_suggestions) {
    // Prepare container for AI responses
    const exContainer = document.getElementById('explain');
    const suContainer = document.getElementById('suggest');

    // Clear previous AI responses before injecting new ones
    exContainer.innerHTML = '';
    suContainer.innerHTML = '';

    // Grab reusable AI response template from DOM (for explanation and suggestions)
    const aiResponseTemplate = document.getElementById('ai-response-template');
    if (!aiResponseTemplate) {
        console.error('AI response template not found.');
        return;
    }

    // AI explanation
    const explanationNode = aiResponseTemplate.content.cloneNode(true);
    explanationNode.querySelector('p').textContent = ai_explanation;
    exContainer.appendChild(explanationNode);

    // AI suggestions
    const suggestions = ai_suggestions.join('\n\n');
    const suggestionNode = aiResponseTemplate.content.cloneNode(true);
    suggestionNode.querySelector('p').textContent = suggestions;
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

// Reset all form fields to empty
document.getElementById('clear-btn').addEventListener('click', function() {
    console.log("Fields cleared.")
    fields.forEach((input) => {
        if (input.type === 'color') input.value = '#000000';
        else input.value = null;
    });
})

// Run simulation when form is submitted
document.getElementById('simulate-btn').addEventListener('click', async (event) => {
    // Prevent default page reload
    // Pass chosen scenario and collected input values to backend
    runSimulation(currentScenarioEndpoint, fieldValues);
});


