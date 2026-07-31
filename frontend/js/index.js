/* global apiCall */

let currentFact = null;

async function initializeHome() {
  await loadRandomFact();
  document
    .getElementById("next-button")
    .addEventListener("click", loadRandomFact);
}

async function loadRandomFact() {
  const response = await apiCall("/catfacts/random/");
  if (!response.ok) {
    document.getElementById("fact-text").textContent = response.data.detail;
    return;
  }
  currentFact = response.data;
  document.getElementById("fact-text").textContent = currentFact.fact;
}
