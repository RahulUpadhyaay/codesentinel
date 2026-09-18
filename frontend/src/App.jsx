import React, { useState, useEffect } from 'react';
import Auth from './components/Auth';
import Auditor from './components/Auditor';

export default function App() {
  const [userName, setUserName] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const storedName = localStorage.getItem('user_name');
    if (token && storedName) {
      setUserName(storedName);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user_name');
    setUserName(null);
  };

  if (!userName) {
    return <Auth onLoginSuccess={(name) => setUserName(name)} />;
  }

  return <Auditor userName={userName} onLogout={handleLogout} />;
}