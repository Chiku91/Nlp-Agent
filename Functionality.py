# 🎯 Root Project Structure
/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── lessons.py
│   │   │   ├── quizzes.py
│   │   │   ├── assistant.py
│   │   │   └── dashboard.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── models/
│   │   │   └── user.py
│   │   ├── services/
│   │   │   ├── chatbot.py
│   │   │   ├── diagram_generator.py
│   │   │   ├── engagement.py
│   │   │   └── swot.py
│   │   └── db/
│   │       └── mongodb.py
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── components/
│   │   │   ├── Assistant.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── QuizGame.tsx
│   │   │   └── Whiteboard.tsx
│   │   └── pages/
│   │       ├── Login.tsx
│   │       ├── Home.tsx
│   │       └── Profile.tsx
├── ai_services/
│   ├── chatbot/
│   │   └── chat_engine.py
│   ├── diagram_gen/
│   │   └── chart_generator.py
│   └── engagement/
│       └── facial_analysis.py
├── database/
│   └── seed_data.py
├── tests/
│   ├── test_api.py
│   └── test_chatbot.py
├── .env
├── requirements.txt
├── docker-compose.yml
└── README.md

# 🔧 Backend: FastAPI Main App
# backend/app/main.py
from fastapi import FastAPI
from app.api import auth, users, lessons, quizzes, assistant, dashboard

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(lessons.router)
app.include_router(quizzes.router)
app.include_router(assistant.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {"message": "EduAI backend up"}

# ⚙️ Config: backend/app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGO_URI = os.getenv("MONGO_URI")
    JWT_SECRET = os.getenv("JWT_SECRET")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

settings = Settings()

# 🧠 Chatbot Engine: ai_services/chatbot/chat_engine.py
import openai
from backend.app.core.config import settings

openai.api_key = settings.OPENAI_API_KEY

def get_chat_response(prompt, context=""):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": context}, {"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# 👩‍🏫 Frontend: Assistant.tsx (React + Tailwind)
// frontend/src/components/Assistant.tsx
import { useState } from 'react';

export default function Assistant() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const handleAsk = async () => {
    const res = await fetch("/api/assistant/ask", {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query }),
    });
    const data = await res.json();
    setResponse(data.answer);
  };

  return (
    <div className="p-4 border rounded-xl">
      <input className="w-full p-2 mb-2 border" value={query} onChange={e => setQuery(e.target.value)} />
      <button onClick={handleAsk} className="px-4 py-2 bg-blue-500 text-white rounded">Ask</button>
      <div className="mt-4 bg-gray-100 p-2 rounded">{response}</div>
    </div>
  );
}

# 🧩 Assistant API Endpoint: backend/app/api/assistant.py
from fastapi import APIRouter, Request
from pydantic import BaseModel
from backend.app.services.chatbot import get_chat_response

router = APIRouter(prefix="/api/assistant")

class Query(BaseModel):
    query: str

@router.post("/ask")
def ask(query: Query):
    response = get_chat_response(query.query)
    return {"answer": response}

# 🧪 Sample Test: tests/test_chatbot.py
def test_chat_response():
    from ai_services.chatbot.chat_engine import get_chat_response
    result = get_chat_response("What is photosynthesis?")
    assert "process" in result.lower()

// Updated AI Educational Platform Code with Advanced Features (including Multimodal Input and AI Integration)

import express from 'express';
import mongoose from 'mongoose';
import multer from 'multer';
import cors from 'cors';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import { Server } from 'socket.io';
import http from 'http';
import fs from 'fs';
import axios from 'axios';

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: '*' } });

app.use(cors());
app.use(express.json());

mongoose.connect('mongodb://localhost/eduai');

// --- Models ---
const User = mongoose.model('User', new mongoose.Schema({
  username: String,
  password: String,
  role: String
}));

const Assignment = mongoose.model('Assignment', new mongoose.Schema({
  title: String,
  description: String,
  file: String,
  submittedBy: String,
  grade: String,
  feedback: String
}));

const Quiz = mongoose.model('Quiz', new mongoose.Schema({
  question: String,
  options: [String],
  answer: String,
  badge: String
}));

// --- Middleware & Auth ---
const secret = 'secret';
const auth = async (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.sendStatus(401);
  try {
    req.user = jwt.verify(token, secret);
    next();
  } catch {
    res.sendStatus(403);
  }
};

// --- Routes ---
app.post('/register', async (req, res) => {
  const { username, password, role } = req.body;
  const hash = await bcrypt.hash(password, 10);
  await User.create({ username, password: hash, role });
  res.sendStatus(201);
});

app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  const user = await User.findOne({ username });
  if (user && await bcrypt.compare(password, user.password)) {
    const token = jwt.sign({ id: user._id, role: user.role }, secret);
    res.json({ token });
  } else {
    res.sendStatus(401);
  }
});

app.get('/dashboard-data', auth, (req, res) => {
  res.json({
    progress: Math.random() * 100,
    badges: ['Quiz Master', 'Top Scorer'],
    performance: {
      strengths: ['Math', 'Science'],
      weaknesses: ['English']
    }
  });
});

// --- Quiz System ---
app.post('/quiz', auth, async (req, res) => {
  const quiz = await Quiz.create(req.body);
  res.json(quiz);
});

app.get('/quiz', auth, async (req, res) => {
  const quizzes = await Quiz.find();
  res.json(quizzes);
});

// --- Assignment Uploads ---
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, 'uploads/'),
  filename: (req, file, cb) => cb(null, Date.now() + '-' + file.originalname)
});
const upload = multer({ storage });

app.post('/assignment', auth, upload.single('file'), async (req, res) => {
  const { title, description } = req.body;
  const file = req.file.filename;
  const submittedBy = req.user.id;
  await Assignment.create({ title, description, file, submittedBy });
  res.sendStatus(201);
});

app.get('/assignments', auth, async (req, res) => {
  const assignments = await Assignment.find();
  res.json(assignments);
});

app.post('/assignment/grade/:id', auth, async (req, res) => {
  const { grade, feedback } = req.body;
  await Assignment.findByIdAndUpdate(req.params.id, { grade, feedback });
  res.sendStatus(200);
});

// --- Multimodal Input: Image Classification (Mock) ---
app.post('/analyze-image', upload.single('image'), async (req, res) => {
  const filePath = `uploads/${req.file.filename}`;
  // Simulate image classification response
  res.json({ labels: ['diagram', 'math', 'whiteboard'] });
});

// --- AI Assistant (OpenAI Text Input Integration) ---
app.post('/ai-assistant', auth, async (req, res) => {
  const { message } = req.body;
  try {
    const openaiRes = await axios.post('https://api.openai.com/v1/chat/completions', {
      model: 'gpt-4',
      messages: [{ role: 'user', content: message }]
    }, {
      headers: {
        'Authorization': `Bearer YOUR_OPENAI_API_KEY`
      }
    });
    res.json({ reply: openaiRes.data.choices[0].message.content });
  } catch (error) {
    res.status(500).json({ error: 'AI service failed' });
  }
});

// --- Collaborative Whiteboard (Sockets) ---
io.on('connection', (socket) => {
  socket.on('draw', (data) => socket.broadcast.emit('draw', data));
});

// --- Start Server ---
server.listen(4000, () => console.log('Server running on http://localhost:4000'));
