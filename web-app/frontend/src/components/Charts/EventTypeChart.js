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

const EventTypeChart = ({ token }) => {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          "http://localhost:8000/protected/elasticsearch/mongo_storm_events_data/aggregate/event_type",
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        const data = await response.json();

        const labels = data.aggregations.map((bucket) => bucket.key);
        const values = data.aggregations.map((bucket) => bucket.doc_count);

        setChartData({
          labels,
          datasets: [
            {
              label: "Event Count by Type",
              data: values,
              backgroundColor: "rgba(75, 192, 192, 0.2)",
              borderColor: "rgba(75, 192, 192, 1)",
              borderWidth: 1,
            },
          ],
        });
      } catch (error) {
        console.error("Error fetching event type data:", error);
      }
    };

    fetchData();
  }, [token]);

  if (!chartData) return <p>Loading chart...</p>;

  return (
    <div>
      <h3 className="text-lg font-semibold mb-2">Event Types Distribution</h3>
      <p className="text-sm text-gray-500 mb-4">
        This chart shows the distribution of different weather event types and
        their frequency.
      </p>
      <Bar data={chartData} />
    </div>
  );
};

export default EventTypeChart;
