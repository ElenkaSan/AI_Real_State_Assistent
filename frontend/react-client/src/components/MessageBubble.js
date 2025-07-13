import React from 'react';

export default function MessageBubble({ sender, text }) {
  const isUser = sender === 'user';

  return (
    <div
      className={`p-2 rounded-lg mb-2 ${
        isUser ? 'card bg-light text-dark align-self-end text-end' : 'card bg-secondary bg-opacity-50 text-dark align-self-start'
      }`}
      style={{ maxWidth: '80%' }}
    >
      <div style={{ fontWeight: 'bold', fontSize: '0.85rem', marginBottom: '0.25rem' }}>
        {isUser ? 'You' : 'AI Assistant'}
      </div>
      <div>{text}</div>
    </div>
  );
}
