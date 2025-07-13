// src/components/Header.js
import React from "react";

function Header({ onClose }) {
  return (
    <div className="bg-blue-600 text-white px-4 py-2 flex justify-between items-center">
      <h2 className="text-sm font-semibold">AI Assistant</h2>
      <button onClick={onClose} className="text-xl font-bold">
        ×
      </button>
    </div>
  );
}

export default Header;
