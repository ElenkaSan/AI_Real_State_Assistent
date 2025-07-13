import React, { useState } from 'react';
import MicInput from './MicInput';
import MessageBubble from './MessageBubble';

export default function ChatWindow({ onClose }) {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hi! How can I help you today?' }
  ]);

  const handleTranscript = async (text) => {
    setMessages((prev) => [...prev, { sender: 'user', text }]);

    try {
      const res = await fetch(`${process.env.REACT_APP_API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: 'demo', message: text }),
      });

      const data = await res.json();
      setMessages((prev) => [...prev, { sender: 'bot', text: data.response }]);
    } catch (err) {
      setMessages((prev) => [...prev, { sender: 'bot', text: 'Sorry, I could not process that.' }]);
    }
  };

  return (
    <div className="card shadow-lg" style={{ width: '350px', height: '500px' }}>
      <div className="card-header d-flex justify-content-between bg-dark text-white">
        <span>AI Assistant</span>
        <button onClick={onClose} className="btn-close btn-close-white"></button>
      </div>
      <div className="card-body overflow-auto d-flex flex-column">
        {messages.map((msg, i) => (
          <MessageBubble key={i} sender={msg.sender} text={msg.text} />
        ))}
      </div>
      <div className="card-footer">
        <MicInput onTranscript={handleTranscript} />
      </div>
    </div>
  );
}
