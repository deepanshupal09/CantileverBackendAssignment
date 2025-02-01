import requests
from bs4 import BeautifulSoup
import psycopg2

# Function to fetch job links from a given page
def fetch_job_links(page, headers):
    URL = f'https://jobsindia.deloitte.com/search/?q=&sortColumn=referencedate&sortDirection=desc&startrow={(page-1)*25+1}'
    r = requests.get(url=URL, headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')
    
    jobLinks = []
    for a in soup.find_all('a', class_='jobTitle-link'):
        href = a['href']
        jobLinks.append(f'https://jobsindia.deloitte.com{href}')
    
    return jobLinks


# Function to fetch job details from the job page
def fetch_job_details(jobLink, headers):
    job = requests.get(url=jobLink, headers=headers)
    jobSoup = BeautifulSoup(job.content, 'html5lib')

    job_title = jobSoup.find('span', attrs={'data-careersite-propertyid': 'title'})
    location = jobSoup.find('span', attrs={'data-careersite-propertyid': 'city'})

    apply_tag = jobSoup.find('a', class_='btn btn-primary btn-large btn-lg apply dialogApplyBtn')
    # apply_link = f'https://jobsindia.deloitte.com{apply_tag["href"]}' if apply_tag else None

    description = jobSoup.find('span', attrs={'data-careersite-propertyid': 'description'})
    job_description = "\n".join([para.get_text(strip=True) for para in description.find_all('p')]) if description else "Job description not found."

    job_data = {
        "title": job_title.get_text() if job_title else "No Title",
        "apply_link": jobLink,
        "job_description": job_description,
        "location": location.get_text() if location else "Location not available",
        "exp_level": None,
        "company": "Deloitte"
    }
    
    return job_data


# Function to insert job data into the PostgreSQL database
def insert_job_to_db(job_data):
    conn = psycopg2.connect(
        "postgresql://deepanshupal:NyVoSBDZhnRgKKMg7lHSdU57Kc76VaK4@dpg-cuf26956l47c73fabv00-a.singapore-postgres.render.com/scrapper_tztj"
    )
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO public.jobs (apply_link, job_title, job_description, location, experience_level, company)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (apply_link) DO NOTHING;
    """
    cursor.execute(insert_query, (
        job_data['apply_link'],
        job_data['title'],
        job_data['job_description'],
        job_data['location'],
        job_data['exp_level'],
        job_data['company']
    ))
    conn.commit()
    cursor.close()
    conn.close()


# Main function to scrape job data from multiple pages and store it in the database
def scrape_jobs_deloitte(pages=1):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
    }

    for page in range(1, pages+1):  
        print(f"Fetching for page: {page}")    
        jobLinks = fetch_job_links(page, headers)

        for jobLink in jobLinks:
            job_data = fetch_job_details(jobLink, headers)
            insert_job_to_db(job_data)  # Insert job data into the database
    
    print(f"Scraping and insertion for {pages} pages completed.")


# Start scraping and inserting jobs into the database
# scrape_jobs_deloitte(2)
