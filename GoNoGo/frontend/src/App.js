import React, { useState, useEffect } from 'react';
import './App.css';
import Login from './Pages/Login'

function App() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch('http://127.0.0.1:8000/login/');
        const usersData = await res.json();
        setUsers(usersData);
      } catch (e) {
        console.log(e);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="App">
      <Login />
    </div>
  );
}

export default App;
