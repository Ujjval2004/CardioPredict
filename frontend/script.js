const BASE_URL = "http://127.0.0.1:5000";

function getToken() {
  return localStorage.getItem("token");
}

function logout() {
  localStorage.removeItem("token");
  alert("Logged out");
  window.location.href = "index.html";
}

async function request(url, method, data = null) {
  return fetch(BASE_URL + url, {
    method: method,
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + getToken()
    },
    body: data ? JSON.stringify(data) : null
  });
}