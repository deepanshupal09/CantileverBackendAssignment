from flask import Flask, request
import google_scrapper
import deloitte_scrapper

app = Flask(__name__)

@app.route('/google-scraper', methods=['GET'])
def google_scraper():    
    
    pages = request.args.get('pages', default=1, type=int)    
    google_scrapper.scrape_jobs(pages=pages)    
    return f'Google jobs scraping initiated for {pages} page(s).'

@app.route('/deloitte-scraper', methods=['GET'])
def deloitte_scraper():

    pages = request.args.get('pages', default=1, type=int)    
    deloitte_scrapper.scrape_jobs_deloitte(pages=pages)    
    return f'Deloitte jobs scraping initiated for {pages} page(s).'

if __name__ == '__main__':
    app.run(debug=True, port=5000)
