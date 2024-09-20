import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Send, MessageCircle } from 'lucide-react';
import ChatMessage from './ChatMessage';
import { useNavigate } from 'react-router-dom';

const ChatWindow = () => {
  const [messages, setMessages] = useState([
    { message: 'Welcome! How can I assist you today?', sender: 'bot' }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const navigate = useNavigate();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    inputRef.current.focus();
  }, []);

  const sendMessage = async () => {
    if (input.trim() === '') return;

    setMessages(prev => [...prev, { message: input, sender: 'user' }]);
    setInput('');
    setIsTyping(true);

    try {
      const response = await axios.post('http://127.0.0.1:8000/chat', { message: input });
      setTimeout(() => {
        setMessages(prev => [...prev, { message: response.data.response, sender: 'bot' }]);
        setIsTyping(false);
      }, 500 + Math.random() * 1000);
    } catch (error) {
      setTimeout(() => {
        setMessages(prev => [...prev, { message: 'Sorry, I am not connected to the backend server.', sender: 'bot' }]);
        setIsTyping(false);
      }, 500);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleLogout = () => {
    navigate('/login');
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto p-4 bg-gradient-to-br from-indigo-100 to-purple-100 relative">
      {/* Top-right button container */}
      <div className="absolute top-4 right-4 space-x-4">
        <motion.button
          className="bg-indigo-600 text-white px-4 py-2 rounded-xl hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors duration-300 ease-in-out shadow-md"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => alert('Coming Soon...')}
        >
          Contact Lawyer
        </motion.button>
        <motion.button
          className="bg-purple-600 text-white px-4 py-2 rounded-xl hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 transition-colors duration-300 ease-in-out shadow-md"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleLogout}
        >
          Sign Out
        </motion.button>
      </div>

      {/* Header */}
      <motion.div 
        className="bg-white rounded-t-3xl shadow-lg p-6 mb-4"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold text-center text-indigo-700 flex items-center justify-center">
          <MessageCircle className="mr-2" size={32} />
          LegalSathi
        </h1>
      </motion.div>

      {/* Messages */}
      <motion.div 
        className="flex-1 overflow-y-auto p-6 bg-white rounded-3xl shadow-xl mb-4"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <div className="space-y-4">
          {messages.map((msg, index) => (
            <ChatMessage key={index} message={msg.message} sender={msg.sender} />
          ))}
        </div>
        {isTyping && (
          <div className="flex items-center space-x-2 text-indigo-500 mt-4">
            <span className="text-sm font-medium">Bot is typing</span>
            <motion.div
              className="w-2 h-2 bg-indigo-500 rounded-full"
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ repeat: Infinity, duration: 0.6, ease: "easeInOut" }}
            />
            <motion.div
              className="w-2 h-2 bg-indigo-500 rounded-full"
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ repeat: Infinity, duration: 0.6, ease: "easeInOut", delay: 0.2 }}
            />
            <motion.div
              className="w-2 h-2 bg-indigo-500 rounded-full"
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ repeat: Infinity, duration: 0.6, ease: "easeInOut", delay: 0.4 }}
            />
          </div>
        )}
        <div ref={messagesEndRef} />
      </motion.div>

      {/* Input field and send button */}
      <motion.div 
        className="flex"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <textarea
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          className="flex-1 p-4 border border-indigo-300 rounded-l-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none text-sm sm:text-base"
          placeholder="Type your message..."
          rows="3"
        />
        <motion.button
          onClick={sendMessage}
          className="px-6 bg-indigo-600 text-white rounded-r-xl hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <Send size={24} />
        </motion.button>
      </motion.div>
    </div>
  );
};

export default ChatWindow;
