// Function that will delete the emergency fund scenario from the database
export async function deleteEmergencyFundScenarioToDB(scenarioId) {
    console.log("deleteEmergencyFundScenarioToDB called with:", scenarioId);
    try {
        const response = await fetch(`http://127.0.0.1:8000/emergency-fund/${scenarioId}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('Failed to delete scenario');
        const result = await response.json();
        console.log('Scenario deleted:', result);
    } catch (err) {
        console.error('Delete error:', err);
    }
}

export async function saveEmergencyFundScenarioToDB(params) {
    try {
        const response = await fetch('http://127.0.0.1:8000/emergency-fund/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(params)
        });

        // Check if the response is okay
        if (!response.ok) throw new Error('Failed to save scenario');

        // Log the result if successful
        const result = await response.json();
        console.log('Scenario saved:', result);

        return result;
    } catch (err) {
        console.error('Fetch error:', err);
    }
}