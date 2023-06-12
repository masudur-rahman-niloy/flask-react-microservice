import React, { useState } from 'react';

const App = () => {
  const host = "http://127.0.0.1:5001";
  // const host = process.env.BACKEND_BASE_URL;
  const [inputValue, setInputValue] = useState('');
  const [responseData, setResponseData] = useState('');

  const [inputGetValue, setInputGetValue] = useState('');
  const [responseGetData, setResponseGetData] = useState('');

  const handleChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleGetChange = (event) => {
    setInputGetValue(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Make an API call here using the inputValue
    // For simplicity, let's assume the API endpoint returns a JSON object with a "data" property
    const requestBody = { name: inputValue };

    // Make the API call
    fetch(host + '/save_data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    })
      .then((response) => response.json())
      .then((data) => {
        setResponseData(JSON.stringify(data));
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  const handleSubmitToGet = (event) => {
    event.preventDefault();
    // Make an API call here using the inputValue
    // For simplicity, let's assume the API endpoint returns a JSON object with a "data" property
    const requestBody = { user_id: inputGetValue };

    // Make the API call
    fetch(host + '/get_data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    })
      .then((response) => response.json())
      .then((data) => {
        
        setResponseGetData(JSON.stringify(data));
      })

      .catch((error) => {
        console.error('Error:', error);
      });
  };

  return (
    <div>
      <div>
        <form onSubmit={handleSubmit}>
          <input type="text" value={inputValue} onChange={handleChange} />
          <button type="submit">Save</button>
        </form>
        {responseData && <p>Response: {responseData}</p>}
      </div>
      <br />
      <div>
        <form onSubmit={handleSubmitToGet}>
          <input type="text" value={inputGetValue} onChange={handleGetChange} />
          <button type="submit">Get</button>
        </form>
        {responseGetData && <p>Response: {responseGetData}</p>}
      </div>
    </div>
  );
};

export default App;
