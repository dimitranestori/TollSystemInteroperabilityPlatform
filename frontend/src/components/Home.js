import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  return (
    <div className="home-container">
      <h1>Welcome to ManagedToll</h1>
      <p>Select an action below:</p>
      <div className="home-buttons">
        <Link to="/pass-entry" className="home-button">
          Enter Pass Data
        </Link>
        <Link to="/cost-calculator" className="home-button">
          Calculate Costs
        </Link>
        
        {/* Ενημέρωση για να πηγαίνει στην σελίδα του StationsForm */}
        <Link to="/stations-form" className="home-button">
          View Statistics
        </Link>
      </div>
    </div>
  );
};

export default Home;
