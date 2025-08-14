import { renderChart, destroyChart, createDataset } from "./charts.js";

let currentScenario = '';
let currentScenarioConfig = {};
let currentScenarioEndpoint = '';
let fields = []; // All fields
let fieldValues = {}; // All field inputs

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
            field("years", "Years Until Enrollment", 0, 1, 5, 'baseline'),
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

function showDashboard(buttonElement) {
    const scenarioKey = buttonElement.dataset.scenario;
    currentScenario = scenarioKey;
    const config = scenariosConfig[scenarioKey];
    currentScenarioConfig = config;
    currentScenarioEndpoint = config.endpoint;

    if (!currentScenarioConfig) return;

    const scenarioTitleElement = document.getElementById('scenario-title');
    scenarioTitleElement.textContent = currentScenarioConfig.label;

    const fieldContainer = document.getElementById('form-fields');
    fieldContainer.innerHTML = '';

    fields = [];
    fieldValues = {};

    const fieldTemplate = document.getElementById('field-template');
    if (!fieldTemplate) {
        console.error('Field template not found.');
        return;
    }

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

        // Event listener to new input for API call and formula calculation
        input.addEventListener('input', function() {
            fieldValues[input.id] = input.type === 'number' ? Number(input.value) : input.value;
        });
      
        // Add to list of fields and values
        fields.push(input);
        fieldValues[input.id] = input.type === 'number' ? Number(input.value) : input.value;

        // Append new field to container
        fieldContainer.appendChild(fieldClone);
    });

    document.getElementById('home').classList.add('hidden');
    document.getElementById('dashboard').classList.remove('hidden');
    renderChart(currentScenario);
}

function showHome() {
    document.getElementById('home').classList.remove('hidden');
    document.getElementById('dashboard').classList.add('hidden');
    destroyChart();
}

async function runSimulation(endpoint, params) {    
    const requestBody = params;
    const scenarioTitle = requestBody.scenario_title;
    const scenarioColor = requestBody.scenario_color;

    try {
        console.log('Running simulation...');
        const response = await fetch(`http://127.0.0.1:8000${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) throw new Error('Request failed');

        const result = await response.json();
        const data = result.data.projection_data.balance_history;
        const labels = result.data.projection_data.months_labels;
        const AIExplanation = result.ai_explanation;
        const AISuggestion = result.ai_suggestions;

        console.log('Title:', scenarioTitle);
        console.log('Color:', scenarioColor);
        console.log('Input:', params);
        console.log('Labels:', labels);
        console.log('Result:', data);
        console.log('Explanation:', AIExplanation)
        console.log('Suggestions:', AISuggestion);

        createDataset(scenarioTitle, scenarioColor, data, labels);
        renderAIResponses(AIExplanation, AISuggestion);

    } catch (err) {
        console.error('Fetch error:', err);
    }
}

function renderAIResponses(ai_explanation, ai_suggestions) {
    const ex_wrapper = document.getElementById('ai-explanation');
    const su_wrapper = document.getElementById('ai-suggest');

    const aiResponseTemplate = document.getElementById('ai-response-template');
    if (!aiResponseTemplate) {
        console.error('AI response template not found.');
        return;
    }

    // Clear previous AI responses
    ex_wrapper.innerHTML = '';
    su_wrapper.innerHTML = '';

    // AI Explanation
    const explanationNode = aiResponseTemplate.content.cloneNode(true);
    explanationNode.querySelector('p').textContent = ai_explanation;
    ex_wrapper.appendChild(explanationNode);

    // AI Suggestions
    const suggestions = ai_suggestions.join('\n\n');
    const suggestionNode = aiResponseTemplate.content.cloneNode(true);
    suggestionNode.querySelector('p').textContent = suggestions;
    su_wrapper.appendChild(suggestionNode);
}

document.querySelectorAll('.card-btn').forEach(button => {
    button.addEventListener('click', function() {
        showDashboard(this);
    });
});

document.getElementById('back-btn').addEventListener('click', function() {
    showHome();
});

document.getElementById('clear-fields-btn').addEventListener('click', function() {
    fields.forEach((input) => {
        input.value = null;
    });
})

document.getElementById('simulation-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    runSimulation(currentScenarioEndpoint, fieldValues);
});