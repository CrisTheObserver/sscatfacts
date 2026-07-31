/* global apiCall */

document.addEventListener("DOMContentLoaded", loadFavorites);

async function loadFavorites() {
  const response = await apiCall("/catfacts/favorites/");
  const container = document.getElementById("favorite-container");
  if (!response.ok) {
    container.innerHTML = `<div class="alert alert-danger">
                ${response.data.detail}
            </div>`;
    return;
  }
  if (response.data.length === 0) {
    container.innerHTML = "<p>No facts available.</p>";
    return;
  }
  container.innerHTML = "";
  response.data.forEach(addCard, container);
}

function addCard(fact) {
  const container = document.getElementById("favorite-container");
  container.innerHTML += `
        <div class="col-12">
            <div class="card">
                <div class="card-body bg-dark">
                    <p class="card-text text-light">
                        ${fact.fact}
                    </p>
                    <span class="badge bg-primary">
                        ❤️ ${fact.favorites_count}
                    </span>
                </div>
            </div>
        </div>
    `;
}
