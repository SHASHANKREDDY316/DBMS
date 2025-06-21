CREATE DATABASE IF NOT EXISTS showroom;
USE showroom;

CREATE TABLE cars (
    CarID INT AUTO_INCREMENT PRIMARY KEY,
    Model VARCHAR(100) NOT NULL,
    Year INT NOT NULL,
    Price DECIMAL(10,2) NOT NULL,
    Color VARCHAR(50) NOT NULL,
    Stock INT NOT NULL
);

CREATE TABLE customers (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    Phone VARCHAR(30),
    Address VARCHAR(200)
);

CREATE TABLE employees (
    EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Role VARCHAR(100) NOT NULL,
    Email VARCHAR(100),
    Phone VARCHAR(30)
);

CREATE TABLE services (
    ServiceID INT AUTO_INCREMENT PRIMARY KEY,
    CarID INT NOT NULL,
    CustomerID INT NOT NULL,
    ServiceDate DATE NOT NULL,
    Description VARCHAR(255) NOT NULL,
    Cost DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (CarID) REFERENCES cars(CarID) ON DELETE CASCADE,
    FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID) ON DELETE CASCADE
);

CREATE TABLE payments (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    Date DATE NOT NULL,
    Method VARCHAR(50) NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID) ON DELETE CASCADE
);
-- SALES table (with auto-increment SaleID)
CREATE TABLE sales (
    SaleID INT AUTO_INCREMENT PRIMARY KEY,
    CarID INT,
    CustomerID INT,
    DrivingLicense VARCHAR(100),
    Amount DECIMAL(12,2),
    Price DECIMAL(12,2),
    Date DATE,
    Method VARCHAR(50),
    PaymentType VARCHAR(50),
    FOREIGN KEY (CarID) REFERENCES cars(CarID),
    FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID)
);

-- (Example for cars/customers, etc, include your existing tables as needed)
CREATE TABLE cars (
    CarID INT AUTO_INCREMENT PRIMARY KEY,
    Model VARCHAR(100),
    Year INT,
    Price DECIMAL(12,2),
    Color VARCHAR(50),
    Stock INT
);

CREATE TABLE customers (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100),
    Phone VARCHAR(20),
    Address VARCHAR(255)
);

-- other tables as previously given...