/* global apiCall */

document.addEventListener("DOMContentLoaded", updateNavbar);

function saveTokens(access, refresh) {
  localStorage.setItem("access", access);
  localStorage.setItem("refresh", refresh);
}

function getAccessToken() {
  return localStorage.getItem("access");
}

function logout() {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
}

function isAuthenticated() {
  return getAccessToken() !== null;
}

async function login(username, password) {
  const response = await apiCall("/auth/login/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username,
      password,
    }),
  });
  if (response.ok) {
    saveTokens(response.data.access, response.data.refresh);
  }
  return response;
}

async function register(username, password) {
  return await apiCall("/auth/register/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username,
      password,
    }),
  });
}

function updateNavbar() {
  const authLink = document.getElementById("auth-link");
  if (!authLink) {
    return;
  }
  if (isAuthenticated()) {
    authLink.textContent = "Logout";
    authLink.href = "#";

    authLink.onclick = (event) => {
      event.preventDefault();
      logout();
      window.location.href = "index.html";
    };
  } else {
    authLink.textContent = "Login";
    authLink.href = "login.html";
    authLink.onclick = null;
  }
}
