# WEATHER STATION WEB APPLICATION

Welcome to the **Weather Station Web Application**, an innovative project designed to help hikers, mountaineers, and outdoor enthusiasts stay informed about weather conditions in real time. This project features a weather station that collects data from various sensors, processes it via a Flask-based API, and presents the information through a web application running in Docker with Docker Compose orchestration.

## PROJECT OVERVIEW

The Weather Station Web Application provides **real-time weather data** from a network of sensors, making it easier for outdoor enthusiasts to get accurate weather information on-the-go.

### KEY COMPONENTS:
- **Raspberry Pi 4**: Serves as the central hub for collecting data from sensors.
- **Sensors**: Three sensors connected to the Raspberry Pi monitor:
  - Temperature Sensor
  - Humidity Sensor
  - Wind Sensor
- **Flask API**: The backend that processes data, handles authentication, and offers additional features like a chat system.
- **MongoDB**: The database where all sensor data is stored for historical reference and analysis.
- **Docker & Docker Compose**: Used for containerization and orchestration of the web application and its dependencies.
- **Web Application**: A user-friendly interface that allows users to access weather data and interact with the system.

### FUTURE FEATURES:
- **AI Weather Prediction**: Integration of machine learning models to predict weather conditions based on sensor data, offering a forecast for the upcoming days.
- **Weather Station Chat System**: A real-time chat feature that enables communication between weather stations across the country, allowing users to request weather data specific to their region.

## WHY IT WAS BUILT

This project was designed with **outdoor adventurers** in mind, specifically targeting hikers, mountaineers, and other enthusiasts who need quick and reliable access to weather information. Whether you’re planning a hike, a mountain climb, or just an outdoor excursion, this application provides an efficient and user-friendly way to get **real-time weather data** from your location and others.

Additionally, this project was created as part of my **learning journey**. It is one of my first larger-scale projects that involves both backend and frontend development, and it has been an excellent opportunity for me to improve my **full-stack development skills**.

## TECHNICAL STACK

- **Flask**: A lightweight web framework for building the API.
- **MongoDB**: A NoSQL database for storing weather data from sensors.
- **Docker & Docker Compose**: Used for containerizing the entire application stack, making it easy to deploy and manage dependencies.
- **Socket.IO**: For real-time communication, particularly useful for the chat system between weather stations.
- **Werkzeug**: A utility library used for password hashing and security.
- **Python**: The programming language used for backend development.

## HOW IT WORKS

1. **Data Collection**: The sensors connected to the Raspberry Pi 4 collect data on temperature, humidity, and wind speed.
2. **Data Transmission**: The collected data is sent to a Flask API, which processes and stores the data in MongoDB.
3. **Real-Time Communication**: Through the web application, users can query the latest weather data, access historical records, and even chat with other weather stations.
4. **AI Prediction (Future)**: The system will eventually use the sensor data to train AI models for weather forecasting, providing users with predictions for the upcoming days.

## FRONTEND STATUS

Please note that the **frontend of this project is still under development**. Currently, the user interface is a **work in progress**, and while the backend functionality is fully operational, the frontend may not yet be polished or fully user-friendly. I am actively working on improving the design and user experience, and I appreciate your patience as I continue to enhance this feature.

## FUTURE ENHANCEMENTS

- **AI-based Weather Predictions**: I plan to implement a machine learning model to predict weather conditions for the coming days based on real-time sensor data.
- **Nationwide Weather Station Network**: Building a chat system that connects weather stations nationwide, allowing users to exchange weather data and provide real-time updates for specific regions.

## HOW IT HELPS THE COMMUNITY

This weather station system is built to assist **outdoor enthusiasts**, especially hikers and mountaineers, by providing them with **real-time weather data**, which is crucial for planning safe and successful expeditions. By centralizing weather data in an easy-to-use web interface, we aim to create a more connected and informed community of outdoor adventurers.

## CONTRIBUTING

Feel free to contribute to the project! If you have any improvements, bug fixes, or new feature ideas, please submit a pull request. Any help is greatly appreciated!
