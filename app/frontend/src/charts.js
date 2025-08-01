let chartData = {};
let beforeChart = null;

const data = {

    emergency_fund: {
        labels: ['Target Amount', 'Current Savings'],
        datasets: [{
            axis: 'y',
            label: 'Emergency Fund',
            data: [],
            fill: false,
            backgroundColor: [
                'rgba(0, 255, 0, 0.2)',
                'rgba(255, 0, 0, 0.2)'
            ],
            borderColor: [
                'rgb(0, 255, 0)',
                'rgb(255, 0, 0)'
            ],
            borderWidth: 1
        }]

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

const ctx = document.getElementById('before-chart');

export function renderBeforeChart(scenario, values) {
    console.log('Rendering chart...')
    chartData = data[scenario];
    chartData.datasets[0].data = values;

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

export function destroyChart() {
    console.log('Destroying chart...')
    beforeChart.destroy();
    beforeChart = null;
}

export function updateChart(fieldIndex, value) {
    console.log('Updating chart...')
    console.log(`Updated [${fieldIndex}]:`, value);
    beforeChart.data.datasets[0].data[fieldIndex] = value;
    beforeChart.update();
}
