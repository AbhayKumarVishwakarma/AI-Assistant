const BASE_URL = "http://127.0.0.1:8000";
const ENDPOINTS = {
  login: "/auth/login",
  signup: "/user/register",
  agent: "/agent/chat",
  health: "/health/ask",
};

// ===== STATE =====
let token = localStorage.getItem("token") || "";
let username = localStorage.getItem("username") || "";
let mode = localStorage.getItem("mode") || "agent";
let chats = { agent: [], health: [] }; // store per-mode chats

// ===== ELEMENTS =====
const chatEl = document.getElementById("chat");
const msgEl = document.getElementById("msg");
const sendBtn = document.getElementById("send");
const btnAgent = document.getElementById("btnAgent");
const btnHealth = document.getElementById("btnHealth");
const userBadge = document.getElementById("userBadge");
const authBtn = document.getElementById("authBtn");
const modalBackdrop = document.getElementById("modalBackdrop");
const toastEl = document.getElementById("toast");

// ===== INIT =====
updateAuthUI();
renderChat();
btnAgent.addEventListener("click", () => switchMode("agent"));
btnHealth.addEventListener("click", () => switchMode("health"));
authBtn.addEventListener("click", () => (token ? logout() : openModal()));
sendBtn.addEventListener("click", sendMessage);
msgEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// ===== HELPERS =====
function bubble(text, who = "bot") {
  const div = document.createElement("div");
  div.className = `bubble ${who}`;
  div.textContent = text;
  chatEl.appendChild(div);
  chatEl.scrollTop = chatEl.scrollHeight;
}

function toast(msg, type = "ok") {
  toastEl.textContent = msg;
  toastEl.className = `toast ${type}`;
  toastEl.style.display = "block";
  setTimeout(() => (toastEl.style.display = "none"), 2200);
}

function renderChat() {
  chatEl.innerHTML = "";
  chats[mode].forEach((m) => bubble(m.text, m.who));
}

function updateAuthUI() {
  userBadge.textContent = token ? `${username}` : "Not Logged In";
  authBtn.textContent = token ? "Logout" : "Login";
}

function switchMode(newMode) {
  if (mode === newMode) return; // no re-render if already active
  mode = newMode;
  localStorage.setItem("mode", mode);
  btnAgent.classList.toggle("active", mode === "agent");
  btnHealth.classList.toggle("active", mode === "health");
  renderChat();
}

// ===== AUTH =====
function openModal() {
  modalBackdrop.style.display = "flex";
  switchTab("login");
}
function closeModal() {
  modalBackdrop.style.display = "none";
}
function switchTab(tab) {
  document.getElementById("formLogin").style.display =
    tab === "login" ? "" : "none";
  document.getElementById("formSignup").style.display =
    tab === "signup" ? "" : "none";
  document
    .getElementById("tabLogin")
    .classList.toggle("active", tab === "login");
  document
    .getElementById("tabSignup")
    .classList.toggle("active", tab === "signup");
}

async function login() {
  const u = document.getElementById("loginUsername").value.trim();
  const p = document.getElementById("loginPassword").value;
  if (!u || !p) return toast("Username & password required", "warn");
  const form = new FormData();
  form.append("username", u);
  form.append("password", p);
  try {
    const res = await fetch(BASE_URL + ENDPOINTS.login, {
      method: "POST",
      body: form,
    });
    const data = await res.json();
    if (res.ok && data.access_token) {
      token = data.access_token;
      username = data.username;
      console.log(username);
      localStorage.setItem("token", token);
      localStorage.setItem("username", username);
      updateAuthUI();
      closeModal();
      toast("Logged in");
    } else toast(data.detail || "Login failed", "warn");
  } catch (e) {
    toast("Login error: " + e, "warn");
  }
}

async function signup() {
  const u = document.getElementById("signupUsername").value.trim();
  const p = document.getElementById("signupPassword").value;
  const e = document.getElementById("signupEmail").value.trim();
  if (!u || !p) return toast("Username & password required", "warn");
  try {
    const res = await fetch(BASE_URL + ENDPOINTS.signup, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: u,
        password: p,
        email: e || undefined,
      }),
    });
    const data = await res.json();
    if (res.ok) {
      toast("Signup successful. Please login.");
      switchTab("login");
    } else toast(data.detail || "Signup failed", "warn");
  } catch (err) {
    toast("Signup error: " + err, "warn");
  }
}

function logout() {
  token = "";
  username = "";
  localStorage.removeItem("token");
  localStorage.removeItem("username");
  updateAuthUI();
  toast("Logged out");
}

// ===== CHAT =====
async function sendMessage() {
  const text = msgEl.value.trim();
  if (!text) return;
  if (!token) {
    toast("Please login", "warn");
    openModal();
    return;
  }
  msgEl.value = "";
  sendBtn.disabled = true;
  chats[mode].push({ text, who: "user" });
  bubble(text, "user");
  const endpoint = mode === "agent" ? ENDPOINTS.agent : ENDPOINTS.health;
  try {
    const res = await fetch(BASE_URL + endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ query: text }),
    });
    const data = await res.json();
    const reply = data.answer || data.response || JSON.stringify(data);
    chats[mode].push({ text: reply, who: "bot" });
    bubble(reply, "bot");
  } catch (e) {
    chats[mode].push({ text: "Error: " + e, who: "bot" });
    bubble("Error: " + e, "bot");
  } finally {
    sendBtn.disabled = false;
  }
}
