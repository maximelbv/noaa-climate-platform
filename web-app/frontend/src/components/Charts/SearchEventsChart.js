import React, { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

const MultiStateEventsChart = ({
  token,
  states = ["TEXAS", "FLORIDA", "CALIFORNIA"],
}) => {
  const [chartData, setChartData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/protected/elasticsearch/mongo_storm_events_data/filter/state?states=${states.join(
            ","
          )}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        if (!response.ok) {
          throw new Error("Failed to fetch data");
        }
        const data = await response.json();

        const labels = states;
        const values = labels.map(
          (state) =>
            data.results.filter((event) => event.STATE === state).length
        );

        setChartData({
          labels,
          datasets: [
            {
              label: "Event Count by State",
              data: values,
              backgroundColor: "rgba(75, 192, 192, 0.2)",
              borderColor: "rgba(75, 192, 192, 1)",
              borderWidth: 1,
            },
          ],
        });
      } catch (err) {
        console.error("Error fetching state filter data:", err);
        setError("Failed to load chart data.");
      }
    };

    fetchData();
  }, [token, states]);

  if (error) return <p className="text-red-500">{error}</p>;
  if (!chartData) return <p>Loading chart...</p>;

  return (
    <div>
      <h3 className="text-lg font-semibold mb-2">Event Count by State</h3>
      <p className="text-sm text-gray-500 mb-4">
        This bar chart visualizes the total number of weather events for each
        selected state, allowing a quick comparison of event frequency across
        regions.
      </p>
      <Bar data={chartData} />
    </div>
  );
};

export default MultiStateEventsChart;
