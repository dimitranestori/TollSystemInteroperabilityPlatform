import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';  // Εισαγωγή του Routes αντί του Switch
import Home from './components/Home';
import PassEntryForm from './components/PassEntryForm';
import CostCalculator from './components/CostCalculator';
import StationsForm from './components/StationsForm'; // Εισαγωγή του StationsFormPage

const App = () => {
  return (
    <Router>
      <Routes>  {/* Αντικαταστήσαμε το Switch με το Routes */}
        <Route path="/" element={<Home />} /> {/* Χρησιμοποιούμε το element εδώ */}
        <Route path="/pass-entry" element={<PassEntryForm />} />
        <Route path="/cost-calculator" element={<CostCalculator />} />
        <Route path="/stations-form" element={<StationsForm />} /> {/* Χρησιμοποιούμε το element εδώ */}
      </Routes>
    </Router>
  );
};

export default App;
