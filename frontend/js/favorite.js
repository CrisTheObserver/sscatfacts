/* global apiCall, currentFact */

document
  .getElementById("favorite-btn")
  .addEventListener("click", toggleFavorite);

async function toggleFavorite() {
  const response = await apiCall(`/catfacts/${currentFact.id}/favorite/`, {
    method: "POST",
  });
  if (!response.ok) {
    alert(response.data.detail);
    return;
  } else {
    console.log(response);
  }
}
