# Application_Monitoring
# Running  the Project
  ### Start all the containers
  sudo docker-compose up --build
  ### Start workload script separately:
  python workload/simulate.py
  ### Setup Grafana: http://localhost:3000/ (Login: admin / admin)
  #### Connect to mysql data source with following credentials
     Host: db:3306
     User: root
     Password: rootpass
     Database: logs
  ### Create Grafana dashboards with respective queries
   #### Request Count Per Endpoint:
    SELECT endpoint, COUNT(*) as count FROM logs GROUP BY endpoint;
   #### Response Time Trend:
    SELECT timestamp as time, AVG(response_time) as avg_response FROM logs GROUP BY time ORDER BY time
   #### Most Frequent Errors:
    SELECT error_message, COUNT(*) FROM logs WHERE error_message IS NOT NULL GROUP BY error_message
   #### Live Logs:
    SELECT timestamp, endpoint, status_code, error_message FROM logs ORDER BY timestamp DESC LIMIT 100
