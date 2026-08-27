# Information System for Improving Business Processes in Sales

## About the Project

This project is an information system designed to automate and optimize business processes in the sales sector.

The system was developed as part of a graduation project in the field of **Applied Informatics in Economics**.

The main goal of the project is to automate managers' work with customers, products, sales, and documents, reduce the number of manual operations, and improve information processing efficiency.

## System Features

* customer management;
* product management;
* sales processing;
* document generation;
* database information storage;
* data search and filtering;
* report generation;
* centralized data management;
* user-friendly graphical interface.

## Technology Stack

### Backend / Application

* **Python 3.9+**
* **PyQt6**
* **SQLAlchemy**

### Database

* **MySQL**

### Architecture

The system uses a three-tier architecture:

* **Presentation Layer** — user interface;
* **Business Logic Layer** — application business logic;
* **Data Access Layer** — interaction with the database.

## Project Structure

```text
project/
│
├── database/              # Database operations
├── models/                # Data models
├── repositories/          # Data access layer
├── services/              # Business logic
├── ui/                    # User interface
├── utils/                 # Utility functions
├── config/                # Application configuration
├── main.py                # Application entry point
├── requirements.txt       # Project dependencies
└── README.md              # Documentation
```

> The project structure may vary depending on the current version of the application.

## Requirements

To run the project, you need to install:

* Python 3.9 or higher;
* MySQL;
* Git.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Vafobekov04/myproproject.git
cd myproproject
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Database

Create a MySQL database and configure the connection parameters in the project configuration file.

If using `.env`:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=sales_system
DB_USER=root
DB_PASSWORD=your_password
```

> Do not publish real passwords or other sensitive information on GitHub.

### 5. Run the Application

```bash
python main.py
```

## Main Modules

### 👥 Customers

Allows users to store and edit customer information required for managers' daily operations.

### 📦 Products

Provides functionality for adding, editing, deleting, and searching for products.

### 💰 Sales

Allows users to process sales and store information about completed transactions.

### 📄 Documents

The system can generate the required documents based on sales data.

### 📊 Reports

Provides tools for analyzing information and generating reports.

### 🔎 Search and Filtering

Allows users to quickly find the required records and work efficiently with large amounts of information.

## Automation Results

The following results were obtained during the research and development of the system:

* reduction in labor costs after automation — **87.80%**;
* reduction in overall costs — **88.56%**;
* estimated payback period — approximately **2 months**;
* estimated annual economic effect — **437,079.28 RUB**.

## Project Purpose

The system is intended for managers who work with customers, products, sales, and related documentation.

The project can also serve as a foundation for further development of the information system and implementation of additional automation features.

## Future Development

Possible directions for further development include:

* development of a web version;
* implementation of user authentication;
* role-based access control;
* expansion of analytics and reporting;
* integration with external services;
* development of a REST API;
* transition to a server-based architecture;
* development of a mobile client.

## Author

**Vafobek Vafobekov**

Field of Study: **09.03.03 — Applied Informatics**

The project was developed as part of a **graduation thesis**.
