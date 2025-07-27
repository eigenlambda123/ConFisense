let currentScenario = null;
let currentScenarioConfig = null;

const field = (id, label, min, max, step, def) => ({ id, label, min, max, step, default: def });

const scenariosConfig = {

  emergency_fund: {
    label: "Building an Emergency Fund",
    endpoint: "/simulate/esmergency-fund",
    fields: [
      field("target_amount", "Target Emergency Fund Amount (₱)", 5000, 500000, 1000, 100000),
      field("monthly_contribution", "Monthly Savings Contribution (₱)", 500, 20000, 500, 5000),
      field("current_savings", "Current Emergency Savings (₱)", 0, 100000, 1000, 20000),
    ],
  },

  budgeting: {
    label: "Effective Budgeting and Expense Tracking",
    endpoint: "/simulate/budgeting",
    fields: [
      field("income", "Monthly Income (₱)", 10000, 100000, 1000, 40000),
      field("fixed_expenses", "Fixed Monthly Expenses (₱)", 0, 50000, 500, 15000),
      field("discretionary_pct", "Discretionary Spending (% of Income)", 10, 50, 1, 20),
      field("target_savings", "Target Monthly Savings (₱)", 0, 30000, 1000, 5000),
    ],
  },

  debt_management: {
    label: "Managing and Reducing Debt",
    endpoint: "/simulate/debt-management",
    fields: [
      field("total_debt", "Total Debt Amount (₱)", 20000, 1000000, 10000, 200000),
      field("interest_rate", "Annual Interest Rate (%)", 5, 30, 0.5, 10),
      field("monthly_payment", "Current Monthly Debt Payment (₱)", 1000, 50000, 1000, 5000),
      field("additional_payment", "Additional Monthly Payment (₱)", 0, 20000, 500, 2000),
    ],
  },

  investing: {
    label: "Starting to Save and Invest for the Future",
    endpoint: "/simulate/investing",
    fields: [
      field("monthly_contribution", "Monthly Contribution (₱)", 500, 30000, 500, 5000),
      field("investment_years", "Investment Horizon (Years)", 1, 40, 1, 10),
      field("annual_return", "Expected Annual Return (%)", 1, 15, 0.1, 6),
      field("current_savings", "Current Investment/Savings Amount (₱)", 0, 500000, 10000, 100000),
    ],
  },

  education_funding: {
    label: "Education Funding",
    endpoint: "/simulate/education-fund",
    fields: [
      field("target_cost_today", "Target Education Cost (Today) (₱)", 100000, 3000000, 50000, 1000000),
      field("years_until_enrollment", "Years Until Enrollment", 1, 18, 1, 5),
      field("current_savings", "Current Education Savings (₱)", 0, 500000, 10000, 100000),
      field("monthly_contribution", "Monthly Savings Contribution (₱)", 500, 20000, 500, 3000),
      field("annual_return", "Expected Annual Investment Return (%)", 1, 10, 0.1, 5),
      field("inflation_rate", "Annual Education Inflation Rate (%)", 3, 7, 0.1, 4),
    ],
  },

  major_purchase: {
    label: "Major Purchase Planning",
    endpoint: "/simulate/major-purchase",
    fields: [
      field("purchase_price", "Target Purchase Price (₱)", 500000, 10000000, 100000, 3000000),
      field("down_payment_pct", "Desired Down Payment (%)", 10, 30, 1, 20),
      field("years_to_save", "Years to Save for Down Payment", 1, 10, 1, 3),
      field("current_savings", "Current Savings (₱)", 0, 1000000, 10000, 200000),
      field("monthly_contribution", "Monthly Savings Contribution (₱)", 1000, 50000, 1000, 10000),
      field("savings_return", "Expected Annual Savings Return (%)", 1, 5, 0.1, 3),
      field("loan_interest", "Loan Interest Rate (Annual %)", 5, 15, 0.1, 8),
      field("loan_term_years", "Loan Term (Years)", 5, 30, 1, 15),
    ],
  },
};

function showDashboard(buttonElement) {
    const scenarioKey = buttonElement.dataset.scenario;
    currentScenario = scenarioKey;
    const config = scenariosConfig[scenarioKey];

    currentScenarioConfig = config;

    if (!currentScenarioConfig) {
      console.error("Scenario configuration not found for:", scenarioKey);
      return;
    }

    const scenarioTitleElement = document.getElementById('scenario-title');
    scenarioTitleElement.textContent = currentScenarioConfig.label;

    const fieldContainer = document.getElementById('form-fields');
    fieldContainer.innerHTML = ''; // Clear existing sliders

    // Add "Your Current Situation" and "Your Actions and Goals" sections dynamically
    // This assumes a logical split of fields, you might need to adjust based on your actual fields
    const currentSituationFields = [
        "current_savings", "income", "fixed_expenses", "total_debt", "current_investment", "target_cost_today", "current_savings", "purchase_price"
    ];
    const actionsGoalsFields = [
        "target_amount", "monthly_contribution", "discretionary_pct", "target_savings", "interest_rate",
        "monthly_payment", "additional_payment", "monthly_contribution", "investment_years",
        "annual_return", "years_until_enrollment", "annual_return", "inflation_rate",
        "down_payment_pct", "years_to_save", "savings_return", "loan_interest", "loan_term_years"
    ];

    const paramGroupDiv = document.createElement('div');
    paramGroupDiv.className = 'flex flex-col justify-equal gap-2 my-2';

    const currentSituationDiv = document.createElement('div');
    currentSituationDiv.innerHTML = '<h2 class="widget-title">Your Current Situation</h3>';
    const actionsGoalsDiv = document.createElement('div');
    actionsGoalsDiv.innerHTML = '<h2 class="widget-title">Your Actions and Goals</h3>';

    paramGroupDiv.appendChild(currentSituationDiv);
    paramGroupDiv.appendChild(actionsGoalsDiv);

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
      input.max = field.max;
      input.step = field.step;
      input.value = field.default;
      input.id = field.id;
      input.className = 'w-full px-2 py-1 border bg-[#060e27] rounded text-[0.75rem] min-[550px]:text-[0.8rem]';

      wrapper.appendChild(label);
      wrapper.appendChild(input);
      
      if (currentSituationFields.includes(field.id)) {
            currentSituationDiv.appendChild(wrapper);
      } else if (actionsGoalsFields.includes(field.id)) {
          actionsGoalsDiv.appendChild(wrapper);
      } else {
          // Fallback for fields not explicitly categorized
          fieldContainer.appendChild(wrapper);
      }
    });

    fieldContainer.appendChild(paramGroupDiv);

    document.getElementById('home').classList.add('hidden');
    document.getElementById('dashboard').classList.remove('hidden');
}

function showHome() {
    currentScenario = null;
    currentScenarioConfig = null;
    document.getElementById('home').classList.remove('hidden');
    document.getElementById('dashboard').classList.add('hidden');
}