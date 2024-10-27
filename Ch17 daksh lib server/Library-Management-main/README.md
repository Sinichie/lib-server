# Library Management System (LMS)

## Overview
The **Library Management System (LMS)** is a web-based application developed using Flask to manage the library's books, students, and book issuance operations. The system allows admins to manage books and students while students can browse available books and view their issued books.

## Features
- **Admin Authentication**: Secure login for admins to access the system.
- **Manage Books**: Add, update, and delete books from the library.
- **Manage Students**: Add and manage student details.
- **Issue Books**: Issue books to students and track issue/return dates.
- **View Books**: Browse and search available books in the library.
- **View Issued Books**: View a list of books issued to students, along with the return dates.

## Technologies Used
- **Flask**: Backend web framework
- **SQLite**: Database management system
- **HTML/CSS**: Frontend interface
- **Jinja2**: Templating engine for dynamic HTML rendering

## Database Structure

### Admin Table
| Field Name | Type         | Description                  |
|------------|--------------|------------------------------|
| Username   | VARCHAR(40)   | User Name                   |
| Password   | VARCHAR(200)  | Password                    |


### Books Table
| Field Name | Type         | Description                  |
|------------|--------------|------------------------------|
| ID         | INT          | Auto-incrementing book ID     |
| NAME       | VARCHAR(40)  | Name of the book              |
| AUTHOR     | VARCHAR(40)  | Author of the book            |
| QUANTITY   | MEDIUMINT    | Number of copies available    |

### Students Table
| Field Name | Type         | Description                  |
|------------|--------------|------------------------------|
| ROLL_NUM   | VARCHAR(15)  | Student's roll number (PK)    |
| NAME       | VARCHAR(40)  | Name of the student           |

### Books_Issued Table
| Field Name | Type         | Description                  |
|------------|--------------|------------------------------|
| S_NO       | INT          | Serial number (PK)            |
| ID         | INT          | Book ID (FK from Books)       |
| ROLL_NUM   | VARCHAR(15)  | Student's roll number (FK)    |
| ISSUE_DATE | DATE         | Date the book was issued      |

## How to Run
1. Clone the repository:
    ```bash
    git clone https://github.com/Aka5h-14/Library-Management.git
    cd Library-Management
    ```

2. Create a virtual environment and install dependencies:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    ```

3. Run the application:
    ```bash
    flask run
    ```

4. Access the application at `http://127.0.0.1:5000`.




## DFD 0
      
      +----------------------------------+
      |            Admin                 |
      |                                  |
      |  - Manage Books                  |  
      |  - Manage Students               |
      +----------------------------------+
                |
                |               +-------------------------+
                |               |   Library Management     |
                +-------------->|        System (LMS)      |<------------------+
                                |                          |                   |
                                +--------------------------+                   |
                                                ^                               |
                                                |                               |
                                      +---------+---------+          +-----------------------+
                                      |      Books        |          |       Students         |
                                      +-------------------+          |                       |
                                                                      +-----------------------+

## DFD 1
      +----------------------------------+
      |          Admin Login             |
      |                                  |
      |  - Input: Username, Password     |
      |  - Output: Login success/failure |
      +----------------------------------+
                    |
                    v
      +----------------------------------+
      |         Manage Books             |
      |                                  |
      |  - Add, Update, Delete Books     |
      +----------------------------------+
                    |
                    v
      +----------------------------------+            +-------------------------+
      |       Manage Students            |------------|    Issue Books          |
      |                                  |            |                         |
      +----------------------------------+            +-------------------------+
                    |
                    v
      +----------------------------------+
      |        View Issued Books         |
      +----------------------------------+
                    |
                    v
      +----------------------------------+
      |          View Books              |
      +----------------------------------+
                    |
                    v
      +----------------------------------+
      |        Library Database          |
      +----------------------------------+
