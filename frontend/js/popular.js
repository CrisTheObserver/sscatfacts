document.addEventListener(
    "DOMContentLoaded",
    loadPopular,
);

async function loadPopular() {
    const response = await apiCall("/catfacts/popular/");
    const container = document.getElementById("popular-container");
    console.log(response);
    if (!response.ok) {
        container.innerHTML =
            `<div class="alert alert-danger">
                ${response.data.detail}
            </div>`;
        return;
    }
    if (response.data.length === 0) {
        container.innerHTML ="<p>No facts available.</p>";
        return;
    }
    container.innerHTML = "";
    response.data.forEach(addCard, container);
}

function addCard(fact, containerName) {
    const container = document.getElementById("popular-container");
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