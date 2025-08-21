import React, { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://18.232.65.45:8000/assignments/") // change to your Django API endpoint
      .then((res) => res.json())
      .then((data) => setData(data))
      .catch((err) => console.error("Error:", err));
  }, []);

  return (
    <div>
      <h1>Test Django API</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}

export default App;
