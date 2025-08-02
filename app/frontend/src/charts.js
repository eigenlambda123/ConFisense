let chartData = {};
let beforeChart = null;
let afterChart = null;

const beforeData = {

    emergency_fund: {
        labels: ['Gap'],
        datasets: [
            {
                axis: 'y',
                label: 'Target Amount',
                data: [],
                fill: false,
                backgroundColor: [
                    'rgba(0, 255, 0, 0.2)'
                ],
                borderColor: [
                    'rgb(0, 255, 0)'
                ],
                borderWidth: 1
            },
            {
                axis: 'y',
                label: 'Current Savings',
                data: [],
                fill: false,
                backgroundColor: [
                    'rgba(255, 0, 0, 0.2)'
                ],
                borderColor: [
                    'rgb(255, 0, 0)'
                ],
                borderWidth: 1
            }
        ]

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

}

const afterData = {

    emergency_fund: {
        labels: ['Progress'],
        datasets: [
            {
                axis: 'y',
                label: 'Current Savings',
                data: [],
                fill: false,
                backgroundColor: [
                    'rgba(0, 255, 0, 0.2)'
                ],
                borderColor: [
                    'rgb(0, 255, 0)'
                ],
                borderWidth: 1
            },
            {
                axis: 'y',
                label: 'Remaining to Target',
                data: [],
                fill: false,
                backgroundColor: [
                    'rgba(255, 0, 0, 0.2)'
                ],
                borderColor: [
                    'rgb(255, 0, 0)'
                ],
                borderWidth: 1
            }
        ]

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

}

export function renderBeforeChart(scenario, values) {
    const ctx = document.getElementById('before-chart');

    console.log('Rendering before chart...')
    chartData = beforeData[scenario];

    for (let i = 0; i < values.length; i++) {
        chartData.datasets[i].data.push(values[i]);
    };

    beforeChart = new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

export function renderAfterChart(scenario) {
    const ctx = document.getElementById('after-chart');
    
    console.log('Rendering after chart...')
    chartData = afterData[scenario];

    afterChart = new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    stacked: true
                },
                y: {
                    stacked: true
                }
            }
        }
    });
}

export function destroyChart() {
    console.log('Destroying chart...')

    beforeChart.destroy();
    beforeChart = null;

    afterChart.destroy();
    afterChart = null;
}

export function updateBeforeChart(fieldIndex, value) {
    console.log('Updating before chart...')
    console.log(`Updated [${fieldIndex}]:`, value);
    beforeChart.data.datasets[fieldIndex].data[0] = value;
    beforeChart.update();
}

export function updateAfterChart(results) {
    console.log('Updating after chart...')

    for (let i = 0; i < results.length; i++) {
        afterChart.data.datasets[i].data[0] = (results[i]);
    };

    afterChart.update();
}
