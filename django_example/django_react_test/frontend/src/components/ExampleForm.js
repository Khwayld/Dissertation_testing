import React, { useState } from 'react';
import Graph from './Graph';

function ExampleForm() {
  const [lambdaValue, setLambdaValue] = useState(1.0);
  const [alphaValue, setAlphaValue] = useState(1.0);
  const [sourceFile, setSourceFile] = useState(null);  // File state for source data
  const [targetFile, setTargetFile] = useState(null);  // File state for target data
  const [results, setResults] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();

    // Create a FormData object to send files and other form data
    const formData = new FormData();
    formData.append('lambda_value', lambdaValue);
    formData.append('alpha_value', alphaValue);
    formData.append('source_data', sourceFile);  // Append source data file
    formData.append('target_data', targetFile);  // Append target data file

    fetch('http://localhost:8000/api/run-example/', { 
      method: 'POST',
      body: formData,
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
        <label>
          Source Data (CSV):
          <input
            type="file"
            accept=".csv"
            onChange={(e) => setSourceFile(e.target.files[0])}
          />
        </label>
        <br />
        <label>
          Target Data (CSV):
          <input
            type="file"
            accept=".csv"
            onChange={(e) => setTargetFile(e.target.files[0])}
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
