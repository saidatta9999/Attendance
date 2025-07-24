-- Create database (optional, if not already created)
CREATE DATABASE IF NOT EXISTS facetrack;
USE facetrack;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(100),
  user_id VARCHAR(50) UNIQUE,
  department VARCHAR(100),
  PRIMARY KEY (id)
);

-- Attendance Table
CREATE TABLE IF NOT EXISTS attendance (
  id INT NOT NULL AUTO_INCREMENT,
  user_id VARCHAR(50),
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);
