import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { User, Lock } from 'lucide-react';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('Username:', username);
        console.log('Password:', password);
        if (username === 'user' && password === 'user') {
            alert('Welcome');
        } else {
            alert('Invalid Credentials');
            setUsername('');
            setPassword('');
        }
    };

    return (
        <div className="flex items-center justify-center h-screen bg-cover bg-center" 
             style={{ 
                 backgroundImage: "url('https://images.pexels.com/photos/5668481/pexels-photo-5668481.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1')",
             }}>
            <motion.div 
                className="w-full max-w-md"
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 0.5 }}
            >
                <form onSubmit={handleSubmit} className="bg-[#fcfcfc] shadow-md rounded-lg px-8 pt-6 pb-8 mb-4">
                    <h2 className="text-3xl font-bold mb-6 text-center text-[#22333b]">LegalSathi</h2>
                    <div className="mb-4">
                        <div className="relative">
                            <User className="absolute top-3 left-3 text-gray-400" size={20} />
                            <input
                                type="text"
                                id="username"
                                value={username}
                                placeholder="Username"
                                className="w-full pl-10 pr-3 py-2 rounded-full border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                                onChange={(e) => setUsername(e.target.value)}
                                required
                            />
                        </div>
                    </div>
                    <div className="mb-6">
                        <div className="relative">
                            <Lock className="absolute top-3 left-3 text-gray-400" size={20} />
                            <input
                                type="password"
                                id="password"
                                value={password}
                                placeholder="Password"
                                className="w-full pl-10 pr-3 py-2 rounded-full border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                        </div>
                    </div>
                    <div className="flex flex-col items-center">
                        <motion.button 
                            className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-full focus:outline-none focus:shadow-outline"
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            Log In
                        </motion.button>
                        <a href="/CreateAccount" className="mt-4 text-indigo-600 hover:text-indigo-800 transition duration-300">Create New Account</a>
                    </div>
                </form>
            </motion.div>
        </div>
    );
};

export default Login;