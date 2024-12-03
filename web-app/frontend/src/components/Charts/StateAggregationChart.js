import React, { useEffect, useState } from "react";
import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, ArcElement, Tooltip, Legend);

const StateAggregationChart = ({ token }) => {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          "http://localhost:8000/protected/elasticsearch/mongo_storm_events_data/aggregate/state",
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
              label: "Event Count by State",
              data: values,
              backgroundColor: labels.map(
                (_, index) => `hsl(${(index / labels.length) * 360}, 70%, 50%)`
              ),
            },
          ],
        });
      } catch (error) {
        console.error("Error fetching state aggregation data:", error);
      }
    };

    fetchData();
  }, [token]);

  if (!chartData) return <p>Loading chart...</p>;

  return (
    <div>
      <h3 className="text-lg font-semibold mb-2">
        Events aggregation by States
      </h3>
      <p className="text-sm text-gray-500 mb-4">
        This chart shows the count of event by States.
      </p>
      <Pie data={chartData} />
    </div>
  );
};

export default StateAggregationChart;
