import requests
import csv

def scrape_rozee():
    url = "https://remotive.io/api/remote-jobs"
    response = requests.get(url)
    data = response.json()

    jobs = []
    for job in data['jobs'][:100]:  # Get first 100 jobs
        title = job['title'] 
        company = job['company_name']
        location = job['candidate_required_location']
        date_posted = job['publication_date']

        jobs.append([title, company, location, date_posted])

    # Save to CSV
    with open('jobs.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'Company', 'Location', 'Date Posted'])
        writer.writerows(jobs)

# Run this only if called directly (optional for Streamlit)
if __name__ == "__main__":
    scrape_rozee()
