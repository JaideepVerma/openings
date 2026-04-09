import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import os
from datetime import datetime, timezone, timedelta

def get_ist_timestamp():
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")

def scrape_barclays():
    url = "https://search.jobs.barclays/search-jobs/results?ActiveFacetID=44699&CurrentPage=1&RecordsPerPage=30&TotalContentResults=&Distance=50&RadiusUnitType=0&Keywords=&Location=India&Latitude=22.00000&Longitude=79.00000&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=8736240&FacetFilters%5B0%5D.FacetType=1&FacetFilters%5B0%5D.Count=30&FacetFilters%5B0%5D.Display=Data+%26+Analytics&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=1&LocationType=2&LocationPath=1269750&OrganizationIds=13015&PostalCode=&ResultsType=0&fc=&fl=&fcf=&afc=&afl=&afcf=&TotalContentPages=NaN"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "Accept": "*/*"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    html_results = data["results"]
    #print(html_results)
    soup = BeautifulSoup(html_results, "html.parser")

    jobs = []
    #print(soup)
    for card in soup.select("div.list-item.list-item--card"):
        title_tag = card.select_one("a.job-title--link")
        location_tag = card.select_one("div.job-location")
        #jobdate=card.select_one("div.job-date") 
        date_text = card.find("span").get_text(strip=True)  
        #print(date_text)     
        job = {
            "company" : "Barclays",
            "job_id": title_tag.get("data-job-id"),
            "role": title_tag.get_text(strip=True),
            "description": "description...",
            "JobFunction" : "JobFunction...",
            "JobFamily" : "JobFamily...",
            "responsibilities": "responsibilities",
            "qualifications": "qualifications",
            "location": location_tag.get_text(strip=True) if location_tag else None,
            "posting_date": date_text,
            "update_date" : 'Null',
            "apply_link": "https://search.jobs.barclays" + title_tag["href"],
    
        }
        print(date_text)
        jobs.append(job)
    print(len(jobs), "barclays Jobs added")
        
    return jobs

    '''
    
    for item in data.get("items", []):
        for req in item.get("requisitionList", []):
            job_id = req.get("Id")
            role = req.get("Title", "N/A")
            description = req.get("ShortDescriptionStr", "N/A")
            responsibilities = req.get("ExternalResponsibilitiesStr", "N/A")
            qualifications = req.get("ExternalQualificationsStr", "N/A")
            location = req.get("PrimaryLocation", "N/A")
            posting_date = req.get("PostedDate", "N/A")
            apply_link = req.get("ExternalApplyLink", "N/A")
            JobFunction = req.get("JobFunction","N/A")
            JobFamily = req.get("JobFamily",'N/A')

            jobs.append({
                "company": "JPMC",
                "job_id": job_id,
                "role": role,
                "description": description,
                "JobFunction" : JobFunction,
                "JobFamily" : JobFamily,
                "responsibilities": responsibilities,
                "qualifications": qualifications,
                "location": location,
                "posting_date": posting_date,
                "update_date" : 'Null',
                "apply_link": 'https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/job/' + job_id                
            })
    #print(jobs)
    return jobs
    '''

def save_jobs(jobs):
    # Get current directory
    current_dir = os.getcwd()
    dbpath = os.path.join(current_dir, 'barclaysjobs.db')
    #dbpath = f'C:/Users/jdver/OneDrive/Desktop/py/JPMCjobs.db'
    print('Jobs added to : ' , dbpath)
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    #print(jobs)
    for job in jobs:

        c.execute("SELECT * FROM jobs WHERE company=? AND job_id=?",
                  (job["company"], job["job_id"]))
        if not c.fetchone():
            c.execute("""INSERT INTO jobs 
                         (company, job_id, role, description, responsibilities, qualifications, location, posting_date, job_family, job_function,update_date, apply_link) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?)""",
                      (job["company"], job["job_id"], job["role"], job["description"], job["responsibilities"], job["qualifications"], job["location"], job["posting_date"], job["JobFamily"], job["JobFunction"],job["update_date"],job["apply_link"])) ##
    conn.commit()
    conn.close()

def create_db():
    current_dir = os.getcwd()
    dbpath = os.path.join(current_dir, 'barclaysjobs.db')
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    #c.execute('''DROP Table jobs''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        job_id TEXT,
        role TEXT,
        description TEXT,
        responsibilities TEXT,
        qualifications TEXT,
        location TEXT,
        posting_date TEXT,
        job_family TEXT,
        job_function TEXT,
        apply_link TEXT,
        update_date TEXT,
        loaded_at TEXT 
            
    )
    ''')
    conn.commit()
    conn.close()

    print("Jobs table updated successfully.")

#Run Below if there is any new column 
'''
conn = sqlite3.connect("JPMCjobs.db")
cur = conn.cursor()
cur.execute("ALTER TABLE jobs ADD COLUMN update_date TEXT;")
conn.commit()
conn.close() 
'''
def main():
    # put your scraping logic here
    create_db()
    jobs =scrape_barclays()
    save_jobs(jobs)
    
    print('Barclays Jobs saved to .db')
    #print("Running JPMC scraper...")

if __name__ == "__main__":
    main()
    


   
