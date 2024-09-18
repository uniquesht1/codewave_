import React from 'react';
import { motion } from 'framer-motion';
import { User, Bot } from 'lucide-react';

const ChatMessage = ({ message, sender }) => {
  const isUser = sender === 'user';
  
  return (
    <motion.div 
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-6`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className={`flex items-end ${isUser ? 'flex-row-reverse' : 'flex-row'} max-w-[80%]`}>
        <motion.div 
          className={`p-4 rounded-2xl shadow-lg ${
            isUser ? 'bg-blue-500 text-white mr-3' : 'bg-white text-gray-800 ml-3'
          }`}
          whileHover={{ scale: 1.02 }}
          transition={{ type: "spring", stiffness: 400, damping: 10 }}
        >
          <p className="text-sm sm:text-base">{message}</p>
        </motion.div>
        <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
          isUser ? 'bg-blue-600' : 'bg-gray-200'
        }`}>
          {isUser ? <User size={20} color="white" /> : <Bot size={20} color="gray" />}
        </div>
      </div>
    </motion.div>
  );
};

export default ChatMessage;