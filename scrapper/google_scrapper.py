import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2 import sql

# PostgreSQL connection details
DATABASE_URL = 'postgresql://deepanshupal:NyVoSBDZhnRgKKMg7lHSdU57Kc76VaK4@dpg-cuf26956l47c73fabv00-a.singapore-postgres.render.com/scrapper_tztj'

# Connect to PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Function to fetch the job links from a given page
def fetch_job_links(page):
    URL = f'https://www.google.com/about/careers/applications/jobs/results?page={page}'
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
    }

    # Fetch job listings page
    r = requests.get(url=URL, headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')

    # Extract all job links
    job_links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('jobs/results/') and href[13:]:
            job_links.append(f'https://www.google.com/about/careers/applications/jobs/results/{href[13:]}')
    
    return job_links

# Function to extract job details from a job page
def extract_job_details(joblink):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
    }

    # Fetch job page
    job = requests.get(url=joblink, headers=headers)
    job_soup = BeautifulSoup(job.content, 'html5lib')

    # Extract job title
    job_title_div = job_soup.find('div', attrs={'data-title': True})
    job_title = job_title_div.get('data-title') if job_title_div else "No Title"

    # Extract apply link
    apply_link = ''
    for a in job_soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('./apply'):
            apply_link = f"https://www.google.com/about/careers/applications/{href[2:]}"  # Convert relative to absolute URL
            break

    # Extract location
    location = None
    location_icons = job_soup.find_all('i', class_="google-material-icons notranslate VfPpkd-kBDsod dPX0he")
    for icon in location_icons:
        if icon.get_text(strip=True) == "place" and icon.next_sibling:
            location = icon.next_sibling.get_text(strip=True)
            break

    # Extract experience level
    experience_level = None
    exp_icons = job_soup.find_all('i', class_="google-material-icons notranslate VfPpkd-kBDsod")
    for icon in exp_icons:
        if icon.get_text(strip=True) == "bar_chart":
            experience_span = icon.find_next('span')
            if experience_span:
                experience_level = experience_span.get_text(strip=True)
            break

    # Extract qualifications and job description
    min_qual_list = extract_qualifications(job_soup, 'Minimum qualifications:')
    pref_qual_list = extract_qualifications(job_soup, 'Preferred qualifications:')
    job_description = extract_job_description(job_soup)

    job_data = {
        "title": job_title,
        "apply_link": apply_link,
        "job_description": f"{min_qual_list}\n{pref_qual_list}\n{job_description}",
        "location": location,
        "exp_level": experience_level,
        "company": "Google"
    }

    return job_data

# Function to extract qualifications (min or pref)
def extract_qualifications(job_soup, header_text):
    qual_list = []
    qual_header = job_soup.find('h3', string=header_text)
    if qual_header:
        qual_ul = qual_header.find_next('ul')
        qual_list = [li.get_text(strip=True) for li in qual_ul.find_all('li')] if qual_ul else []

    return "\n".join(qual_list)

# Function to extract job description
def extract_job_description(job_soup):
    aboutjob_section = job_soup.find('h3', string="About the job")
    aboutjob = ""
    
    # Extracting about the job section
    if aboutjob_section:
        aboutjob_section = aboutjob_section.find_next_sibling()
        while aboutjob_section and aboutjob_section.name == 'p':
            aboutjob += str(aboutjob_section.get_text())+'\n'
            aboutjob_section = aboutjob_section.find_next_sibling()

    # Extracting responsibilities section
    responsibilities_header = job_soup.find('h3', string="Responsibilities")
    if responsibilities_header:
        responsibilities_list = responsibilities_header.find_next('ul')
        if responsibilities_list:
            responsibilities = [li.get_text(strip=True) for li in responsibilities_list.find_all('li')]
            aboutjob += "\n".join(responsibilities)  

    return aboutjob
# Function to insert job data into the database
def insert_job_data(job_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    insert_query = sql.SQL("""
        INSERT INTO public.jobs (apply_link, job_title, job_description, location, experience_level, company)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (apply_link) DO NOTHING;
    """)
    
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

# Main function to scrape job data across multiple pages
def scrape_jobs(pages=1):
    jobs_data = []

    for page in range(1, pages+1):
        print(f"Fetching jobs from page {page}...")
        job_links = fetch_job_links(page)
        print(f"Fetched {len(job_links)} job links from page {page}. Extracting data...")

        for joblink in job_links:
            job_data = extract_job_details(joblink)
            jobs_data.append(job_data)
            insert_job_data(job_data)  

    return jobs_data


# def print_job_data(jobs_data):
#     for job in jobs_data:
#         print("\n===================================")
#         print(f"Title: {job['title']}")
#         print(f"Apply Link: {job['apply_link']}")
#         print(f"Job Description: {job['job_description']}")
#         print(f"Location: {job['location']}")
#         print(f"Experience Level: {job['exp_level']}")


# jobs_data = scrape_jobs(1)
# print_job_data(jobs_data)
