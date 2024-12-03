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

const PropertyDamageByEventTypeChart = ({ token }) => {
  const [chartData, setChartData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          "http://localhost:8000/protected/elasticsearch/mongo_storm_events_data/aggregate/event_type",
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        if (!response.ok) {
          throw new Error("Failed to fetch data");
        }
        const data = await response.json();

        // Prepare data for the chart
        const labels = data.aggregations.map((bucket) => bucket.key);
        const values = data.aggregations.map(
          (bucket) => bucket.sum_damage_property.value || 0 // Fallback to 0 if no damage data
        );

        setChartData({
          labels,
          datasets: [
            {
              label: "Property Damage by Event Type (in $)",
              data: values,
              backgroundColor: "rgba(255, 99, 132, 0.2)",
              borderColor: "rgba(255, 99, 132, 1)",
              borderWidth: 1,
            },
          ],
        });
      } catch (err) {
        console.error("Error fetching aggregation data:", err);
        setError("Failed to load chart data.");
      }
    };

    fetchData();
  }, [token]);

  if (error) return <p className="text-red-500">{error}</p>;
  if (!chartData) return <p>Loading chart...</p>;

  return (
    <div>
      <h3 className="text-lg font-semibold mb-2">
        Property Damage by Event Type
      </h3>
      <p className="text-sm text-gray-500 mb-4">
        This chart displays the total property damage (in dollars) caused by
        each type of weather event.
      </p>
      <Bar data={chartData} />
    </div>
  );
};

export default PropertyDamageByEventTypeChart;
