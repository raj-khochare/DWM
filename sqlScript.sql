CREATE TABLE Product_Dimension ( 
    Product_id NUMBER PRIMARY KEY, 
    Product_Name VARCHAR2(50), 
    Product_Category VARCHAR2(50), 
    Price NUMBER 
);

CREATE TABLE Emp_Dimension ( 
    Emp_id NUMBER PRIMARY KEY, 
    Emp_Name VARCHAR2(50), 
    Title VARCHAR2(50), 
    Department VARCHAR2(50), 
    Region VARCHAR2(50) 
);

CREATE TABLE Customer_Dimension ( 
    Customer_id NUMBER PRIMARY KEY, 
    Customer_Name VARCHAR2(50), 
    Address VARCHAR2(100), 
    City VARCHAR2(50) 
);

CREATE TABLE Time_Dimension ( 
    Order_id NUMBER PRIMARY KEY, 
    Order_Date DATE, 
    Year NUMBER, 
    Month VARCHAR2(15) 
);

CREATE TABLE Sales ( 
    Product_id NUMBER REFERENCES Product_Dimension(Product_id), 
    Customer_id NUMBER REFERENCES Customer_Dimension(Customer_id), 
    Order_id NUMBER REFERENCES Time_Dimension(Order_id), 
    Emp_id NUMBER REFERENCES Emp_Dimension(Emp_id), 
    Total NUMBER, 
    Quantity NUMBER, 
    Discount NUMBER 
);

INSERT INTO Product_Dimension VALUES (101, 'Laptop', 'Electronics', 75000);
INSERT INTO Product_Dimension VALUES (102, 'Smartphone', 'Electronics', 35000);
INSERT INTO Product_Dimension VALUES (103, 'Washing Machine', 'Home Appliance', 25000);
INSERT INTO Product_Dimension VALUES (104, 'Refrigerator', 'Home Appliance', 40000);
INSERT INTO Product_Dimension VALUES (105, 'Office Chair', 'Furniture', 8000);

INSERT INTO Emp_Dimension VALUES (201, 'Amit Sharma', 'Sales Executive', 'Sales', 'North');
INSERT INTO Emp_Dimension VALUES (202, 'Priya Patel', 'Sales Manager', 'Sales', 'West');
INSERT INTO Emp_Dimension VALUES (203, 'Rahul Mehta', 'Sales Executive', 'Sales', 'South');
INSERT INTO Emp_Dimension VALUES (204, 'Sneha Rao', 'Account Manager', 'Accounts', 'East');
INSERT INTO Emp_Dimension VALUES (205, 'Vikram Singh', 'Sales Executive', 'Sales', 'Central');

INSERT INTO Customer_Dimension VALUES (301, 'Ravi Kumar', '12 MG Road', 'Delhi');
INSERT INTO Customer_Dimension VALUES (302, 'Neha Verma', '23 FC Road', 'Pune');
INSERT INTO Customer_Dimension VALUES (303, 'Arjun Nair', '45 MG Layout', 'Bangalore');
INSERT INTO Customer_Dimension VALUES (304, 'Anjali Desai', '89 Ring Road', 'Mumbai');
INSERT INTO Customer_Dimension VALUES (305, 'Kiran Yadav', '67 Lake View', 'Lucknow');

INSERT INTO Time_Dimension VALUES (401, TO_DATE('2024-01-15', 'YYYY-MM-DD'), 2024, 'January');
INSERT INTO Time_Dimension VALUES (402, TO_DATE('2024-03-10', 'YYYY-MM-DD'), 2024, 'March');
INSERT INTO Time_Dimension VALUES (403, TO_DATE('2024-06-05', 'YYYY-MM-DD'), 2024, 'June');
INSERT INTO Time_Dimension VALUES (404, TO_DATE('2024-09-20', 'YYYY-MM-DD'), 2024, 'September');
INSERT INTO Time_Dimension VALUES (405, TO_DATE('2024-12-11', 'YYYY-MM-DD'), 2024, 'December');

-- Product_id | Customer_id | Order_id | Emp_id | Total | Quantity | Discount

INSERT INTO Sales VALUES (101, 301, 401, 201, 150000, 2, 5000);
INSERT INTO Sales VALUES (102, 302, 402, 202, 70000, 2, 2000);
INSERT INTO Sales VALUES (103, 303, 403, 203, 25000, 1, 1000);
INSERT INTO Sales VALUES (104, 304, 404, 204, 80000, 2, 3000);
INSERT INTO Sales VALUES (105, 305, 405, 205, 16000, 2, 500);
INSERT INTO Sales VALUES (101, 302, 401, 202, 75000, 1, 0);
INSERT INTO Sales VALUES (102, 303, 403, 203, 105000, 3, 2500);
INSERT INTO Sales VALUES (104, 301, 402, 201, 40000, 1, 1500);
INSERT INTO Sales VALUES (105, 304, 405, 205, 24000, 3, 800);
INSERT INTO Sales VALUES (103, 305, 404, 203, 50000, 2, 1200);

select * from Product_Dimension;

select * from Emp_Dimension;

select * from Customer_Dimension;

select * from Time_Dimension;

select * from Sales;




--Roll-up the sales data to see the total sales by month
SELECT
    t.Year,
    t.Month,
    SUM(s.Total) AS Total_Sales
FROM
    Sales s
    JOIN Time_Dimension t ON s.Order_id = t.Order_id
GROUP BY
    t.Year, t.Month
ORDER BY
    t.Year, t.Month;

--Drill down the sales data to see the total sales by day
SELECT
    t.Order_Date,
    SUM(s.Total) AS Total_Sales
FROM
    Sales s
    JOIN Time_Dimension t ON s.Order_id = t.Order_id
GROUP BY
    t.Order_Date
ORDER BY
    t.Order_Date;

--Slice the data to see the total sales for a specific product category (e.g.,'Electronics')
SELECT
    p.Product_Category,
    SUM(s.Total) AS Total_Sales
FROM
    Sales s
    JOIN Product_Dimension p ON s.Product_id = p.Product_id
WHERE
    p.Product_Category = 'Electronics'
GROUP BY
    p.Product_Category;

--Dice the data to see the sales for multiple specific criteria
SELECT
    p.Product_Category,
    SUM(s.Total) AS Total_Sales
FROM
    Sales s
    JOIN Product_Dimension p ON s.Product_id = p.Product_id
WHERE
    p.Product_Category IN ('Electronics', 'Home Appliance')
GROUP BY
    p.Product_Category;

--Pivot the data to show the total sales per product category across differentregions
SELECT
    p.Product_Category,
    SUM(CASE WHEN e.Region = 'North' THEN s.Total ELSE 0 END) AS North_Sales,
    SUM(CASE WHEN e.Region = 'South' THEN s.Total ELSE 0 END) AS South_Sales,
    SUM(CASE WHEN e.Region = 'East' THEN s.Total ELSE 0 END) AS East_Sales,
    SUM(CASE WHEN e.Region = 'West' THEN s.Total ELSE 0 END) AS West_Sales,
    SUM(CASE WHEN e.Region = 'Central' THEN s.Total ELSE 0 END) AS Central_Sales
FROM
    Sales s
    JOIN Product_Dimension p ON s.Product_id = p.Product_id
    JOIN Emp_Dimension e ON s.Emp_id = e.Emp_id
GROUP BY
    p.Product_Category;
