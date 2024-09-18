import React from 'react';
import { motion } from 'framer-motion';
import { User, Bot } from 'lucide-react';

// Helper function to format bullet points and bold text
const formatMessageWithBulletsAndBold = (message) => {
  // Check for lines starting with bullet points (* or -)
  const lines = message.split('\n');
  
  const isBulletPoint = (line) => line.trim().startsWith('*') || line.trim().startsWith('-');
  
  // Function to handle bolding text between ** **
  const formatBoldText = (text) => {
    const boldRegex = /\*\*(.*?)\*\*/g;
    return text.replace(boldRegex, (match, p1) => `<strong>${p1}</strong>`);
  };

  // Check if any line is a bullet point, if not, return the formatted message
  const containsBullets = lines.some(isBulletPoint);

  if (!containsBullets) {
    return (
      <p
        className="text-sm sm:text-base"
        dangerouslySetInnerHTML={{ __html: formatBoldText(message) }}
      />
    );
  }

  // Format the message into a list if bullet points are detected
  return (
    <ul className="list-disc list-inside text-sm sm:text-base">
      {lines.map((line, index) => (
        isBulletPoint(line) ? (
          <li key={index} dangerouslySetInnerHTML={{ __html: formatBoldText(line.replace(/^[*-]\s*/, '')) }}></li> // Bold text and render bullet points
        ) : (
          <p key={index} dangerouslySetInnerHTML={{ __html: formatBoldText(line) }}></p> // Format normal text with bold
        )
      ))}
    </ul>
  );
};

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
          className={`p-4 rounded-2xl shadow-lg ${isUser ? 'bg-blue-500 text-white mr-3' : 'bg-white text-gray-800 ml-3'}`}
          whileHover={{ scale: 1.02 }}
          transition={{ type: "spring", stiffness: 400, damping: 10 }}
        >
          {/* Use the formatting function to handle bullet points and bold text */}
          {formatMessageWithBulletsAndBold(message)}
        </motion.div>
        <div className={`w-10 h-10 rounded-full flex items-center justify-center ${isUser ? 'bg-blue-600' : 'bg-gray-200'}`}>
          {isUser ? <User size={20} color="white" /> : <Bot size={20} color="gray" />}
        </div>
      </div>
    </motion.div>
  );
};

export default ChatMessage;
  