import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Send, Database, Settings, Terminal, Play, Bot, User,
  ChevronDown, Activity, Sparkles, Command, ShieldCheck,
  Plus, MessageSquare, Trash2, X
} from 'lucide-react';
import './index.css';

const API_URL = 'http://localhost:5000/api/query'; // Adjust if backend port differs

// --- Components ---

const SettingsModal = ({ config, setConfig, onClose }) => {
  return (
    <motion.div
      className="modal-overlay"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <motion.div
        className="modal-content"
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.95, opacity: 0 }}
      >
        <div className="modal-header">
          <h2>Settings</h2>
          <button onClick={onClose} className="icon-btn"><X size={20} /></button>
        </div>

        <div className="modal-body">
          <div className="field">
            <label>Database URL</label>
            <input
              className="input-styled"
              type="password"
              placeholder="postgresql://user:pass@host/db"
              value={config.database_url}
              onChange={(e) => setConfig({ ...config, database_url: e.target.value })}
            />
            <p className="hint">Connection string to your PostgreSQL database.</p>
          </div>

          <div className="field">
            <label>LLM Provider</label>
            <div className="select-wrapper">
              <select
                className="input-styled"
                value={config.provider}
                onChange={(e) => setConfig({ ...config, provider: e.target.value })}
              >
                <option value="gemini">Google Gemini</option>
                <option value="groq">Groq Llama 3</option>
              </select>
            </div>
          </div>

          <div className="field">
            <label>API Key</label>
            <input
              className="input-styled"
              type="password"
              placeholder="sk-..."
              value={config.api_key}
              onChange={(e) => setConfig({ ...config, api_key: e.target.value })}
            />
          </div>

          <div className="field">
            <label>SQL Mode</label>
            <div className="select-wrapper">
              <select
                className="input-styled"
                value={config.sql_mode}
                onChange={(e) => setConfig({ ...config, sql_mode: e.target.value })}
              >
                <option value="read_only">Read Only (SELECT)</option>
                <option value="write_no_delete">Write (No Delete)</option>
                <option value="write_full">Full CRUD</option>
              </select>
            </div>
          </div>
        </div>

        <div className="modal-footer">
          <button className="btn-primary" onClick={onClose}>Save & Close</button>
        </div>
      </motion.div>
    </motion.div>
  );
};

// --- Main App ---

function App() {
  // State
  const [sessions, setSessions] = useState(() => {
    const saved = localStorage.getItem('chat_sessions');
    return saved ? JSON.parse(saved) : [{ id: 1735700000000, title: 'New Chat', messages: [] }];
  });
  const [activeSessionId, setActiveSessionId] = useState(() => {
    const saved = localStorage.getItem('chat_sessions');
    return saved ? JSON.parse(saved)[0].id : 1735700000000;
  });

  const [config, setConfig] = useState(() => {
    const saved = localStorage.getItem('app_config');
    return saved ? JSON.parse(saved) : {
      database_url: '',
      api_key: '',
      provider: 'groq',
      sql_mode: 'write_full',
    };
  });

  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [showSettings, setShowSettings] = useState(false);

  const bottomRef = useRef(null);

  // Persistence
  useEffect(() => {
    localStorage.setItem('chat_sessions', JSON.stringify(sessions));
  }, [sessions]);

  useEffect(() => {
    localStorage.setItem('app_config', JSON.stringify(config));
  }, [config]);

  // Scroll to bottom
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [sessions, activeSessionId, loading]);

  // Derived state
  const activeSession = sessions.find(s => s.id === activeSessionId) || sessions[0];
  const messages = activeSession ? activeSession.messages : [];

  // Actions
  const createNewSession = () => {
    const newSession = { id: Date.now(), title: 'New Chat', messages: [] };
    setSessions([newSession, ...sessions]);
    setActiveSessionId(newSession.id);
  };

  const deleteSession = (e, id) => {
    e.stopPropagation();
    const newSessions = sessions.filter(s => s.id !== id);
    if (newSessions.length === 0) {
      // Always keep at least one
      const fresh = { id: Date.now(), title: 'New Chat', messages: [] };
      setSessions([fresh]);
      setActiveSessionId(fresh.id);
    } else {
      setSessions(newSessions);
      if (activeSessionId === id) {
        setActiveSessionId(newSessions[0].id);
      }
    }
  };

  const handleSend = async (text = input) => {
    if (!text.trim()) return;

    // Optimistic Update
    const userMessage = { role: 'user', content: text };
    const updatedMessages = [...messages, userMessage];

    // Update Session
    const updatedSessions = sessions.map(s => {
      if (s.id === activeSessionId) {
        return {
          ...s,
          messages: updatedMessages,
          title: s.messages.length === 0 ? text.slice(0, 30) + (text.length > 30 ? '...' : '') : s.title
        };
      }
      return s;
    });
    setSessions(updatedSessions);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(API_URL, {
        question: text,
        chat_history: updatedMessages.map(m => ({ role: m.role, content: m.content })),
        database_url: config.database_url,
        api_key: config.api_key,
        provider: config.provider,
        sql_mode: config.sql_mode,
        model: 'llama-3.3-70b-versatile'
      });

      const { answer, sql, results, kind } = response.data;

      const assistantMessage = {
        role: 'assistant',
        content: answer,
        sql: sql,
        results: results,
        kind: kind
      };

      setSessions(prev => prev.map(s =>
        s.id === activeSessionId
          ? { ...s, messages: [...updatedMessages, assistantMessage] }
          : s
      ));

    } catch (error) {
      console.error(error);
      const errorMsg = {
        role: 'assistant',
        content: `**Error:** ${error.response?.data?.error || error.message}`,
        isError: true
      };
      setSessions(prev => prev.map(s =>
        s.id === activeSessionId
          ? { ...s, messages: [...updatedMessages, errorMsg] }
          : s
      ));
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div id="root">
      {/* Sidebar History */}
      <motion.div
        className="sidebar"
        initial={{ x: -20, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
      >
        <div className="sidebar-header">
          <button className="new-chat-btn" onClick={createNewSession}>
            <Plus size={18} />
            <span>New Chat</span>
          </button>
        </div>

        <div className="sidebar-content">
          <div className="history-label">Recent History</div>
          <div className="session-list">
            {sessions.map(session => (
              <div
                key={session.id}
                className={`session-item ${session.id === activeSessionId ? 'active' : ''}`}
                onClick={() => setActiveSessionId(session.id)}
              >
                <MessageSquare size={16} className="session-icon" />
                <span className="session-title">{session.title}</span>
                <button
                  className="delete-btn"
                  onClick={(e) => deleteSession(e, session.id)}
                >
                  <Trash2 size={14} />
                </button>
              </div>
            ))}
          </div>
        </div>

        <div className="sidebar-footer">
          <button className="settings-btn" onClick={() => setShowSettings(true)}>
            <Settings size={18} />
            <span>Settings</span>
          </button>
        </div>
      </motion.div>

      {/* Main Chat */}
      <div className="chat-layout">
        <header className="navbar">
          <h1>
            <Sparkles size={18} style={{ color: '#2563EB' }} />
            NL → SQL Assistant
          </h1>
          <div className="status-indicator">
            <div className={`status-dot ${config.api_key ? 'active' : ''}`} />
            <span>{config.api_key ? 'Connected' : 'No API Key'}</span>
          </div>
        </header>

        <div className="messages-area">
          <AnimatePresence>
            {messages.length === 0 && (
              <motion.div
                className="empty-state"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
              >
                <div className="empty-icon"><Activity size={32} /></div>
                <h2>Start a new conversation</h2>
                <div className="suggestion-grid">
                  <div className="suggestion-card" onClick={() => handleSend("Show table schema")}>
                    <h4>Schema</h4><p>View database structure</p>
                  </div>
                  <div className="suggestion-card" onClick={() => handleSend("List top 5 users")}>
                    <h4>Users</h4><p>Show top 5 users</p>
                  </div>
                </div>
              </motion.div>
            )}

            {messages.map((msg, idx) => (
              <motion.div
                key={idx}
                className="message-row"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <div className={`message-avatar ${msg.role === 'user' ? 'user' : 'ai'}`}>
                  {msg.role === 'user' ? <User size={18} /> : <Bot size={18} />}
                </div>

                <div className={`message-bubble ${msg.role}`}>
                  <div className="prose">
                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                  </div>

                  {msg.sql && (
                    <div className="sql-card">
                      <div className="sql-header">
                        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                          <Terminal size={14} />
                          <span>Generated SQL</span>
                        </div>
                      </div>
                      <pre className="sql-code"><code>{msg.sql}</code></pre>
                    </div>
                  )}

                  {msg.results && msg.results.length > 0 && (
                    <div className="table-wrapper">
                      <div className="table-stats">
                        <Activity size={12} style={{ marginRight: '4px', display: 'inline' }} />
                        Result: {msg.results.length} rows
                      </div>
                      <div className="data-table-container">
                        <table className="data-table">
                          <thead>
                            <tr>
                              {/* Detect if first row is array or object to determine headers */}
                              {Array.isArray(msg.results[0])
                                ? msg.results[0].map((_, i) => <th key={i}>Col {i + 1}</th>)
                                : Object.keys(msg.results[0]).map(key => <th key={key}>{key}</th>)
                              }
                            </tr>
                          </thead>
                          <tbody>
                            {msg.results.map((row, i) => (
                              <tr key={i}>
                                {Array.isArray(row)
                                  ? row.map((val, j) => (
                                    <td key={j}>
                                      {typeof val === 'object' && val !== null ? JSON.stringify(val) : String(val)}
                                    </td>
                                  ))
                                  : Object.values(row).map((val, j) => (
                                    <td key={j}>
                                      {typeof val === 'object' && val !== null ? JSON.stringify(val) : String(val)}
                                    </td>
                                  ))
                                }
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {loading && (
            <div className="message-row">
              <div className="message-avatar ai"><Bot size={18} /></div>
              <div className="typing-indicator"><div className="dot" /><div className="dot" /><div className="dot" /></div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        <div className="input-section">
          <div className="input-container">
            <textarea
              className="chat-input"
              placeholder="Ask a question..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
            />
            <button className="send-btn" onClick={() => handleSend()} disabled={loading || !input.trim()}>
              <Send size={18} />
            </button>
          </div>
        </div>
      </div>

      {/* Settings Modal */}
      <AnimatePresence>
        {showSettings && (
          <SettingsModal
            config={config}
            setConfig={setConfig}
            onClose={() => setShowSettings(false)}
          />
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;
