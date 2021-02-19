CREATE DATABASE IF NOT EXISTS lab4ece140a;

USE lab4ece140a;

CREATE TABLE IF NOT EXISTS Commands (
  id         int AUTO_INCREMENT PRIMARY KEY,
  message    VARCHAR(32) NOT NULL,
  completed  boolean DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);