import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import json
import re
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional
try:
    from bs4 import BeautifulSoup
    _HAS_BS4 = True
except Exception:
    _HAS_BS4 = False


def get_ist_timestamp():
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")

url = "https://swiggy.mynexthire.com/employer/careers/reqlist/get"

headers = {
    "accept": "application/json",
    "Content-Type": "application/json;charset=UTF-8",
    "x-api-key": "PbxxNwIlTi4FP5oijKdtk3IrBF5CLd4R4oPHsKNh",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
}

def scrape_swiggy():
    # Payload copied from DevTools
    payload = {
        "source": "careers",
        "code": "",
        "filterByBuId": -1,
        "filterByCustomField": {
            "career_page_category": "Technology"
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    #print(data['reqDetailsBOList'])
    jobs = data.get("reqDetailsBOList",[])
    #print(jobs)
    all_jobs=[]
    for job_data in jobs:
        #job_data = item.get("data", {})
        req_id = job_data.get("reqId")
        #print(req_id)
        title = job_data.get("reqTitle")
        description = job_data.get("jdDisplay")
        qualificationsRAW = description
        qualifications_index_start = qualificationsRAW.find("What qualities are we looking for?")
        qualifications_index_end=qualificationsRAW.find("What will you get to do here?")
        responsibilities_index_end = qualificationsRAW.find("Visit our tech blogs")
        qualifications = description[qualifications_index_start:qualifications_index_end]
        responsibilities = description[qualifications_index_end:responsibilities_index_end]
        location = job_data.get("location")
        #city = job_data.get("city")
        #state = job_data.get("state")
        #country = job_data.get("country")
        posted_date = job_data.get("approvedOn")
        job_family= job_data.get("buName")
        #create_date=job_data.get("create_date")
        #update_date=job_data.get("update_date")
        apply_url = 'https://careers.swiggy.com/#/careers?src=careers&career_page_category=Technology' 
        
        all_jobs.append({
                        "company": "SWIGGY",
                        "job_id": req_id,
                        "role": title,
                        "description": 'description',
                        "JobFunction" : 'JobFunction',
                        "JobFamily" : job_family,
                        "responsibilities": responsibilities,
                        "qualifications": qualifications,
                        "location": location,
                        "posting_date": posted_date,
                        "update_date" : 'update_date',
                        "apply_link": apply_url            
                    })
    #hit = data['searchHits'][0]        # TEST
    #fields = hit.get("fields", {})     # TEST
    #print(all_jobs)                      # TEST
    return all_jobs

def save_jobs(jobs):
    dbpath = "swiggyjobs.db"
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    for job in jobs:

        c.execute("SELECT * FROM jobs WHERE company=? AND job_id=?",
                  (job["company"], job["job_id"]))
        if not c.fetchone():
            c.execute("""INSERT INTO jobs 
                         (company, job_id, role, description, responsibilities, qualifications, location, posting_date, job_family, job_function, apply_link, update_date) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)""",
                      (job["company"], job["job_id"], job["role"], job["description"], job["responsibilities"], job["qualifications"], job["location"], job["posting_date"], job["JobFamily"], job["JobFunction"], job["apply_link"], job["update_date"]))
    conn.commit()
    conn.close()

#Run Below if there is any new column 
'''
conn = sqlite3.connect("JPMCjobs.db")
cur = conn.cursor()
cur.execute("ALTER TABLE jobs ADD COLUMN loaded_at TEXT;")
conn.commit()
conn.close() 
'''
def create_db():
    conn = sqlite3.connect("swiggyjobs.db")
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


def main():
    create_db()
    jobs = scrape_swiggy()
    save_jobs(jobs)
    print('SWIGGY -Jobs saved to .db')    
if __name__ == "__main__":
    main()