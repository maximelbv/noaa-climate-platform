import React, { useState, useEffect } from "react";
import axios from "axios";

const DataTable = ({ token }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          "http://localhost:8000/protected/elasticsearch/mongo_storm_events_data?page=1&size=10",
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        setData(response.data.results);
      } catch (error) {
        console.error("Failed to fetch data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [token]);

  if (loading) return <p>Loading data...</p>;

  return (
    <table>
      <thead>
        <tr>
          <th>State</th>
          <th>Event Type</th>
          <th>Date</th>
        </tr>
      </thead>
      <tbody>
        {data.map((row, index) => (
          <tr key={index}>
            <td>{row.STATE}</td>
            <td>{row.EVENT_TYPE}</td>
            <td>{row.BEGIN_DATE_TIME}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default DataTable;
