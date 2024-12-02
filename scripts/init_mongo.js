db = db.getSiblingDB("my_database");

db.createUser({
  user: "my_user",
  pwd: "my_password",
  roles: [{ role: "readWrite", db: "my_database" }],
});

db.createCollection("storm_events");
db.createCollection("climate_text_reports");

db.storm_events.createIndex({ event_id: 1 });
db.climate_text_reports.createIndex({ report_id: 1 });
