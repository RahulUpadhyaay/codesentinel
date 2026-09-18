import React, { useState } from 'react';
import api from '../api';
import { Shield, Lock, User, Mail } from 'lucide-react';

export default function Auth({ onLoginSuccess }) {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isLogin) {
        // Login Request
        const res = await api.post('/api/auth/login', { email, password });
        localStorage.setItem('token', res.data.access_token);
        localStorage.setItem('user_name', res.data.user_name);
        onLoginSuccess(res.data.user_name);
      } else {
        // Register Request
        await api.post('/api/auth/register', { email, password, full_name: fullName });
        setIsLogin(true);
        alert('Registration successful! Please login with your credentials.');
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="bg-slate-800 border border-slate-700 p-8 rounded-2xl shadow-2xl w-full max-w-md">
        <div className="flex justify-center mb-4">
          <div className="bg-emerald-500/20 p-3 rounded-xl border border-emerald-500/40">
            <Shield className="w-10 h-10 text-emerald-400" />
          </div>
        </div>
        <h1 className="text-2xl font-bold text-center text-white mb-2">CodeSentinel AI</h1>
        <p className="text-slate-400 text-center text-sm mb-6">
          {isLogin ? 'Sign in to access AI Code Security Auditor' : 'Create an account to scan your code'}
        </p>

        {error && (
          <div className="bg-red-500/20 border border-red-500/50 text-red-300 p-3 rounded-lg text-sm mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {!isLogin && (
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Full Name</label>
              <div className="relative">
                <User className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                <input
                  type="text"
                  required
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg py-2 pl-9 pr-3 text-sm text-white focus:outline-none focus:border-emerald-500"
                  placeholder="Rahul Upadhyay"
                />
              </div>
            </div>
          )}

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Email Address</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg py-2 pl-9 pr-3 text-sm text-white focus:outline-none focus:border-emerald-500"
                placeholder="rahul@example.com"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg py-2 pl-9 pr-3 text-sm text-white focus:outline-none focus:border-emerald-500"
                placeholder="••••••••"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-semibold py-2.5 rounded-lg transition-colors shadow-lg shadow-emerald-500/20"
          >
            {loading ? 'Processing...' : isLogin ? 'Sign In' : 'Create Account'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <button
            onClick={() => setIsLogin(!isLogin)}
            className="text-slate-400 hover:text-emerald-400 text-xs transition-colors"
          >
            {isLogin ? "Don't have an account? Sign Up" : 'Already have an account? Sign In'}
          </button>
        </div>
      </div>
    </div>
  );
}