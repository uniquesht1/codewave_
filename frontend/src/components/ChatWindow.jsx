import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Send } from 'lucide-react';
import ChatMessage from './ChatMessage';

const ChatWindow = () => {
  const [messages, setMessages] = useState([
    { message: 'Welcome! How can I assist you today?', sender: 'bot' }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

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
        setMessages(prev => [...prev, { message: 'Error connecting to server', sender: 'bot' }]);
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

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto p-4 bg-gray-100">
      <motion.h1 
        className="text-3xl font-bold mb-6 text-center text-blue-600"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        Legal Chatbot
      </motion.h1>
      <motion.div 
        className="flex-1 overflow-y-auto p-6 bg-white rounded-2xl shadow-xl"
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
          <div className="flex items-center space-x-2 text-gray-500 mt-4">
            <span className="text-sm">Bot is typing</span>
            <motion.div
              className="w-2 h-2 bg-gray-400 rounded-full"
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ repeat: Infinity, duration: 0.6, ease: "easeInOut" }}
            />
            <motion.div
              className="w-2 h-2 bg-gray-400 rounded-full"
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ repeat: Infinity, duration: 0.6, ease: "easeInOut", delay: 0.2 }}
            />
            <motion.div
              className="w-2 h-2 bg-gray-400 rounded-full"
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ repeat: Infinity, duration: 0.6, ease: "easeInOut", delay: 0.4 }}
            />
          </div>
        )}
        <div ref={messagesEndRef} />
      </motion.div>
      <motion.div 
        className="mt-6 flex"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <textarea
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          className="flex-1 p-4 border border-gray-300 rounded-l-xl focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none text-sm sm:text-base"
          placeholder="Type your message..."
          rows="3"
        />
        <motion.button
          onClick={sendMessage}
          className="px-6 bg-blue-500 text-white rounded-r-xl hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
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