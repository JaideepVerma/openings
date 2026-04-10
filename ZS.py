import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import os

from datetime import datetime, timezone, timedelta

def get_ist_timestamp():
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")

def scrape_zs():
    url = "https://jobs.zs.com/api/jobs?location=India&woe=12&regionCode=IN&stretchUnit=MILES&stretch=10&page=1&sortBy=posted_date&descending=true&internal=false"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
    page= 1
    all_jobs = []
    while page <= 2 :
        params = {"location": "India",
            "woe": 12,
            "regionCode": "IN",
            "stretchUnit": "MILES",
            "stretch": 10,
            "page": page,
            "sortBy": "posted_date",
            "descending": True,
            "internal": False,}
        response = requests.get(url,params=params, headers=headers)
        data = response.json()
        #print(data['jobs'])
        datajobs =data['jobs']
        #print(dataa)
        jobs = data.get("jobs", [])

        for item in jobs:
            #print(item)
            if item is None:
                break
            job_data = item.get("data", {})
            req_id = job_data.get("req_id")
            title = job_data.get("title")
            #description = job_data.get("description")
            qualificationsRAW = job_data.get("qualifications")
            responsibilities = job_data.get("responsibilities")
            #print(req_id)
            if (responsibilities) :
                responsibilities_index2 = responsibilities.find("What you’ll bring")
                #print(responsibilities)
                responsibilities1 = responsibilities[:responsibilities_index2]
                responsibilities2 = responsibilities[responsibilities_index2:]
            location = job_data.get("location_name")
            city = job_data.get("city")
            state = job_data.get("state")
            country = job_data.get("country")
            posted_date = job_data.get("posted_date")
            #create_date=job_data.get("create_date")
            update_date=job_data.get("update_date")
            apply_url = 'https://jobs.zs.com/all/jobs/' + req_id if req_id  else "NA" 
            #print(responsibilities1,' --- ',responsibilities2 )
            
            #print(apply_url,req_id, title, location, city, state, country, posted_date,update_date)
            all_jobs.append({
                    "company": "ZS",
                    "industry" : 'Business Consulting and Services' ,
                    "job_id": req_id,
                    "role": title,
                    "description": 'description',
                    "JobFunction" : 'JobFunction',
                    "JobFamily" : 'JobFamily',
                    "responsibilities": responsibilities1,
                    "qualifications": responsibilities2,
                    "location": location,
                    "posting_date": posted_date,
                    "update_date" : 'update_date',
                    "apply_link": apply_url            
                })
        page += 1  
        
    print(len(all_jobs))
    return all_jobs

def create_db():

    conn = sqlite3.connect("ZSjobs.db")
    c = conn.cursor()
    #c.execute('''DROP Table jobs ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS jobs(
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
        posted_at TEXT,
        update_date TEXT
        
            
    )
    ''')

    conn.commit()
    conn.close() 

    print("Jobs table updated successfully.")

def save_jobs(jobs):
    #dbpath = f'C:/Users/jdver/OneDrive/Desktop/py/ZSjobs.db'
    current_dir = os.getcwd()
    print(current_dir)
    dbpath = os.path.join(current_dir, 'ZSjobs.db')
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    for job in jobs:

        c.execute("SELECT * FROM jobs WHERE company=? AND job_id=?",
                  (job["company"], job["job_id"]))
        if not c.fetchone():
            c.execute("""INSERT INTO jobs 
                         (company,industry job_id, role, description, responsibilities, qualifications, location, posting_date, job_family, job_function, apply_link, update_date) 
                         VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?)""",
                      (job["company"],job["industry"], job["job_id"], job["role"], job["description"], job["responsibilities"], job["qualifications"], job["location"], job["posting_date"], job["JobFamily"], job["JobFunction"], job["apply_link"],job["update_date"]))
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

def main():
    create_db()
    jobs = scrape_zs()
    save_jobs(jobs)
    print('ZS Jobs saved to .db')  
if __name__ == "__main__":
    main()
