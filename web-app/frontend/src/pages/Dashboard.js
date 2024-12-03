import React from "react";
import EventTypeChart from "../components/Charts/EventTypeChart";
import StateAggregationChart from "../components/Charts/StateAggregationChart";
import SearchEventsChart from "../components/Charts/SearchEventsChart";
import PropertyDamageByEventTypeChart from "../components/Charts/PropertyDamageByEventTypeChart";

const Dashboard = ({ token, onLogout }) => {
  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <button
          onClick={onLogout}
          className="bg-red-500 text-white py-2 px-4 rounded-md hover:bg-red-600"
        >
          Logout
        </button>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <div className="bg-white p-4 shadow-md rounded">
          <EventTypeChart token={token} />
        </div>
        <div className="bg-white p-4 shadow-md rounded">
          <StateAggregationChart token={token} />
        </div>
        {/* <div className="bg-white p-4 shadow-md rounded">
          <SearchEventsChart
            token={token}
            states={["TEXAS", "FLORIDA", "CALIFORNIA"]}
          />
        </div>
        <div className="bg-white p-4 shadow-md rounded">
          <PropertyDamageByEventTypeChart token={token} />
        </div> */}
      </div>
    </div>
  );
};

export default Dashboard;
