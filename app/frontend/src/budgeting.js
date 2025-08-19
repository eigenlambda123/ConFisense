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
