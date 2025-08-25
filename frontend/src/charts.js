// Global Chart.js defaults applied to all charts
Chart.defaults.set({
    font: {
        family: 'Roboto, sans-serif',
        size: 12
    },
    plugins: {
        legend: {
            display: true,
            position: 'top',
            align: 'center',
        },
        title: {
            color: '#060e27',
            font: {
                size: 16,
                weight: 'bold'
            },
            padding: {
                top: 10,
                bottom: 30
            },
        }
    },
    scales: {
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
                color: '#3b3b3b'
            },
            grid: {
                color: 'gray',
                lineWidth: 1
            },
            border: {
                color: 'gray',
                width: 1
            }
        },
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
                color: '#3b3b3b'
            },
            grid: {
                color: 'gray',
                lineWidth: 1
            },
            border: {
                color: 'gray',
                width: 1
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
    debt_management: '',
    wealth_building: ''
};

// Initial dataset structure for each scenario
const chartDataConfig = {
    budget_optimization: {
        labels: [],
        datasets: [
            {}
        ]
    },
    debt_management: {},
    wealth_building: {}
}

// Consiguration for chart behavior and visuals per scenario
const chartSettingsConfig = {

    budget_optimization: {
        responsive: true,
        maintainAspectRatio: false,
        ...Chart.defaults.plugins,
        plugins: {
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
    debt_management: {},
    wealth_building: {}

};

// Renders new Chart.js instance on canvas based on selected scenario
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

// Adds new chart data to active chart after simulation is run
export function addChartData(data) {
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
    console.log("Datasets successfully added.");
}

export function updateChart(labels) {
    if (!chart) {
        console.error('Chart not initialized.');
    }
    chart.data.labels = labels; // Refresh labels (x-axis)
    chart.update(); // Redraw chart with new data
}

export function destroyChart() {
    if (!chart) {
        console.log('No chart to destroy.');
        return;
    }

    chart.destroy(); // Properly dispose Chart.js instance

     // Clear global chartData's datasets and labels
    chart.data.datasets = [];
    chart.data.labels = [];

    console.log('Chart instance destroyed.');
    chart = null; // Explicitly set to null immediately after destruction
}

// Retrieves explanation text after API fetch
let explanation;
export function getExplanation(explanationText) {
    explanation = explanationText;
}

// Retrieves suggestions array after API fetch
let suggestions;
export function getSuggestions(suggestionsArray) {
    suggestions = suggestionsArray;
}

// Generates and downloads PDF report containing chart and AI-generated insights
export function exportChart() {
    if (!chart) {
        throw new Error("Chart is not available");
    }
    if (!explanation) {
        throw new Error("Explanation is not available");
    }
    if (!suggestions || suggestions.length === 0) {
        throw new Error("Suggestions are not available or are empty");
    }

    const chartImage = chart.toBase64Image(); // Convert chart instance into base64 image

    // Define structure and content of PDF
    const docDefinition = {
        content: [
            // Title of report
            { text: 'Simulation Report', style: 'header' },

            // Embed chart image
            { image: chartImage, width: 500 },

            // Subheading for the explanation section
            { text: 'AI-Powered Explanation:', style: 'subheader' },

            // Explanation text with bottom margin
            { text: explanation, margin: [0, 0, 0, 10] },

            // Subheading for suggestions section
            { text: 'AI-Powered Suggestions:', style: 'subheader' },

            // Renders suggestions array as bullet list automatically
            { ul: suggestions }
        ],
        // Define reusable styles for headings and subheadin
        styles: {
            header: { fontSize: 18, bold: true, alignment: 'center', margin: [0, 0, 0, 20] },
            subheader: { fontSize: 14, bold: true, margin: [0, 10, 0, 5] }
        }
    };

    // Create and trigger download of the PDF
    pdfMake.createPdf(docDefinition).download("report.pdf");
}