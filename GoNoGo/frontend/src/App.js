import React, { useState, useEffect } from 'react';
import './App.css';

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
      <header className="App-header">
        {users.map(item => (
          <div key={item.id}>
            <h1>{item.email}</h1>
            <span>{item.first_name}</span>
          </div>
        ))}
      </header>
    </div>
  );
}

export default App;
