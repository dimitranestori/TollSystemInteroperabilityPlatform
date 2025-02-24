import React, { useState } from 'react';
import './CostCalculator.css';

const CostCalculator = () => {
  const [formData, setFormData] = useState({
    tollOpID: '',
    dateFrom: '',
    dateTo: '',
  });
  const [calculationResult, setCalculationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleCalculate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setCalculationResult(null);

    try {
      const response = await fetch(
        `https://localhost:9115/api/chargesBy/${formData.tollOpID}/${formData.dateFrom}/${formData.dateTo}`
      );
      
      if (!response.ok) {
        throw new Error('Failed to fetch data');
      }
      
      const data = await response.json();
      setCalculationResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="cost-calculator">
      <h2>Passes Cost Calculator</h2>
      <form onSubmit={handleCalculate}>
        <label htmlFor="tollOpID">Toll Operator ID:</label>
        <input
          type="text"
          id="tollOpID"
          name="tollOpID"
          value={formData.tollOpID}
          onChange={handleChange}
          required
        />

        <label htmlFor="dateFrom">From Date:</label>
        <input
          type="date"
          id="dateFrom"
          name="dateFrom"
          value={formData.dateFrom}
          onChange={handleChange}
          required
        />

        <label htmlFor="dateTo">To Date:</label>
        <input
          type="date"
          id="dateTo"
          name="dateTo"
          value={formData.dateTo}
          onChange={handleChange}
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? 'Calculating...' : 'Calculate'}
        </button>
      </form>

      {error && <p className="error">Error: {error}</p>}

      {calculationResult && (
        <div className="result">
          <h3>Calculation Result</h3>
          <p><strong>Toll Operator ID:</strong> {calculationResult.tollOpID}</p>
          <p><strong>Period:</strong> {calculationResult.periodFrom} to {calculationResult.periodTo}</p>
          <h4>Debts by Visiting Operators:</h4>
          {calculationResult.vOpList.length > 0 ? (
            <ul>
              {calculationResult.vOpList.map((op, index) => (
                <li key={index}>
                  <strong>Operator:</strong> {op.visitingOpID},
                  <strong> Passes:</strong> {op.nPasses},
                  <strong> Total Cost (€):</strong> {op.passesCost}
                </li>
              ))}
            </ul>
          ) : (
            <p>No debts recorded in this period.</p>
          )}
        </div>
      )}
    </div>
  );
};

export default CostCalculator;



















/**import React, { useState } from 'react';
import './CostCalculator.css';

const CostCalculator = () => {
  const [formData, setFormData] = useState({
    tollOpID: '',
    tagOpID: '',
    dateFrom: '',
    dateTo: '',
  });

  const [calculationResult, setCalculationResult] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleCalculate = (e) => {
    e.preventDefault();

    // Dummy calculation result for the frontend
    const dummyResult = {
      tollOpID: formData.tollOpID,
      tagOpID: formData.tagOpID,
      nPasses: Math.floor(Math.random() * 100), // Random number for dummy data
      passesCost: (Math.random() * 500).toFixed(2), // Random cost for dummy data
    };

    setCalculationResult(dummyResult);
  };

  return (
    <div className="cost-calculator">
      <h2>Passes Cost Calculator</h2>
      <form onSubmit={handleCalculate}>
        <label htmlFor="tollOpID">Toll Operator ID:</label>
        <input
          type="text"
          id="tollOpID"
          name="tollOpID"
          value={formData.tollOpID}
          onChange={handleChange}
          required
        />

        <label htmlFor="tagOpID">Tag Operator ID:</label>
        <input
          type="text"
          id="tagOpID"
          name="tagOpID"
          value={formData.tagOpID}
          onChange={handleChange}
          required
        />

        <label htmlFor="dateFrom">From Date:</label>
        <input
          type="date"
          id="dateFrom"
          name="dateFrom"
          value={formData.dateFrom}
          onChange={handleChange}
          required
        />

        <label htmlFor="dateTo">To Date:</label>
        <input
          type="date"
          id="dateTo"
          name="dateTo"
          value={formData.dateTo}
          onChange={handleChange}
          required
        />

        <button type="submit">Calculate</button>
      </form>

      {calculationResult && (
        <div className="result">
          <h3>Calculation Result</h3>
          <p><strong>Toll Operator ID:</strong> {calculationResult.tollOpID}</p>
          <p><strong>Tag Operator ID:</strong> {calculationResult.tagOpID}</p>
          <p><strong>Number of Passes:</strong> {calculationResult.nPasses}</p>
          <p><strong>Total Cost (€):</strong> {calculationResult.passesCost}</p>
        </div>
      )}
    </div>
  );
};

export default CostCalculator;
 */