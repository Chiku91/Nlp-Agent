// React Frontend for Edu AI Platform

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import axios from 'axios';

import Login from './components/Login';
import Dashboard from './components/Dashboard';
import Quiz from './components/Quiz';
import Assignments from './components/Assignments';
import ChatAssistant from './components/ChatAssistant';
import Whiteboard from './components/Whiteboard';

const App = () => {
  const [token, setToken] = useState(localStorage.getItem('token'));

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token);
    }
  }, [token]);

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login setToken={setToken} />} />
        <Route path="/dashboard" element={token ? <Dashboard token={token} /> : <Navigate to="/login" />} />
        <Route path="/quiz" element={token ? <Quiz token={token} /> : <Navigate to="/login" />} />
        <Route path="/assignments" element={token ? <Assignments token={token} /> : <Navigate to="/login" />} />
        <Route path="/assistant" element={token ? <ChatAssistant token={token} /> : <Navigate to="/login" />} />
        <Route path="/whiteboard" element={token ? <Whiteboard /> : <Navigate to="/login" />} />
        <Route path="*" element={<Navigate to="/dashboard" />} />
      </Routes>
    </Router>
  );
};

export default App;


// components/Login.jsx
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Login = ({ setToken }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const login = async () => {
    try {
      const res = await axios.post('http://localhost:4000/login', { username, password });
      setToken(res.data.token);
      navigate('/dashboard');
    } catch {
      alert('Invalid credentials');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="p-6 bg-white rounded-2xl shadow-xl w-80">
        <h2 className="text-2xl font-bold mb-4 text-center">Login</h2>
        <input onChange={e => setUsername(e.target.value)} placeholder="Username" className="w-full mb-3 p-2 border rounded-xl" />
        <input onChange={e => setPassword(e.target.value)} type="password" placeholder="Password" className="w-full mb-3 p-2 border rounded-xl" />
        <button onClick={login} className="w-full bg-blue-600 text-white p-2 rounded-xl">Login</button>
      </div>
    </div>
  );
};
export default Login;

// components/Dashboard.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Dashboard = ({ token }) => {
  const [data, setData] = useState(null);
  useEffect(() => {
    axios.get('http://localhost:4000/dashboard-data', {
      headers: { Authorization: `Bearer ${token}` }
    }).then(res => setData(res.data));
  }, [token]);

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
      {data ? (
        <div className="space-y-4">
          <p>Progress: {data.progress.toFixed(2)}%</p>
          <p>Badges: {data.badges.join(', ')}</p>
          <p>Strengths: {data.performance.strengths.join(', ')}</p>
          <p>Weaknesses: {data.performance.weaknesses.join(', ')}</p>
        </div>
      ) : <p>Loading...</p>}
    </div>
  );
};
export default Dashboard;

// components/Quiz.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Quiz = ({ token }) => {
  const [quizzes, setQuizzes] = useState([]);
  const [score, setScore] = useState(0);

  useEffect(() => {
    axios.get('http://localhost:4000/quiz', {
      headers: { Authorization: `Bearer ${token}` }
    }).then(res => setQuizzes(res.data));
  }, [token]);

  const checkAnswer = (quiz, answer) => {
    if (quiz.answer === answer) {
      setScore(score + 1);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Quiz</h1>
      <p className="mb-4">Score: {score}</p>
      {quizzes.map((quiz, i) => (
        <div key={i} className="mb-4 p-4 border rounded-xl shadow-sm">
          <p className="font-semibold">{quiz.question}</p>
          {quiz.options.map(opt => (
            <button
              key={opt}
              onClick={() => checkAnswer(quiz, opt)}
              className="mr-2 mt-2 bg-blue-500 text-white px-3 py-1 rounded-xl">
              {opt}
            </button>
          ))}
        </div>
      ))}
    </div>
  );
};
export default Quiz;

// components/Assignments.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Assignments = ({ token }) => {
  const [assignments, setAssignments] = useState([]);
  const [file, setFile] = useState(null);
  const [title, setTitle] = useState('');
  const [desc, setDesc] = useState('');

  const fetchAssignments = () => {
    axios.get('http://localhost:4000/assignments', {
      headers: { Authorization: `Bearer ${token}` }
    }).then(res => setAssignments(res.data));
  };

  const upload = async () => {
    const form = new FormData();
    form.append('file', file);
    form.append('title', title);
    form.append('description', desc);
    await axios.post('http://localhost:4000/assignment', form, {
      headers: { Authorization: `Bearer ${token}` }
    });
    fetchAssignments();
  };

  useEffect(() => {
    fetchAssignments();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Assignments</h1>
      <div className="mb-6 space-y-2">
        <input placeholder="Title" onChange={e => setTitle(e.target.value)} className="border p-2 rounded-xl w-full" />
        <input placeholder="Description" onChange={e => setDesc(e.target.value)} className="border p-2 rounded-xl w-full" />
        <input type="file" onChange={e => setFile(e.target.files[0])} className="border p-2 rounded-xl w-full" />
        <button onClick={upload} className="bg-green-600 text-white px-4 py-2 rounded-xl">Upload</button>
      </div>
      <h2 className="text-xl font-semibold mb-2">Submitted Assignments</h2>
      {assignments.map((a, i) => (
        <div key={i} className="border p-3 rounded-xl mb-2">
          <p><strong>{a.title}</strong></p>
          <p>{a.description}</p>
          <p className="text-sm">Grade: {a.grade || 'Pending'}</p>
        </div>
      ))}
    </div>
  );
};
export default Assignments;

// components/ChatAssistant.jsx
import React, { useState } from 'react';
import axios from 'axios';

const ChatAssistant = ({ token }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const send = async () => {
    setMessages([...messages, { role: 'user', content: input }]);
    const res = await axios.post('http://localhost:4000/ai-assistant', { message: input }, {
      headers: { Authorization: `Bearer ${token}` }
    });
    setMessages([...messages, { role: 'user', content: input }, { role: 'assistant', content: res.data.reply }]);
    setInput('');
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">AI Assistant</h1>
      <div className="space-y-2 mb-4 max-h-80 overflow-y-auto">
        {messages.map((msg, i) => (
          <div key={i} className={`p-2 rounded-xl ${msg.role === 'user' ? 'bg-blue-100' : 'bg-gray-200'}`}>{msg.content}</div>
        ))}
      </div>
      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        className="border p-2 rounded-xl w-3/4"
      />
      <button onClick={send} className="ml-2 px-4 py-2 bg-blue-600 text-white rounded-xl">Send</button>
    </div>
  );
};
export default ChatAssistant;

// components/Whiteboard.jsx
import React, { useRef, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:4000');

const Whiteboard = () => {
  const canvasRef = useRef();
  const ctxRef = useRef();

  useEffect(() => {
    const canvas = canvasRef.current;
    canvas.width = 800;
    canvas.height = 500;
    const ctx = canvas.getContext('2d');
    ctx.lineWidth = 3;
    ctx.strokeStyle = '#333';
    ctxRef.current = ctx;

    socket.on('draw', ({ x, y, px, py }) => {
      ctx.beginPath();
      ctx.moveTo(px, py);
      ctx.lineTo(x, y);
      ctx.stroke();
    });
  }, []);

  const draw = (e) => {
    const canvas = canvasRef.current;
    const ctx = ctxRef.current;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    if (e.buttons === 1) {
      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.lineTo(x + 1, y + 1);
      ctx.stroke();
      socket.emit('draw', { x, y, px: x - 1, py: y - 1 });
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Whiteboard</h1>
      <canvas ref={canvasRef} onMouseMove={draw} className="border rounded-xl shadow-md" />
    </div>
  );
};
export default Whiteboard;


import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './Login';
import Dashboard from './Dashboard';
import Quiz from './Quiz';
import Assignments from './Assignments';
import ChatAssistant from './ChatAssistant';
import Whiteboard from './Whiteboard';

const App = () => {
  const isAuthenticated = !!localStorage.getItem('token');

  return (
    <Router>
      <div className="min-h-screen bg-gray-100 font-sans">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/dashboard"
            element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />}
          />
          <Route
            path="/quiz"
            element={isAuthenticated ? <Quiz /> : <Navigate to="/login" />}
          />
          <Route
            path="/assignments"
            element={isAuthenticated ? <Assignments /> : <Navigate to="/login" />}
          />
          <Route
            path="/chat"
            element={isAuthenticated ? <ChatAssistant /> : <Navigate to="/login" />}
          />
          <Route
            path="/whiteboard"
            element={isAuthenticated ? <Whiteboard /> : <Navigate to="/login" />}
          />
          <Route
            path="*"
            element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} />}
          />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
