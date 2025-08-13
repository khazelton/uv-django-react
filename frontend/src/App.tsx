import { useEffect, useState } from "react";
import { apiUrl } from "./config";
import "./App.css";

function App() {
  const [message, setMessage] = useState<string>("loading...");
  useEffect(() => {
    fetch(apiUrl("/api/ping/"))
      .then((r) => r.json())
      .then((data) => setMessage(data.message))
      .catch(() => setMessage("backend unreachable"));
  }, []);
  return (
    <>
      <h1>uv + Django + React</h1>
      <p>API says: {message}</p>
    </>
  );
}
export default App;
