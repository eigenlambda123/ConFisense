let chartType = '';
let chartData = {};
let chartSettings = {};
let chart = null;

const chartTypeConfig = {
    emergency_fund: 'line',
    budgeting: '',
    debt_management: '',
    investing: '',
    education_funding: '',
    major_purchase: ''
};

const chartDataConfig = {

    emergency_fund: {
        labels: [],
        datasets: [
            {
                // Placeholder
                data: [],
            },
        ],
    },
    budgeting: {
        labels: [],
        datasets: [],
    },
    debt_management: {
        labels: [],
        datasets: [],
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
                    display: false
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

    },

    debt_management: {

    },

    investing: {

    },

    education_funding: {

    },

    major_purchase: {

    }

};

export function renderChart(scenario) {
    const ctx = document.getElementById('chart-canvas');

    if (chart) {
        destroyChart();
    }

    console.log('Rendering chart...')

    chartType = chartTypeConfig[scenario];
    chartData = chartDataConfig[scenario];
    chartSettings = chartSettingsConfig[scenario];

    chart = new Chart(ctx, {
        type: chartType,
        data: chartData,
        options: chartSettings,
    });
}

let datasetCounter = 1;
const activeScenariosContainer = document.getElementById('active-scenarios');

export function createDataset(title, color, data, labels) {
    if (!chart) {
        console.error('Chart not initialized.')
        return;
    }

    const newDataset = {
        label: title,
        data: data,
        fill: false,
        borderColor: color,
        tension: 0.1
    };

    chart.data.datasets.push(newDataset);
    console.log("Datasets: ", chart.data.datasets);
    const datasetIndex = datasetCounter;
    datasetCounter++;

    const tabTemplate = document.getElementById('scenario-tab-template');
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

    // Event listener for cloned button
    deleteBtn.onclick = () => {
        chart.data.datasets.splice(datasetIndex, 1);
        console.log(`Removing dataset '${newDataset.label}'.`);
        tabWrapper.remove();
        updateChart(chart.data.labels);
    };

    activeScenariosContainer.appendChild(tabClone);
    updateChart(labels);
}

export function updateChart(labels) {
    if (!chart) {
        console.error('Chart not initialized.')
    }
    chart.data.labels = labels;
    chart.update();
}

export function destroyChart() {
    console.log('Destroying chart...')
    if (chart) {
        chart.destroy();
        chart = null;
    }
}