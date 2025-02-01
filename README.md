# Cantilever Backend Assignment
 
This project consists of two main components:
1. **NestJS Server** - The backend server for handling API requests.
2. **Python Scraper** - A web scraper written in Python.

## Prerequisites
Before running the project, ensure you have the following installed:
- **Node.js** (v16 or later) & **npm**
- **Python** (v3.8 or later) & **pip**
- **Virtualenv** (for managing Python dependencies)

---

## Running the NestJS Server

1. Navigate to the project root:
   ```sh
   cd my-nest-app

2. Install dependencies:
   ```sh
   npm install
   
3. Start the NestJS server in development mode:
     ```sh
     npm run start

4. The backend server will start at:
     ```sh
     http://localhost:3000
     
## Setting Up and Running the Python Scraper

1. Navigate to the scrapper:
   ```sh
   cd scrapper

2. Create a virtual environment:
   ```sh
   python -m venv env

3. Activate the virtual environment
     ```sh
     .\env\Scripts\activate

4. Install dependencies:
     ```sh
     pip install -r requirements.txt
     
4. Start the scraper server:
     ```sh
     python main.py
     
5. The scrapper server will start at:
     ```sh
     http://127.0.0.1:5000/
     
## Project Structure

  ```sh
  my-nest-app/       # NestJS Backend
  scrapper/          # Python Web Scraper
    ├── env/         # Virtual Environment (ignored in .gitignore)
    ├── main.py      # Main script to run scraper
    ├── requirements.txt  # Dependencies for the scraper
    ├── __pycache__/ # Cached Python files (ignored in .gitignore)


