import { 
    renderChart, 
    destroyChart, 
    addDatasets, 
    updateChartTitle, 
    clearChartTitle
} from "./charts.js";

// Global states
let currentScenario = ''; // ID of current selected scenario
let currentScenarioConfig = {}; // Config object of active scenario
let currentScenarioEndpoint = ''; // API endpoint for simulation
let fields = []; // DOM input elements (for current scenario)
let fieldValues = {}; // Store current input values
let formulas = [];

const field = (id, label, category, min, step, def, type='number') => ({id, label, category, min, step, default: def, type});

const scenariosConfig = {
    budget_optimization: {
        label: "Manage My Family's Budget",
        endpoint: "/simulate/budget-optimization",
        fields: [
            // General Parameters
            field("projection_months", "Projection Months", "General", 12, 1, 12),

            // Income Fields
            field("monthly_gross_income", "Monthly Gross Income (₱)", "Income", 0, 1000, 50000),
            field("other_monthly_income", "Other Monthly Income (₱)", "Income", 0, 500, 0),

            // Fixed Needs Expenses
            field("rent", "Rent (₱)", "Fixed Needs", 0, 1000, 15000),
            field("utilities", "Utilities (₱)", "Fixed Needs", 0, 500, 4000),
            field("loan_payments", "Loan Payments (₱)", "Fixed Needs", 0, 100, 0),
            field("insurance_premiums", "Insurance Premiums (₱)", "Fixed Needs", 0, 100, 0),
            field("tuition_fees", "Tuition & Fees (₱)", "Fixed Needs", 0, 1000, 0),
            field("groceries", "Food & Groceries (₱)", "Fixed Needs", 0, 500, 8000),
            field("transportation", "Transportation (₱)", "Fixed Needs", 0, 500, 3000),
            
            // Variable Needs Expenses
            field("household_supplies", "Household Supplies (₱)", "Variable Needs", 0, 100, 500),
            field("medical_health", "Medical & Health (₱)", "Variable Needs", 0, 100, 0),
            field("misc_needs", "Miscellaneous Needs (₱)", "Variable Needs", 0, 100, 0),

            // Wants & Discretionary Expenses
            field("dining_out", "Dining Out (₱)", "Wants", 0, 100, 2500),
            field("entertainment_hobbies", "Entertainment & Hobbies (₱)", "Wants", 0, 100, 1500),
            field("personal_care", "Personal Care (₱)", "Wants", 0, 100, 0),
            field("shopping_leisure", "Shopping & Leisure (₱)", "Wants", 0, 100, 0),
            field("travel_vacation", "Travel & Vacation (₱)", "Wants", 0, 1000, 0),
            field("misc_wants", "Other Wants (₱)", "Wants", 0, 100, 0),

            // Savings Goals Fields
            field("target_monthly_savings", "Target Monthly Savings (₱)", "Goals", 0, 100, 5000),
            field("emergency_fund_target", "Emergency Fund Target (₱)", "Goals", 0, 1000, 120000),

            // What-if Factors
            field('income_growth_rate', 'Income Growth Rate (%)', "What-If Factors (Monthly)", 0, 100, 0),
            field('wants_reduction_rate', 'Wants Reduction Rate (%)', "What-If Factors (Monthly)", 0, 100, 0),
            field('savings_increase_rate', 'Savings Increase Rate (%)', "What-If Factors (Monthly)", 0, 100, 0)
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
function showMessage(message, className) {
    messageBox.classList.add(className);
    messageText.innerHTML = message;
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
    formulas = [];

    // Grab reusable field template from DOM (for each input field)
    const fieldTemplate = document.getElementById('field-template');
    if (!fieldTemplate) {
        console.error('Field template not found.');
        return;
    }

    let currentCategory = null;
    let firstCategory = true;

    // Dynamically generate input fields based on scenario config
    currentScenarioConfig.fields.forEach(field => {

        if (field.category && field.category != currentCategory) {
            // Create new heading element for category
            const categoryHeading = document.createElement('h3');
            categoryHeading.textContent = field.category;
            categoryHeading.classList.add('category-label');
            
            if (firstCategory) { firstCategory = false }
            else {
                const lineBreak = document.createElement('hr');
                lineBreak.classList.add('category-line');
                fieldContainer.appendChild(lineBreak);
            }

            fieldContainer.appendChild(categoryHeading);
            currentCategory = field.category; // Update the current category
        }

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
    openDashboard();
    clearChartTitle();
    //clearAIResponses();
    renderChart(currentScenario);
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

// Only for budget optimization for now
const buildRequestBody = (flatData) => {
    const body = {
        scenario_type: flatData.scenario_type,
        user_type: flatData.user_type,
        projection_months: flatData.projection_months,
        income: {
            monthly_gross_income: flatData.monthly_gross_income,
            other_monthly_income: flatData.other_monthly_income,
            income_frequency: "monthly"
        },
        expenses: {
            fixed_needs: {
                rent: flatData.rent,
                utilities: flatData.utilities,
                loan_payments: flatData.loan_payments,
                insurance_premiums: flatData.insurance_premiums,
                tuition_fees: flatData.tuition_fees,
                groceries: flatData.groceries,
                transportation: flatData.transportation
            },
            variable_needs: {
                household_supplies: flatData.household_supplies,
                medical_health: flatData.medical_health,
                misc_needs: flatData.misc_needs
            },
            wants_discretionary: {
                dining_out: flatData.dining_out,
                entertainment_hobbies: flatData.entertainment_hobbies,
                personal_care: flatData.personal_care,
                shopping_leisure: flatData.shopping_leisure,
                travel_vacation: flatData.travel_vacation,
                misc_wants: flatData.misc_wants
            }
        },
        savings_goals: {
            target_monthly_savings: flatData.target_monthly_savings,
            emergency_fund_target: flatData.emergency_fund_target
        },
        what_if_factors: {
            income_growth_rate: flatData.income_growth_rate / 100,
            wants_reduction_rate: flatData.wants_reduction_rate / 100,
            savings_increase_rate: flatData.savings_increase_rate / 100
        }
    };
    return body;
};

async function runSimulation(endpoint, params) {
    const requestBody = buildRequestBody(params); // Prepare request payload
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
        const insight = result.data.insight;
        const keyMetrics = result.data.key_metrics;
        formulas = result.data.show_my_math;
        
        // FOR DEBUGGING
        console.log('Result: ', result);
        console.log('Chart Data: ', chartData);
        console.log('Insight: ', insight);
        console.log('Key Metrics: ', keyMetrics);
        console.log('Inputs Received: ', inputsReceived);
        console.log('Formulas: ', formulas); 

        addDatasets(chartData);

    } catch (err) {
        console.error('Fetch error:', err);
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
        showMessage("Please fill in all input fields before running the simulation.", 'empty-field-msg-box');
        console.warn("Simulation prevented: Some input fields are empty.");
        return; // Stop the function if fields are empty
    }
    runSimulation(currentScenarioEndpoint, fieldValues);
});

document.getElementById('explain-btn').addEventListener('click', async (event) => {
    await fetchAndRenderAIExplanation();
});

document.getElementById('math-btn').addEventListener('click', async (event) => {
    if (formulas.length === 0) {
        showMessage('Run simulation first to see formulas.' ,'math-msg-box');
        return;
    }
    showMessage(`Formulas Used<br><br>${formulas.join('<br><br>')}` ,'math-msg-box');
});

document.getElementById('suggest-btn').addEventListener('click', async (event) => {
    await fetchAndRenderAISuggestions();
});

document.getElementById('close-msg-btn').addEventListener('click', function() {
    messageBox.style.display = 'none';
    messageBox.className = '';
});