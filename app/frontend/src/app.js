import { renderBeforeChart, destroyChart, updateBeforeChart, renderAfterChart, updateAfterChart } from "./charts.js";

let currentScenario = '';
let currentScenarioConfig = {};
let currentScenarioEndpoint = '';
let inputValues = {}; // All input values from all fields

const field = (id, label, min, step, def, type) => ({ id, label, min, step, default: def, type });

const scenariosConfig = {
    emergency_fund: {
        label: "Building an Emergency Fund",
        endpoint: "/simulate/emergency-fund",
        fields: [
            field("target", "Target Emergency Fund Amount (₱)", 0, 1000, 100000, 'baseline'),
            field("current_savings", "Current Emergency Savings (₱)", 0, 1000, 20000, 'baseline'),
            field("monthly_contrib", "Monthly Savings Contribution (₱)", 0, 500, 5000, 'actionable'),
        ],
    },
    budgeting: {
        label: "Effective Budgeting and Expense Tracking",
        endpoint: "/simulate/budgeting",
        fields: [
            field("income", "Monthly Income (₱)", 0, 1000, 40000, 'baseline'),
            field("fixed_expenses", "Fixed Monthly Expenses (₱)", 0, 500, 15000, 'baseline'),
            field("target_savings", "Target Monthly Savings (₱)", 0, 1000, 5000, 'baseline'), // This is often a goal, so could be actionable too, but per your plan it's baseline.
            field("discretionary_pct", "Discretionary Spending (% of Income)", 0, 1, 20, 'actionable'),
        ],
    },
    debt_management: {
        label: "Managing and Reducing Debt",
        endpoint: "/simulate/debt-management",
        fields: [
            field("debt", "Total Debt Amount (₱)", 0, 10000, 200000, 'baseline'),
            field("interest_rate", "Annual Interest Rate (%)", 0, 0.5, 10, 'baseline'),
            field("monthly_payment", "Current Monthly Debt Payment (₱)", 0, 1000, 5000, 'baseline'),
            field("extra_payment", "Additional Monthly Payment (₱)", 0, 500, 2000, 'actionable'),
        ],
    },
    investing: {
        label: "Starting to Save and Invest for the Future",
        endpoint: "/simulate/investing",
        fields: [
            field("initial", "Current Investment/Savings Amount (₱)", 0, 10000, 100000, 'baseline'),
            field("years", "Investment Horizon (Years)", 0, 1, 10, 'baseline'),
            field("monthly", "Monthly Contribution (₱)", 0, 500, 5000, 'actionable'),
            field("return_rate", "Expected Annual Return (%)", 0, 0.1, 6, 'actionable'),
        ],
    },
    education_funding: {
        label: "Education Funding",
        endpoint: "/simulate/education-fund",
        fields: [
            field("today_cost", "Target Education Cost (Today) (₱)", 0, 50000, 1000000, 'baseline'),
            field("years", "Years Until Enrollment", 0, 1, 5, 'baseline'),
            field("current_savings", "Current Education Savings (₱)", 0, 10000, 100000, 'baseline'),
            field("inflation_rate", "Annual Education Inflation Rate (%)", 0, 0.1, 4, 'baseline'),
            field("monthly_contrib", "Monthly Savings Contribution (₱)", 0, 500, 3000, 'actionable'),
            field("return_rate", "Expected Annual Investment Return (%)", 0, 0.1, 5, 'actionable'),
        ],
    },
    major_purchase: {
        label: "Major Purchase Planning",
        endpoint: "/simulate/major-purchase",
        fields: [
            field("price", "Target Purchase Price (₱)", 0, 100000, 3000000, 'baseline'),
            field("down_pct", "Desired Down Payment (%)", 0, 1, 20, 'baseline'),
            field("years_to_save", "Years to Save for Down Payment", 0, 1, 3, 'baseline'),
            field("current_savings", "Current Savings (₱)", 0, 10000, 200000, 'baseline'),
            field("loan_rate", "Loan Interest Rate (Annual %)", 0, 0.1, 8, 'baseline'),
            field("monthly_contrib", "Monthly Savings Contribution (₱)", 0, 1000, 10000, 'actionable'),
            field("savings_return", "Expected Annual Savings Return (%)", 0, 0.1, 3, 'actionable'),
            field("loan_term", "Loan Term (Years)", 0, 1, 15, 'actionable'),
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

    const paramGroupDiv = document.createElement('div');
    paramGroupDiv.className = 'flex flex-col justify-equal gap-2 my-2';

    const currentSituationDiv = document.createElement('div');
    currentSituationDiv.innerHTML = '<h2 class="widget-title">Your Current Situation</h3>';
    
    const actionsGoalsDiv = document.createElement('div');
    actionsGoalsDiv.innerHTML = '<h2 class="widget-title">Your Actions and Goals</h3>';

    fieldContainer.appendChild(paramGroupDiv);
    paramGroupDiv.appendChild(currentSituationDiv);
    paramGroupDiv.appendChild(actionsGoalsDiv);

    let fieldCounter = 0 // Counter for baseline fields
    let fieldInputs = {}; // All baseline field input elements

    currentScenarioConfig.fields.forEach(field => {
        const wrapper = document.createElement('div');
        wrapper.className = 'my-4';

        const label = document.createElement('label');
        label.textContent = field.label;
        label.htmlFor = field.id;
        label.className = 'block font-medium text-[0.75rem] min-[550px]:text-[0.8rem] mb-1';

        const input = document.createElement('input');
        input.type = 'number';
        input.min = field.min;
        input.step = field.step;
        input.value = field.default;
        input.id = field.id;
        input.dataset.type = field.type;
        input.className = 'w-full px-2 py-1 border bg-[#060e27] rounded text-[0.75rem] min-[550px]:text-[0.8rem]';

        wrapper.appendChild(label);
        wrapper.appendChild(input);
      
        // Dynamically append to the correct section based on 'type'
        if (field.type === 'baseline') {
            currentSituationDiv.appendChild(wrapper);
        } else if (field.type === 'actionable') {
            actionsGoalsDiv.appendChild(wrapper);
        } else {
            console.warn(`Field ${field.id} has no defined type (baseline/actionable). Appending to main container.`);
            fieldContainer.appendChild(wrapper);
        }
        
        fieldInputs[fieldCounter] = input;
        if (input.dataset.type === 'baseline') fieldCounter += 1;

        inputValues[input.id] = Number(input.value); // get default values for api

    });
    
    // Automatically renders before graph with default values
    let beforeValues = Object.values(fieldInputs)
        .filter(input => input.dataset.type === 'baseline')
        .map(input => Number(input.value));
    renderBeforeChart(currentScenario, beforeValues);

    // Render after chart with no data
    renderAfterChart(currentScenario);
        
    // Watches changes in the baseline inputs and updates graph accordingly
    for (const [index, input] of Object.entries(fieldInputs)) {
        if (input.dataset.type === 'baseline') {
            input.addEventListener('input', function() {
                updateBeforeChart(index, Number(input.value));
                inputValues[input.id] = Number(input.value); // For API call and formula calculation
            });
        } else {
            input.addEventListener('input', function() {
                inputValues[input.id] = Number(input.value); // For API call and formula calculation
            });
        }
    }

    document.getElementById('home').classList.add('hidden');
    document.getElementById('dashboard').classList.remove('hidden');
}

function showHome() {
    document.getElementById('home').classList.remove('hidden');
    document.getElementById('dashboard').classList.add('hidden');
    destroyChart();
}

async function runSimulation(endpoint, params) {
    const requestBody = params;

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

        console.log('Input:', params);
        console.log('Result:', result.values);

        updateAfterChart(result.values)
    } catch (err) {
        console.error('Fetch error:', err);
    }
}

document.querySelectorAll('.card-btn').forEach(button => {
    button.addEventListener('click', function() {
        showDashboard(this);
    });
});


document.getElementById('back-btn').addEventListener('click', function() {
    showHome();
});

document.getElementById('simulation-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    runSimulation(currentScenarioEndpoint, inputValues);
});