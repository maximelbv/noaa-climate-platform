import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [events, setEvents] = useState([]);
  const [gsodData, setGsodData] = useState([]);

  useEffect(() => {
    // Fetch combined data (events and GSOD)
    axios
      .get("http://localhost:8000/combined-data")
      .then((response) => {
        setEvents(response.data.events);
        setGsodData(response.data.gsod_data);
      })
      .catch((error) => console.error("Error fetching combined data: ", error));
  }, []);

  return (
    <div className="App">
      <h1>NOAA Climate Data</h1>

      <h2>Events (from Elasticsearch)</h2>
      <ul>
        {events.map((event, index) => (
          <li key={index}>
            <strong>{event.STATE}</strong> - {event.EVENT_TYPE} in {event.YEAR}{" "}
            <br />
            Damage: ${event.DAMAGE_PROPERTY}, Injuries: {event.INJURIES_DIRECT}
          </li>
        ))}
      </ul>

      <h2>GSOD Data (from PostgreSQL)</h2>
      <ul>
        {gsodData.map((data, index) => (
          <li key={index}>
            Station: {data.STATION}, Date: {data.DATE}, Temperature: {data.TEMP}
            , Precipitation: {data.PRCP}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
