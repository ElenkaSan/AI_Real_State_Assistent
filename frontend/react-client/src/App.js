import React, { useState } from "react";
import ChatWindow from "./components/ChatWindow";
import nycImage from "./assets/nyc-bg.jpg"; // Put your image here

function App() {
  const [showChat, setShowChat] = useState(false);

  return (
    <div
      className="bg-dark text-white d-flex flex-column justify-content-center align-items-center vh-100"
      style={{
        backgroundImage: `url(${nycImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        position: "relative"
      }}
    >
      <div className="text-center bg-dark bg-opacity-50 p-4 rounded">
        <h1 className="display-4">Okada & Co</h1>
        <h2>AI Real Estate Assistant & CRM</h2>
        <p className="lead">
          Voice-powered AI assistant for commercial listings & broker tools.
        </p>
      </div>

      {!showChat && (
        <button
          className="btn btn-light rounded-circle position-absolute"
          style={{ bottom: "20px", right: "20px", width: "60px", height: "60px" }}
          onClick={() => setShowChat(true)}
        >
          💬
        </button>
      )}

      {showChat && (
        <div className="position-absolute bottom-0 end-0 m-3">
          <ChatWindow onClose={() => setShowChat(false)} />
        </div>
      )}
    </div>
  );
}

export default App;
