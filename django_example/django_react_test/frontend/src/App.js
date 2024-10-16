import React, { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/kale/")
      .then((response) => response.json())
      .then((data) => setData(data.accuracy));
  }, []);

  return (
    <div className="App">
      <h1>PyKale Model Accuracy: {data ? data : "Loading..."}</h1>
    </div>
  );
}

export default App;
