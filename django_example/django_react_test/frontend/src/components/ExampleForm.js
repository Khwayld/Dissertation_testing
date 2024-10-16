// src/components/ExampleForm.js
import React, { useState } from 'react';
import Graph from './Graph';

function ExampleForm() {
  const [nSamples, setNSamples] = useState(200);
  const [lambdaValue, setLambdaValue] = useState(1.0);
  const [alphaValue, setAlphaValue] = useState(1.0);
  const [results, setResults] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();

    const formData = {
      n_samples: nSamples,
      lambda_value: lambdaValue,
      alpha_value: alphaValue,
    };

    fetch('http://localhost:8000/api/run-example/', { 
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((data) => {
        setResults(data);
      })
      .catch((error) => console.error('Error:', error));
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          Number of Samples:
          <input
            type="number"
            value={nSamples}
            onChange={(e) => setNSamples(e.target.value)}
          />
        </label>
        <br />
        <label>
          Lambda Value:
          <input
            type="number"
            value={lambdaValue}
            onChange={(e) => setLambdaValue(e.target.value)}
          />
        </label>
        <br />
        <label>
          Alpha Value:
          <input
            type="number"
            value={alphaValue}
            onChange={(e) => setAlphaValue(e.target.value)}
          />
        </label>
        <br />
        <button type="submit">Run Example</button>
      </form>

      {results && (
        <div>
          <h3>Results</h3>
          <p>Accuracy Before Adaptation: {results.accuracy_before}</p>
          <p>Accuracy After Adaptation: {results.accuracy_after}</p>

          <Graph graphData={results.graph_data} />
        </div>
      )}
    </div>
  );
}

export default ExampleForm;
