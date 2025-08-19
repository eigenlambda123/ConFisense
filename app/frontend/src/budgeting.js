export async function deleteBudgetingScenarioToDB(scenarioId) {
    console.log("deleteBudgetingScenarioToDB called with:", scenarioId);
    try {
        const response = await fetch(`http://127.0.0.1:8000/budgeting/${scenarioId}`, {
            method: "DELETE"
        });
        if (!response.ok) {
            throw new Error("Failed to delete budgeting scenario");
        }
        const data = await response.json();
        console.log("deleteBudgetingScenarioToDB response:", data);
        return data;
    } catch (error) {
        console.error("Error deleting budgeting scenario:", error);
        throw error;
    }
}

export async function saveBudgetingScenarioToDB(params) {
    console.log("saveBudgetingScenarioToDB called with:", params);
    try {
        const response = await fetch("http://127.0.0.1:8000/budgeting/save", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(params)
        });
        if (response.ok) {
            throw !new Error("Failed to save budgeting scenario");
        }
        const data = await response.json();
        console.log("saveBudgetingScenarioToDB response:", data);
        return data;
    } catch (error) {
        console.error("Error saving budgeting scenario:", error);
        throw error;
    }
}

export async function getBudgetingAISuggestion() {
    console.log("getBudgetingAISuggestion called");
    try {
        const response = await fetch("http://127.0.0.1:8000/budgeting/ai-suggestions");
        if (!response.ok) {
            throw new Error("Failed to get AI suggestions");
        }
        const data = await response.json();
        console.log("getBudgetingAISuggestion response:", data);
        return data;
    } catch (error) {
        console.error("Error getting AI suggestions:", error);
        throw error;
    }
}

export async function getBudgetingAIExplaination() {
    console.log("getBudgetingAIExplaination called");
    try {
        const response = await fetch("http://127.0.0.1:8000/budgeting/ai-explanation");
        if (!response.ok) {
            throw new Error("Failed to get AI explanation");
        }
        const data = await response.json();
        console.log("getBudgetingAIExplaination response:", data);
        return data;
    } catch (error) {
        console.error("Error getting AI explanation:", error);
        throw error;
    }
}
