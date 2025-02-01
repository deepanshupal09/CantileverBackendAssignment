# Project Documentation

## Overview

This project consists of two main components:
1. **NestJS Server** - The backend server for handling API requests and scheduling cron jobs.
2. **Python Scraper** - A web scraper written in Python for fetching job listings from various websites.

The NestJS server includes a cron job that triggers the Python scrapers at regular intervals to fetch job listings and store them in a PostgreSQL database.

## Architecture and Technologies

### NestJS Server
- **Framework**: NestJS
- **Language**: TypeScript
- **Database**: PostgreSQL
- **ORM**: TypeORM
- **Scheduling**: `@nestjs/schedule`

The NestJS server is responsible for scheduling the cron jobs and handling API requests. It uses TypeORM to interact with the PostgreSQL database and the `@nestjs/schedule` package to manage the cron jobs.

### Python Scraper
- **Framework**: Flask
- **Language**: Python
- **Libraries**: 
  - `requests` for making HTTP requests
  - `BeautifulSoup` for parsing HTML
  - `psycopg2` for PostgreSQL database interaction

The Python scraper is responsible for fetching job listings from various websites. It uses the `requests` library to make HTTP requests, `BeautifulSoup` to parse the HTML content, and `psycopg2` to interact with the PostgreSQL database.

### Cron Job
The cron job is implemented in the NestJS server using the `@nestjs/schedule` package. It triggers the Python scrapers by making HTTP GET requests to the Flask endpoints.

## Frequency of the Cron Job

- The cron job is scheduled to run every 12 hours using the `CronExpression.EVERY_12_HOURS` expression. This frequency is chosen to ensure that the job listings are updated regularly without overwhelming the target websites or the server.
  
    ```sh
    import { Cron, CronExpression } from '@nestjs/schedule';
    
    @Cron(CronExpression.EVERY_12_HOURS)
    async handleCron() {
      // Cron job logic
    }

## Reasoning for Frequency
- Regular Updates: Running the cron job every 12 hours ensures that the job listings are updated regularly.
- Server Load: This frequency helps in balancing the server load and avoids overwhelming the target websites.
- Data Freshness: Ensures that the data remains fresh and relevant for users.
- Avoiding Duplications
- To avoid duplications while scraping the same website repeatedly, the scrapers use the ON CONFLICT DO NOTHING clause in the PostgreSQL INSERT statements. This ensures that  if a job listing with the same apply_link already exists in the database, it will not be inserted again.
    
    ```sh
    insert_query = """
    INSERT INTO public.jobs (apply_link, job_title, job_description, location, experience_level, company)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (apply_link) DO NOTHING;
    """

## Additional Measures
- Unique Constraints: Ensure that the apply_link field in the database has a unique constraint.
- Hashing: Optionally, use hashing to detect duplicate content if URLs are not unique.

## Possible Errors
### Network Errors
- Description: Issues with network connectivity can prevent the scrapers from accessing the target websites.
- Handling: Implement retry logic and error handling in the scrapers.
    
    ```sh
    import requests
    from requests.exceptions import RequestException
    
    def fetch_url(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except RequestException as e:
            print(f"Network error: {e}")
            return None

### Database Connection Errors
- Description: Issues with connecting to the PostgreSQL database.
- Handling: Ensure proper database configuration and implement retry logic.
    
    ```sh
    import psycopg2
    from psycopg2 import OperationalError
    
    def connect_db():
        try:
            connection = psycopg2.connect(
                dbname="your_db",
                user="your_user",
                password="your_password",
                host="your_host",
                port="your_port"
            )
            return connection
        except OperationalError as e:
            print(f"Database connection error: {e}")
            return None

### Parsing Errors

- Description: Errors while parsing the HTML content of the target websites.
- Handling: Implement robust error handling and logging in the scrapers.

    ```sh
    from bs4 import BeautifulSoup
    
    def parse_html(html_content):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            // Parsing logic
        except Exception as e:
            print(f"Parsing error: {e}")



## Schema/Model of the Scraped Data

- The scraped job data is stored in a PostgreSQL database with the following schema:

    ```sh
    // filepath: src/jobs/jobs.entity.ts
    import { Entity, Column, PrimaryColumn } from 'typeorm';
    
    @Entity('jobs')
    export class Job {
      @PrimaryColumn()
      apply_link: string;  
    
      @Column({ nullable: true })
      job_title: string; 
      
      @Column('text', { nullable: true })
      job_description: string;  
    
      @Column({ nullable: true })
      location: string;  
    
      @Column({ nullable: true })
      experience_level: string;  
    
      @Column({ nullable: true })
      company: string;  
    }

### Fields
- apply_link: The URL to apply for the job (Primary Key).
- job_title: The title of the job.
- job_description: The description of the job.
- location: The location of the job.
- experience_level: The required experience level for the job.
- company: The company offering the job.


