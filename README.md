# Senior Design Software Mini Project

Web application that plots temperature and humidity data for users. Each user may have multiple sources that log data into a database. User authentication completed using Google authentication. 

## Authentication

Google authentication

## Database and Table Design

The database is implemented with SQlite3. 

The database contains a table called 'temprh'.
The table consists of the following query keys:
* userid = Unique ID for the user
* source = Source number
* label = Name of the source, determined by the user
* time = Time for which the temperature and humidity is associated with
* temp = Temperature for specified time
* humdity = Humidity for specified time

This table format allows for logging the temperature and humidity over a 24 hour time period for the user's source. Each entry in the table represents the temperature and humidity for a single hour.

All SQLite queries are parameterized queries, which sanitizes all input.  

## WebApp Design

### frontend
#### css
#### html
#### images
#### javascript

### server_code
#### add_sources
#### display_results
#### list_sources
#### login

### database
Database python file.

### tmp_files
Stores generated plots. All files are deleted upon user logout. 

## Testing and Verification

## Running the Application

### Prerequisites

* Sqlite3

### Run via CMD

```
python -m web_server
```

## Authors

* **June Hua** 
* **Trishita Tiwari**
