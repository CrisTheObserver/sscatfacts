/* global register */

const form = document.getElementById("register-form");
form.addEventListener("submit", handleRegister);

async function handleRegister(event) {
  event.preventDefault();
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirm-password").value;
  if (password !== confirmPassword) {
    alert("Passwords do not match.");
    return;
  }
  const response = await register(username, password);
  if (!response.ok) {
    const message =
      response.data.detail ??
      response.data.username?.[0] ??
      response.data.password?.[0] ??
      "Registration failed.";

    alert(message);
    return;
  }
  window.location.href = "login.html";
}
