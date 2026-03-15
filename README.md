# Amazon Product Scraper & Data Pipeline

A Python-based web scraping project that collects product data from Amazon, stores the data in JSON format, and loads it into a PostgreSQL database.  
This project demonstrates a complete **data pipeline using Selenium, JSON, and PostgreSQL with logging and error handling**.

---

## Project Overview

This script automates the process of:

1. Searching multiple product categories on Amazon.
2. Scraping product information such as:
   - Product Category
   - Product Name
   - Price
   - Rating
3. Saving the scraped data into a JSON file.
4. Loading the data into a PostgreSQL database.
5. Logging the entire process for monitoring and debugging.

The project is designed to simulate a **real-world data ingestion pipeline**.

---

## Features

- Automated Amazon product search
- Multi-category scraping
- Data stored in JSON format
- PostgreSQL database integration
- Bulk insert for faster database loading
- Logging system for monitoring and debugging
- Error handling using try-except blocks
- Environment variable support for secure database credentials

---

## Technologies Used

- Python
- Selenium
- PostgreSQL
- Psycopg2
- JSON
- Logging
- Dotenv

---

## Project Structure

```
Amazon_hunter
│
├── main.py            # Main scraping and data pipeline script
├── products.json      # Scraped product data
├── amazon_scraper.log # Log file
├── .env               # Environment variables for database credentials
└── README.md          # Project documentation
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/amazon-product-scraper.git
cd amazon-product-scraper
```

### 2. Install Dependencies
pip install selenium psycopg2 python-dotenv
### 3. Setup PostgreSQL Database

Create a database in PostgreSQL and add your credentials in a .env file.

Example .env file:
```
YOUR_HOST_NAME=localhost
YOUR_USER_NAME=postgres
YOUR_PASSWORD=yourpassword
YOUR_DATABASE=amazon_db
```
### 4. Run the Script
python main.py
Example Output
```
JSON Data
{
  "product_category": "Shampoo",
  "product_name": "Clinic Plus Strong & Long Shampoo",
  "price": 276,
  "rating": 4.3
}
```
Database Table
product_category	product_name	price	rating
Shampoo	XYZ Shampoo	276	4.3
Soap	ABC Soap	45	4.1
Logging

The script generates a log file:

amazon_scraper.log

Example log entries:
```
INFO - Amazon website opened successfully
INFO - Successfully scraped Shampoo
INFO - JSON file saved successfully
INFO - Data inserted successfully
```

## Future Improvements

Implement pagination to scrape more products

Add rotating user agents to avoid scraping blocks

Use Pandas for data cleaning

Implement PostgreSQL COPY for faster bulk inserts

Deploy scraper using Airflow or scheduling tools

### Author

Praveen Suresh
Python Developer | Web Scraping Enthusiast

License

This project is for educational purposes only.
Amazon content belongs to their respective owners.


