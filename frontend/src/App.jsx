import { useMemo, useRef, useState } from "react";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

const ROLES = [
  { id: "student", label: "Student", persona: "Friendly & Supportive Academic Assistant", icon: "🎓", email: "student@example.com" },
  { id: "parent", label: "Parent", persona: "Caring & Patient Parent Support Assistant", icon: "👨‍👩‍👧", email: "parent@example.com" },
  { id: "teacher", label: "Teacher", persona: "Professional Teaching Assistant", icon: "👩‍🏫", email: "teacher@example.com" },
  { id: "principal", label: "Principal", persona: "Professional Management Assistant", icon: "🏫", email: "principal@example.com" }
];

const LANGUAGES = [
  "English", "Hindi", "Tamil", "Telugu", "Marathi", "Bengali",
  "Gujarati", "Punjabi", "Kannada", "Malayalam", "Urdu"
];

function App() {
  const [role, setRole] = useState(null);
  const [email, setEmail] = useState("");
  const [session, setSession] = useState(null);
  const [language, setLanguage] = useState("English");
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [pendingAction, setPendingAction] = useState(null);
  const [listening, setListening] = useState(false);
  const recognitionRef = useRef(null);

  const roleMeta = useMemo(
    () => ROLES.find((item) => item.id === role),
    [role]
  );

  async function login() {
    setError("");
    if (!role || !email.trim()) {
      setError("Select your role and enter your email.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(`${API}/api/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, role })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Login failed");

      setSession(data);
      setMessages([
        {
          role: "assistant",
          content: `Hello ${data.user.name}. I'm CampusMind AI, your ${roleMeta.persona}. How can I help you today?`
        }
      ]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function sendMessage(text = message) {
    const trimmed = text.trim();
    if (!trimmed || !session || loading) return;

    setMessage("");
    setMessages((prev) => [...prev, { role: "user", content: trimmed }]);
    setLoading(true);

    try {
      const res = await fetch(`${API}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: session.session_id,
          message: trimmed,
          language
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "AI request failed");

      setMessages((prev) => [...prev, { role: "assistant", content: data.answer }]);
      setPendingAction(data.pending_action || null);
      speak(data.answer);
    } catch (err) {
      setMessages((prev) => [...prev, { role: "assistant", content: `Error: ${err.message}` }]);
    } finally {
      setLoading(false);
    }
  }

  async function confirmSupport() {
    if (!pendingAction || !session) return;

    setLoading(true);
    try {
      const res = await fetch(`${API}/api/support/confirm`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: session.session_id,
          action_type: pendingAction.type
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Unable to submit request");

      const requestId = data?.data?.request_id || "";
      const text = `Your ${pendingAction.type === "teacher" ? "teacher" : "school management"} support request has been submitted${requestId ? ` with request ID ${requestId}` : ""}.`;
      setMessages((prev) => [...prev, { role: "assistant", content: text }]);
      speak(text);
      setPendingAction(null);
    } catch (err) {
      setMessages((prev) => [...prev, { role: "assistant", content: `Error: ${err.message}` }]);
    } finally {
      setLoading(false);
    }
  }

  function startListening() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setError("Speech recognition is not supported in this browser.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = language === "Hindi" ? "hi-IN" : "en-IN";
    recognition.interimResults = false;
    recognition.continuous = false;

    recognition.onstart = () => setListening(true);
    recognition.onend = () => setListening(false);
    recognition.onerror = () => {
      setListening(false);
      setError("Speech recognition could not start.");
    };
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setMessage(transcript);
      sendMessage(transcript);
    };

    recognitionRef.current = recognition;
    recognition.start();
  }

  function speak(text) {
    if (!("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = language === "Hindi" ? "hi-IN" : "en-IN";
    window.speechSynthesis.speak(utterance);
  }

  function logout() {
    setSession(null);
    setRole(null);
    setEmail("");
    setMessages([]);
    setMessage("");
    setPendingAction(null);
  }

  if (!session) {
    return (
      <div className="landing">
        <div className="brand">CampusMind AI</div>
        <div className="orb idle"></div>
        <p className="eyebrow">Human-Like AI School Assistant</p>
        <h1>Meet your school assistant.</h1>
        <p className="muted">Choose your role to continue.</p>

        <div className="role-grid">
          {ROLES.map((item) => (
            <button
              key={item.id}
              className={`role-card ${role === item.id ? "active" : ""}`}
              onClick={() => {
                setRole(item.id);
                setEmail(item.email);
              }}
            >
              <div className="role-icon">{item.icon}</div>
              <div className="role-title">{item.label}</div>
              <div className="role-persona">{item.persona}</div>
            </button>
          ))}
        </div>

        {roleMeta && (
          <div className="login-card">
            <h2>{roleMeta.label} Login</h2>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
            />
            <div className="hint">Demo account: {roleMeta.email}</div>
            {error && <div className="error">{error}</div>}
            <button className="primary" onClick={login} disabled={loading}>
              {loading ? "Signing in…" : "Enter CampusMind AI"}
            </button>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <div className="brand">CampusMind AI</div>
          <div className="role-line">{session.user.role} · {session.user.name}</div>
        </div>
        <div className="top-actions">
          <select value={language} onChange={(e) => setLanguage(e.target.value)}>
            {LANGUAGES.map((item) => <option key={item}>{item}</option>)}
          </select>
          <button className="ghost" onClick={logout}>Logout</button>
        </div>
      </header>

      <main className="workspace">
        <section className="hero-row">
          <div>
            <p className="eyebrow">{roleMeta?.persona}</p>
            <h1>Hello, {session.user.name}.</h1>
            <p className="muted">Ask about attendance or support by typing or using your voice.</p>
          </div>
          <div className={`avatar ${listening || loading ? "active" : ""}`}>
            <div className="orb"></div>
            <div className="avatar-label">
              {listening ? "Listening…" : loading ? "Thinking…" : "CampusMind AI"}
            </div>
          </div>
        </section>

        <section className="quick-actions">
          {role === "student" && (
            <button onClick={() => setMessage("What is my attendance?")}>My attendance</button>
          )}
          {role === "parent" && (
            <>
              <button onClick={() => setMessage("How much attendance does Rahul have?")}>Child attendance</button>
              <button onClick={() => setMessage("I am not satisfied. I want to talk to my child's teacher.")}>Talk to Teacher</button>
              <button onClick={() => setMessage("I want to contact school management.")}>Contact Management</button>
            </>
          )}
          {role === "teacher" && (
            <>
              <button onClick={() => setMessage("Mark Rahul absent today.")}>Mark Rahul absent</button>
              <button onClick={() => setMessage("Show Rahul's attendance.")}>View attendance</button>
            </>
          )}
          {role === "principal" && (
            <button onClick={() => setMessage("What is the overall attendance?")}>School attendance analytics</button>
          )}
        </section>

        <section className="chat">
          <div className="chat-head">
            <div>
              <h2>Conversation</h2>
              <span>Qwen 2.5 3B · LangGraph · Mock ERP Services</span>
            </div>
            <div className="status">● Ready</div>
          </div>

          <div className="messages">
            {messages.map((item, index) => (
              <div key={index} className={`bubble ${item.role}`}>
                {item.content}
              </div>
            ))}
            {loading && <div className="bubble assistant">CampusMind AI is thinking…</div>}
          </div>

          {pendingAction && (
            <div className="confirm-card">
              <div>
                <strong>Human support confirmation</strong>
                <p>Confirm this request before it is submitted.</p>
              </div>
              <button className="primary" onClick={confirmSupport}>Confirm request</button>
            </div>
          )}

          <div className="composer">
            <button className={`mic ${listening ? "recording" : ""}`} onClick={startListening} title="Speak">
              🎙️
            </button>
            <input
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") sendMessage();
              }}
              placeholder="Ask CampusMind AI…"
            />
            <button className="primary send" onClick={() => sendMessage()}>Send</button>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
