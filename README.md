**Visualization Dashboard**


**Project Overview**

This project is a Data Visualization Dashboard that provides insights using interactive graphs and charts. It is built using Django for the backend and JavaScript/Bootstrap for the frontend. The dashboard fetches data from a MySQL database populated from the provided JSON file (jsondata.json) and visualizes key metrics like intensity, likelihood, relevance, year, country, topics, region, and city using D3.js.



**Tech Stack**
Backend: Django
Frontend: JavaScript, Bootstrap
Database: MySQL


**Visualization Library:**
D3.js 



**Features**
✅ Data Processing:
Convert the provided JSON (jsondata.json) into a MySQL database.
Create Django API endpoints to retrieve data from the database.


✅ Interactive Dashboard:
Display key metrics using D3.js visualizations.
Use filters to dynamically update charts.


✅ Filters for Data Exploration:
End Year
Topics
Sector
Region
PEST (Political, Economic, Social, Technological)
Source
SWOT (Strengths, Weaknesses, Opportunities, Threats)
Country & City


✅ Dynamic API Integration:
The dashboard reads data from MySQL via Django REST API.
API supports filtering and fetching relevant data.
