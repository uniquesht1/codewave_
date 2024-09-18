import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { User, Mail, Lock, Phone, Calendar } from 'lucide-react';

const SignUp = () => {
    // Prefilled input values
    const [username, setUsername] = useState('john_doe'); // Example username
    const [email, setEmail] = useState('john@example.com'); // Example email
    const [password, setPassword] = useState('password123'); // Example password
    const [confirmPassword, setConfirmPassword] = useState('password123'); // Example confirm password
    const [phoneNumber, setPhoneNumber] = useState('123-456-7890'); // Example phone number
    const [dateOfBirth, setDateOfBirth] = useState('1990-01-01'); // Example date of birth
    
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();
        // Add sign-up logic here
        alert('Account created successfully!');
        navigate('/login'); // Route to login after sign up
    };

    return (
        <div className="flex h-screen justify-center items-center bg-gradient-to-br from-blue-100 to-purple-100">
            <motion.div 
                className="w-full max-w-md p-8 bg-white rounded-2xl shadow-lg"
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 0.5 }}
            >
                <h2 className='text-3xl font-bold mb-6 text-center text-indigo-700'>Sign Up</h2>
                <form onSubmit={handleSubmit} className="space-y-4">
                    {/* Username Input */}
                    <div className="relative">
                        <User className="absolute top-3 left-3 text-gray-400" size={20} />
                        <input
                            type="text"
                            id="username"
                            value={username}
                            placeholder='Username'
                            className='w-full pl-10 pr-3 py-2 rounded-full border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500'
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>
                    
                    {/* Email Input */}
                    <div className="relative">
                        <Mail className="absolute top-3 left-3 text-gray-400" size={20} />
                        <input
                            type="email"
                            id="email"
                            value={email}
                            placeholder='Email'
                            className='w-full pl-10 pr-3 py-2 rounded-full border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500'
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>

                    {/* Password Input */}
                    <div className="relative">
                        <Lock className="absolute top-3 left-3 text-gray-400" size={20} />
                        <input
                            type="password"
                            id="password"
                            value={password}
                            placeholder='Password'
                            className='w-full pl-10 pr-3 py-2 rounded-full border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500'
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>

                    {/* Confirm Password Input */}
                    <div className="relative">
                        <Lock className="absolute top-3 left-3 text-gray-400" size={20} />
                        <input
                            type="password"
                            id="confirmPassword"
                            value={confirmPassword}
                            placeholder='Confirm Password'
                            className='w-full pl-10 pr-3 py-2 rounded-full border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500'
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            required
                        />
                    </div>

                    {/* Phone Number Input */}
                    <div className="relative">
                        <Phone className="absolute top-3 left-3 text-gray-400" size={20} />
                        <input
                            type="tel"
                            id="phoneNumber"
                            value={phoneNumber}
                            placeholder='Phone Number'
                            className='w-full pl-10 pr-3 py-2 rounded-full border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500'
                            onChange={(e) => setPhoneNumber(e.target.value)}
                        />
                    </div>

                    {/* Date of Birth Input */}
                    <div className="relative">
                        <Calendar className="absolute top-3 left-3 text-gray-400" size={20} />
                        <input
                            type="date"
                            id="dateOfBirth"
                            value={dateOfBirth}
                            className='w-full pl-10 pr-3 py-2 rounded-full border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500'
                            onChange={(e) => setDateOfBirth(e.target.value)}
                        />
                    </div>

                    <div className='flex flex-col items-center'>
                        <motion.button 
                            className='w-full bg-indigo-600 text-white py-2 rounded-full hover:bg-indigo-700 transition duration-300'
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            Sign Up
                        </motion.button>
                        <a href="/login" className="mt-4 text-indigo-600 hover:text-indigo-800 transition duration-300">Already have an account? Log In</a>
                    </div>
                </form>
            </motion.div>
        </div>
    );
};

export default SignUp;
