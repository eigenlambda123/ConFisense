import {deleteEmergencyFundScenarioToDB} from './emergency-fund.js';

// Global Chart.js defaults applied to all charts for consistent styles and typography
Chart.defaults.set({
    font: {
        family: 'Roboto, sans-serif',
        size: 12,
    },
    plugins: {
        title: {
            color: 'white',
            font: {
                size: 16,
                weight: 'bold',
            },
            padding: {
                top: 10,
                bottom: 30
            },
        }
    }
});

// State variables for the active chart instance
let chartType = '';
let chartData = {};
let chartSettings = {};
let chart = null;

// Different scenarios may use different visualizations
const chartTypeConfig = {
    emergency_fund: 'line',
    budgeting: 'bar',
    debt_management: '',
    investing: '',
    education_funding: '',
    major_purchase: ''
};

// Initial dataset structure for each scenario
const chartDataConfig = {

    emergency_fund: {
        labels: [],
        datasets: [
            {
                // Placeholder until API provides real data
                data: [],
            },
        ],
    },
    budgeting: {
        labels: [],
        datasets: [
            {
                // Placeholder until API provides real data
                data: [],
            },
        ],
    },
    debt_management: {
        labels: [],
        datasets: [
            {
                // Placeholder until API provides real data
                data: [],
            },
        ],
    },
    investing: {
        labels: [],
        datasets: [],
    },
    education_funding: {
        labels: [],
        datasets: [],
    },
    major_purchase: {
        labels: [],
        datasets: [],
    }

}

// Consiguration for chart behavior and visuals per scenario
const chartSettingsConfig = {

    emergency_fund: {
        responsive: true,
        maintainAspectRatio: false,
        elements: {
            point: {
                radius: 0, 
                hitRadius: 10,
            }
        },
        plugins: {
            legend: {
                display: false,
            },
            title: {
                display: true,
            },
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Time (Months)'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Total Savings ($)'
                }
            }
        }
    },
    
    budgeting: {
        responsive: true,
        maintainAspectRatio: false,
    },

    debt_management: {
        responsive: true,
        maintainAspectRatio: false,
    },

    investing: {
        responsive: true,
        maintainAspectRatio: false,
    },

    education_funding: {
        responsive: true,
        maintainAspectRatio: false,
    },

    major_purchase: {
        responsive: true,
        maintainAspectRatio: false,
    }

};

export function renderChart(scenario) {
    console.log(scenario);
    const ctx = document.getElementById('chart-canvas');

    if (chart) {
        destroyChart(); // Destroy existing chart if switching scenarios
    }

    if (!ctx) {
        console.error("Canvas element with ID 'chart-canvas' not found.");
        return;
    }

    console.log('Rendering chart...')

    // Load correct config for chosen scenario
    chartType = chartTypeConfig[scenario];
    chartData = chartDataConfig[scenario];
    chartSettings = chartSettingsConfig[scenario];

    // Check if chartType is valid
    if (!chartType) {
        console.error(`Error: Chart type for scenario '${scenario}' is undefined or empty. Please define it in chartTypeConfig.`);
        chartType = 'line'; // Fallback to 'line' to prevent "not a registered controller" error
    }

    // Create new Chart.js instance bound to canvas
    chart = new Chart(ctx, {
        type: chartType,
        data: chartData,
        options: chartSettings,
    });
}

let datasetCounter = 1;
const activeScenariosContainer = document.getElementById('active-graphs');

export function createDataset(title, color, data, labels, summary, scenarioId) {
    if (!chart) {
        console.error('Chart not initialized.')
        return;
    }

    // New dataset for scenario run
    const newDataset = {
        label: title,
        data: data,
        fill: false,
        borderColor: color, // Scenario color picked by user
        tension: 0.1, // Curve smoothing for readability
        scenarioId: scenarioId // ID identifier for the scenario
    };
    
    // Update chart title dynamically with scenario summary
    const chartTitle = chart.options.plugins.title;
    chartTitle.text = summary;

    // Push dataset into chart's data collection
    chart.data.datasets.push(newDataset);
    console.log("Datasets: ", chart.data.datasets);
    const datasetIndex = datasetCounter;
    datasetCounter++;

    // Build UI tab for dataset so user can identfy/remove it
    const tabTemplate = document.getElementById('graph-tab-template');
    if (!tabTemplate) {
        console.error('Scenario tab template not found.');
        return;
    }
    
    // Clone entire structure from template
    const tabClone = tabTemplate.content.cloneNode(true);
    const tabWrapper = tabClone.querySelector('div');
    const label = tabClone.querySelector('label');
    const deleteBtn = tabClone.querySelector('button');

    // Populate cloned elements with dynamic data
    label.textContent = newDataset.label;
    tabWrapper.style.border = `2px solid ${color}`;

    // Delete button removes dataset from chart and UI
    deleteBtn.onclick = () => {
        chart.data.datasets.splice(datasetIndex, 1);
        datasetCounter--;
        console.log(`Removing dataset '${newDataset.label}'.`);
        tabWrapper.remove();
        console.log(chart.data.datasets);
        updateChart(chart.data.labels);

        // Delete emergency fund scenario from database
        console.log("Deleting dataset with ID:", newDataset.scenarioId);
        deleteEmergencyFundScenarioToDB(newDataset.scenarioId);
    };

    activeScenariosContainer.appendChild(tabClone); // Append to "active scenarios" container
    updateChart(labels); // Trigger chart update with latest labels
}

export function updateChart(labels) {
    if (!chart) {
        console.error('Chart not initialized.');
    }
    chart.data.labels = labels; // Refresh labels (x-axis)
    chart.update(); // Redraw chart with new data
}

export function destroyChart() {
    console.log('Destroying chart...');
    if (chart) {
        chart.destroy(); // Properly dispose Chart.js instance
        console.log('Chart instance destroyed.');
        chart = null; // Explicitly set to null immediately after destruction
    } 
    else {
        console.log('No chart to destroy.');
    }

    // Always clear the global chartData's datasets and labels
    chartData.datasets = [];
    chartData.labels = [];

    // Clear the content of the active scenarios container to prevent old tabs from lingering
    const activeScenariosContainer = document.getElementById('active-graphs');
    if (activeScenariosContainer) {
        activeScenariosContainer.innerHTML = '';
        console.log('Active scenarios tabs cleared.');
    }
    
    // Reset datasetCounter for a fresh start when new datasets are added
    datasetCounter = 1;
}