import React, { useState } from 'react';
import Chatbot from './Chatbot';
import Welcome from './Welcome';

function App() {
  const [showChatbot, setShowChatbot] = useState(false);

  const handleStartChat = () => {
    setShowChatbot(true);
  };

  return (
    <div className="h-screen flex items-center justify-center">
      {showChatbot ? (
        <Chatbot />
      ) : (
        <Welcome onStartChat={handleStartChat} />
      )}
    </div>
  );
}

export default App;