import React, { useState } from 'react';
import Papa from 'papaparse';
import './PassEntryForm.css';

const PassEntryForm = () => {
  const [csvData, setCsvData] = useState([]);
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Διαβάζουμε το CSV
      Papa.parse(file, {
        header: true,
        skipEmptyLines: true,
        complete: (result) => {
          setCsvData(result.data);
          setSuccessMessage('CSV data successfully uploaded and transcribed!');
          uploadCsvToServer(file); // Στέλνουμε το αρχείο στο API
        },
      });
    }
  };

  const uploadCsvToServer = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('https://localhost:9115/api/admin/addpasses', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setSuccessMessage('Data successfully added to the database!');
        setErrorMessage(''); // Καθαρίζουμε τυχόν προηγούμενα μηνύματα σφάλματος
      } else {
        setErrorMessage(`Failed to add data: ${data.info}`);
        setSuccessMessage(''); // Καθαρίζουμε το μήνυμα επιτυχίας αν αποτύχει
      }
    } catch (error) {
      setErrorMessage(`Error: ${error.message}`);
      setSuccessMessage('');
    }
  };

  return (
    <div className="pass-entry-form">
      <h2>Upload CSV File</h2>
      <div className="upload-container">
        <input type="file" id="csvUpload" accept=".csv" onChange={handleFileUpload} />
        <label htmlFor="csvUpload" className="upload-button">Choose File</label>
      </div>

      {successMessage && <p className="success-message">{successMessage}</p>}
      {errorMessage && <p className="error-message">{errorMessage}</p>}
    </div>
  );
};

export default PassEntryForm;

