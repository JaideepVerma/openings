import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import os
from datetime import datetime, timezone, timedelta
from datetime import datetime


def get_ist_timestamp():
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")

def scrape_ms():

    #url ="https://morganstanley.eightfold.ai/api/pcsx/search?domain=morganstanley.com&query=&location=india&start=0&sort_by=timestamp&filter_include_remote=1&filter_city=Mumbai&filter_city=Bengaluru"
    url ="https://morganstanley.eightfold.ai/api/pcsx/search?domain=morganstanley.com&query=Analytics&location=india&start=0&sort_by=timestamp&filter_include_remote=1&filter_businessarea=investment+management&filter_businessarea=risk+management&filter_city=Mumbai&filter_city=Bengaluru"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
  
    jobs= ((data["data"]["positions"]))
    
    all_jobs = []
    #print(soup)
    for job in jobs:
        #print(job.get("id"))
        #print(datetime.fromtimestamp(job.get("postedTs")))
        job_id=job.get("id")
        role=job.get("name")
        JobFamily =job.get("department")
        location=job.get("locations") 
        posting_date= datetime.fromtimestamp(job.get("postedTs"))

        all_jobs.append( {
            "company" : "Morgan Stanley",
            "industry": 'Financial Services',
            "job_id": job_id,
            "role": role,
            "description": "description...",
            "JobFunction" : "JobFunction...",
            "JobFamily" : JobFamily,
            "responsibilities": "responsibilities",
            "qualifications": "qualifications",
            "location": location[0] ,
            "posting_date": posting_date,
            "update_date" : 'Null',
            "apply_link": "https://morganstanley.eightfold.ai/careers?source=mscom&start=0&pid=" + str(job_id)
    
        })
    print(posting_date)
    print(len(jobs), " MS Jobs added")
    return all_jobs

def save_jobs(jobs):
    # Get current directory
    current_dir = os.getcwd()
    dbpath = os.path.join(current_dir, 'msjobs.db')
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
                         (company,industry, job_id, role, description, responsibilities, qualifications, location, posting_date, job_family, job_function,update_date, apply_link) 
                         VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?)""",
                      (job["company"],job["industry"], job["job_id"], job["role"], job["description"], job["responsibilities"], job["qualifications"], job["location"], job["posting_date"], job["JobFamily"], job["JobFunction"],job["update_date"],job["apply_link"])) ##
    conn.commit()
    conn.close()

def create_db():
    current_dir = os.getcwd()
    dbpath = os.path.join(current_dir, 'msjobs.db')
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    c.execute('''DROP Table jobs''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        industry TEXT,      
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
    jobs =scrape_ms()
    save_jobs(jobs)
    
    print('MS Jobs saved to .db')
    #print("Running JPMC scraper...")

if __name__ == "__main__":
    main()
    #scrape_ms()
    


   