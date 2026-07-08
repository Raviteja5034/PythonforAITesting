/**
 * app.js — BPI Q&A Chatbot frontend logic
 * Handles: sending questions, rendering answers, showing sources, health checks
 */

const API_BASE = window.location.origin;

// ── DOM refs ──────────────────────────────────────────────────────────────────
const chatMessages    = document.getElementById("chat-messages");
const questionInput   = document.getElementById("question-input");
const sendBtn         = document.getElementById("send-btn");
const typingIndicator = document.getElementById("typing-indicator");
const statusBadge     = document.getElementById("status-badge");
const charHint        = document.getElementById("char-hint");
const infoModel       = document.getElementById("info-model");
const infoDocs        = document.getElementById("info-docs");
const infoWatcher     = document.getElementById("info-watcher");
const infoLastIngest  = document.getElementById("info-last-ingest");
const infoLastFile    = document.getElementById("info-last-file");

// ── Character counter ─────────────────────────────────────────────────────────
questionInput.addEventListener("input", () => {
  const len = questionInput.value.length;
  charHint.textContent = `${len} / 2000`;
  charHint.style.color = len > 1800 ? "#dc2626" : "";
});

// ── Send on Enter (Shift+Enter = newline) ─────────────────────────────────────
questionInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendQuestion();
  }
});

// ── Fill question from sidebar buttons ────────────────────────────────────────
function fillQuestion(btn) {
  questionInput.value = btn.textContent.trim();
  charHint.textContent = `${questionInput.value.length} / 2000`;
  questionInput.focus();
}

// ── Append a message bubble to chat ──────────────────────────────────────────
function appendMessage(role, html, sources = []) {
  const wrapper = document.createElement("div");
  wrapper.className = `message message--${role}`;

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = role === "bot" ? "🤖" : "👤";

  const bubble = document.createElement("div");
  bubble.className = "bubble" + (role === "error" ? " bubble--error" : "");
  bubble.innerHTML = html;

  // Sources intentionally not displayed

  wrapper.appendChild(avatar);
  wrapper.appendChild(bubble);
  chatMessages.appendChild(wrapper);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return wrapper;
}

// ── Main send function ────────────────────────────────────────────────────────
async function sendQuestion() {
  const question = questionInput.value.trim();
  if (!question) return;

  // Append user message
  appendMessage("user", `<p>${escapeHtml(question)}</p>`);
  questionInput.value = "";
  charHint.textContent = "0 / 2000";

  // Disable input while waiting
  sendBtn.disabled = true;
  questionInput.disabled = true;

  // Show typing indicator with elapsed timer so testers know it's working
  typingIndicator.classList.remove("hidden");
  chatMessages.scrollTop = chatMessages.scrollHeight;
  const timerEl = document.getElementById("typing-timer");
  let elapsed = 0;
  const timer = setInterval(() => {
    elapsed++;
    if (timerEl) timerEl.textContent = `Thinking… ${elapsed}s`;
  }, 1000);

  try {
    const resp = await fetch(`${API_BASE}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    clearInterval(timer);
    typingIndicator.classList.add("hidden");
    if (timerEl) timerEl.textContent = "Thinking…";

    if (!resp.ok) {
      const err = await resp.json().catch(() => ({ detail: resp.statusText }));
      appendMessage("error", `<p><strong>Error ${resp.status}:</strong> ${escapeHtml(err.detail || "Unknown error")}</p>`);
    } else {
      const data = await resp.json();
      const answerHtml = formatAnswer(data.answer);
      appendMessage("bot", answerHtml, data.sources || []);
    }
  } catch (err) {
    clearInterval(timer);
    typingIndicator.classList.add("hidden");
    if (timerEl) timerEl.textContent = "Thinking…";
    appendMessage("error", `<p><strong>Connection Error:</strong> Cannot reach the backend server. Make sure it is running on <code>localhost:8000</code>.</p>`);
  } finally {
    sendBtn.disabled = false;
    questionInput.disabled = false;
    questionInput.focus();
  }
}

// ── Format answer text into HTML ──────────────────────────────────────────────
function formatAnswer(text) {
  if (!text) return "<p>No answer returned.</p>";

  // Convert markdown-ish content to basic HTML
  let html = escapeHtml(text);

  // Bold: **text**
  html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");

  // Convert numbered lists: lines starting with "1. "
  html = html.replace(/^(\d+)\.\s+(.+)$/gm, "<li>$2</li>");
  html = html.replace(/(<li>.*<\/li>)/s, "<ol>$1</ol>");

  // Convert bullet lists: lines starting with "- " or "• "
  html = html.replace(/^[-•]\s+(.+)$/gm, "<li>$1</li>");

  // Wrap consecutive <li> not inside <ol> in <ul>
  html = html.replace(/(?<!<ol>)(<li>(?:(?!<\/ol>).)*<\/li>)(?!<\/ol>)/gs, (m) => {
    if (!m.startsWith("<ol>")) return `<ul>${m}</ul>`;
    return m;
  });

  // Convert double newlines to paragraphs
  const paragraphs = html.split(/\n{2,}/);
  return paragraphs
    .map(p => p.trim())
    .filter(p => p.length > 0)
    .map(p => {
      if (p.startsWith("<ul>") || p.startsWith("<ol>") || p.startsWith("<li>")) return p;
      // Replace single newlines within a paragraph with <br>
      return `<p>${p.replace(/\n/g, "<br>")}</p>`;
    })
    .join("");
}

// ── Health check ──────────────────────────────────────────────────────────────
let _prevIngestPending = false;

async function checkHealth() {
  try {
    const resp = await fetch(`${API_BASE}/health`);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const data = await resp.json();

    infoModel.textContent      = data.ollama_model || "—";
    infoDocs.textContent       = data.vectorstore_ready ? "✅ Loaded" : "⚠️ Not loaded";
    infoWatcher.textContent    = data.watcher_active ? "✅ Active" : "⚠️ Off";
    infoLastIngest.textContent = data.last_ingest   || "—";
    infoLastFile.textContent   = data.last_changed_file || "—";

    if (data.ingest_pending) {
      statusBadge.textContent = "⏳ Updating…";
      statusBadge.className   = "badge badge--checking";
    } else if (data.vectorstore_ready) {
      statusBadge.textContent = "✅ Ready";
      statusBadge.className   = "badge badge--ready";
    } else {
      statusBadge.textContent = "⚠️ No Docs";
      statusBadge.className   = "badge badge--error";
    }

    // If ingest just finished → notify tester in chat
    if (_prevIngestPending && !data.ingest_pending && data.vectorstore_ready) {
      appendMessage("bot",
        `<p>📄 <strong>Documents updated!</strong> New files from the share path have been indexed. You can now ask questions about them.</p>`
      );
    }
    _prevIngestPending = data.ingest_pending;

  } catch (e) {
    statusBadge.textContent = "❌ Offline";
    statusBadge.className   = "badge badge--error";
    infoModel.textContent   = "—";
    infoDocs.textContent    = "Server not running";
    infoWatcher.textContent = "—";
  }
}

// ── Utility: escape HTML ──────────────────────────────────────────────────────
function escapeHtml(str) {
  if (!str) return "";
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  // Wire send button
  sendBtn.addEventListener("click", sendQuestion);

  // Wire quick-question buttons
  document.querySelectorAll(".quick-questions button").forEach(btn => {
    btn.addEventListener("click", () => fillQuestion(btn));
  });

  // Wire refresh button
  document.getElementById("refresh-btn").addEventListener("click", checkHealth);

  checkHealth();
  // Poll health every 15 seconds to show live watcher / ingest status
  setInterval(checkHealth, 15000);
  questionInput.focus();
});
