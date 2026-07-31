const form = document.getElementById("login-form");
form.addEventListener("submit",handleLogin,);

async function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const response = await login(username,password);
    if (!response.ok) {
        alert(response.data.detail)
        return;
    }
    window.location.href = "index.html";
}