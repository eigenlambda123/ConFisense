import {deleteEmergencyFundScenarioToDB} from './emergency-fund.js';

// Global Chart.js defaults applied to all charts for consistent styles and typography
Chart.defaults.set({
    font: {
        family: 'Roboto, sans-serif',
        size: 12,
    },
    plugins: {
        title: {
            color: '#060e27',
            font: {
                size: 16,
                weight: 'bold',
            },
            padding: {
                top: 10,
                bottom: 30
            },
        }
    },
    scales: {
        // Default settings for ALL x-axes
        x: {
            title: {
                display: true,
                color: '#3b3b3b',
                font: {
                    size: 14,
                    weight: 'bold'
                }
            },
            ticks: {
                color: '#3b3b3b' // Default color for x-axis tick labels
            },
            grid: {
                color: 'gray', // Default color for x-axis grid lines
                lineWidth: 1, // Default width for x-axis grid lines
                // You can also set tickColor here if you want it different from grid.color
                // tickColor: 'green'
            },
            border: {
                color: 'gray', // Default color for the x-axis line itself
                width: 1, // Default width for the x-axis line
            }
        },
        // Default settings for ALL y-axes
        y: {
            title: {
                display: true,
                color: '#3b3b3b',
                font: {
                    size: 14,
                    weight: 'bold'
                }
            },
            ticks: {
                color: '#3b3b3b' // Default color for y-axis tick labels
            },
            grid: {
                color: 'gray', // Default color for y-axis grid lines
                lineWidth: 1, // Default width for y-axis grid lines
                // You can also set tickColor here if you want it different from grid.color
                // tickColor: 'orange'
            },
            border: {
                color: 'gray', // Default color for the y-axis line itself
                width: 1, // Default width for the y-axis line
            }
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
    budget_optimization: 'bar',
};

// Initial dataset structure for each scenario
const chartDataConfig = {
    budget_optimization: {
        labels: [],
        datasets: [],
    },
}

// Consiguration for chart behavior and visuals per scenario
const chartSettingsConfig = {

    budget_optimization: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
            },
            title: {
                display: true,
                text: 'Income vs. Expense Categories'
            },
        },
        scales: {
            x: {
                ...Chart.defaults.scales.x,
                stacked: true,
                title: {
                    ...Chart.defaults.scales.x.title,
                    text: 'Time (Months)'
                }
            },
            y: {
                ...Chart.defaults.scales.y,
                stacked: true,
                title: {
                    ...Chart.defaults.scales.y.title,
                    text: 'Amount (PHP)'
                }
            }
        }
    },
    
    budgeting: {
        responsive: true,
        maintainAspectRatio: false,
    },

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

export function addDatasets(data) {
    if (!chart) {
        console.error('Chart not initialized.')
        return;
    }

    const chartLabels = data.map(item => item.month);
    const fixedExpensesData = data.map(item => item.fixed_expenses);
    const variableExpensesData = data.map(item => item.variable_expenses);
    const wantsExpensesData = data.map(item => item.wants_expenses);
    const netCashFlowData = data.map(item => item.net_cash_flow);

    // New dataset for scenario run
    const datasets = [
        {
            label: 'Fixed Expenses',
            data: fixedExpensesData,
            backgroundColor: '#4c72b0'
        },
        {
            label: 'Variable Expenses',
            data: variableExpensesData,
            backgroundColor: '#55a868'
        },
        {
            label: 'Wants Expenses',
            data: wantsExpensesData,
            backgroundColor: '#c44e52'
        },
        {
            label: 'Net Cash Flow',
            data: netCashFlowData,
            backgroundColor: '#8172b3'
        }
    ];

    chart.data.labels = chartLabels;
    chart.data.datasets = datasets;
    console.log("Labels: ", chart.data.labels);
    console.log("Datasets: ", chart.data.datasets);

    chart.update();
}

export function updateChartTitle(summary) {
    // Update chart title dynamically with scenario summary
    if (chart) {
        chart.options.plugins.title.text = summary;
        chart.update();
        console.log('Chart title updated.')
    }
}

export function clearChartTitle() {
    if (chart) {
        // Clear chart title when exiting dashboard
        chart.options.plugins.title.text = '';
        chart.update();
        console.log('Chart title cleared.')
    }
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