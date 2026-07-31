let currentFact = "Unlike humans, cats cannot detect sweetness which likely explains why they are not drawn to it at all.";

document.addEventListener("DOMContentLoaded",initializeHome);

async function initializeHome() {
    await loadRandomFact();
    document
        .getElementById("next-button")
        .addEventListener("click",loadRandomFact);
}

async function loadRandomFact() {
    const response = await apiCall("/catfacts/random/");
    if (!response.ok) {
        document.getElementById("fact-text").textContent =
            response.data.detail;
        return;
    }
    currentFact = response.data;
    document.getElementById("fact-text").textContent = currentFact.fact;
}