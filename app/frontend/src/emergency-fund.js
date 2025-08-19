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

export async function getEmergencyFundAISuggestion() {
    try {
        const response = await fetch('http://127.0.0.1:8000/emergency-fund/ai-suggestions');
        if (!response.ok) throw new Error('Failed to fetch AI suggestion');
        const result = await response.json();
        console.log('AI Suggestion:', result);
        return result;
    } catch (error) {
        console.error('Error getting AI suggestion:', error);
        throw error;
    }
}

export async function getEmergencyFundAIExplaination() {
    try {
        const response = await fetch('http://127.0.0.1:8000/emergency-fund/ai-explanation');
        if (!response.ok) throw new Error('Failed to fetch AI explanation');
        const result = await response.json();
        console.log('AI Explanation:', result);
        return result;
    } catch (error) {
        console.error('Error getting AI explanation:', error);
        throw error;
    }
}

export async function getEmergencyFundAISummary() {
    try {
        const response = await fetch('http://127.0.0.1:8000/emergency-fund/summary');
        if (!response.ok) throw new Error('Failed to fetch AI summary');
        const result = await response.json();
        console.log('AI Summary:', result);
        return result;
    } catch (error) {
        console.error('Error getting AI summary:', error);
        throw error;
    }
}
