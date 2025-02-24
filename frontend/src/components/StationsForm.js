import React, { useState } from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const stationsList = [...Array.from({ length: 30 }, (_, i) => `AM${String(i + 1).padStart(2, '0')}`),
  ...Array.from({ length: 74 }, (_, i) => `EG${String(i + 1).padStart(2, '0')}`),
  ...Array.from({ length: 2 }, (_, i) => `GE${String(i + 1).padStart(2, '0')}`),
  ...Array.from({ length: 26 }, (_, i) => `KO${String(i + 1).padStart(2, '0')}`),
  ...Array.from({ length: 18 }, (_, i) => `MO${String(i + 1).padStart(2, '0')}`),
  ...Array.from({ length: 41 }, (_, i) => `NAO${String(i + 1).padStart(2, '0')}`),
  ...Array.from({ length: 34 }, (_, i) => `NO${String(i + 1).padStart(2, '0')}`),
  ...Array.from({ length: 28 }, (_, i) => `OO${String(i + 1).padStart(2, '0')}`)
];

const StationsForm = () => {
  const [selectedStations, setSelectedStations] = useState([]);
  const [chartType, setChartType] = useState('totalPasses');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [colors, setColors] = useState({});

  const handleAddStation = (station) => {
    if (station && !selectedStations.includes(station)) {
      const newColor = `#${Math.floor(Math.random() * 16777215).toString(16)}`;
      setColors(prevColors => ({ ...prevColors, [station]: newColor }));
      setSelectedStations([...selectedStations, station]);
    }
  };

  const handleRemoveStation = (station) => {
    setSelectedStations(selectedStations.filter(s => s !== station));
    setColors(prevColors => {
      const newColors = { ...prevColors };
      delete newColors[station];
      return newColors;
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (selectedStations.length === 0 || !dateFrom || !dateTo) {
      alert('Please select at least one station and a date range.');
      return;
    }

    setLoading(true);
    try {
      const datasets = [{
        label: chartType === 'totalPasses' ? 'Total Passes' : 'Total Revenue (€)',
        data: [],
        backgroundColor: selectedStations.map(station => colors[station]),
        borderColor: '#000',
        borderWidth: 1,
        barPercentage: 0.6,
        categoryPercentage: 0.8,
      }];
      
      for (const station of selectedStations) {
        const response = await fetch(
          `https://localhost:9115/api/tollStationPasses/${station}/${dateFrom}/${dateTo}`
        );
        const data = await response.json();
        datasets[0].data.push(chartType === 'totalPasses' ? data.nPasses : data.passList.reduce((sum, pass) => sum + pass.passCharge, 0));
      }
      
      setChartData({ labels: selectedStations, datasets });
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="stations-form">
      <h2>Select Multiple Stations and Chart Type</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="station">Select Station:</label>
        <select id="station" onChange={(e) => handleAddStation(e.target.value)}>
          <option value="">Select Station</option>
          {stationsList.map((station) => (
            <option key={station} value={station}>{station}</option>
          ))}
        </select>
        <div>
          <h4>Selected Stations:</h4>
          <ul>
            {selectedStations.map(station => (
              <li key={station} style={{ color: colors[station] }}>{station} <button type="button" onClick={() => handleRemoveStation(station)}>Remove</button></li>
            ))}
          </ul>
        </div>
        <div>
          <label>Select Chart Type:</label>
          <label>
            <input type="radio" name="chartType" value="totalPasses" checked={chartType === 'totalPasses'} onChange={() => setChartType('totalPasses')} />
            Total Passes
          </label>
          <label>
            <input type="radio" name="chartType" value="totalRevenue" checked={chartType === 'totalRevenue'} onChange={() => setChartType('totalRevenue')} />
            Total Revenue (€)
          </label>
        </div>
        <div>
          <label htmlFor="dateFrom">Start Date:</label>
          <input type="date" id="dateFrom" value={dateFrom} onChange={(e) => setDateFrom(e.target.value)} required />
          <label htmlFor="dateTo">End Date:</label>
          <input type="date" id="dateTo" value={dateTo} onChange={(e) => setDateTo(e.target.value)} required />
        </div>
        <button type="submit" disabled={loading}>{loading ? 'Loading...' : 'Generate Chart'}</button>
      </form>
      {chartData && (
        <div style={{ width: '80%', margin: '20px auto' }}>
          <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '10px' }}>
            {selectedStations.map(station => (
              <div key={station} style={{ marginRight: '15px', display: 'flex', alignItems: 'center' }}>
                <div style={{ width: '15px', height: '15px', backgroundColor: colors[station], marginRight: '5px' }}></div>
                <span>{station}</span>
              </div>
            ))}
          </div>
          <Bar 
            data={chartData}
            options={{
              responsive: true,
              plugins: {
                legend: { display: false },
                title: { display: true, text: 'Toll Station Data' }
              },
              scales: {
                x: { grid: { display: false } },
                y: { beginAtZero: true }
              }
            }}
          />
        </div>
      )}
    </div>
  );
};

export default StationsForm;


