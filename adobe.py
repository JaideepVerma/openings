import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import os
from datetime import datetime, timezone, timedelta

def get_ist_timestamp():
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")

def scrape_adobe():
    url = "https://careers.adobe.com/widgets"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "Accept": "*/*"
    }
    payload = {"lang":"en_us","deviceType":"desktop","country":"us","pageName":"Engineering and Product jobs","ddoKey":"refineSearch","sortBy":"Most recent","subsearch":"","from":0,"irs":'false',"jobs":'true',"counts":'true',"all_fields":["remote","country","state","city","experienceLevel","category","profession","employmentType","jobLevel"],"pageType":"category","size":20,"clearAll":'false',"jdsource":"facets","isSliderEnable":'false',"pageId":"page62-ds","siteType":"external","keywords":"","global":'true',"selected_fields":{"category":["Engineering and Product"],"country":["India"]},"sort":{"order":"desc","field":"postedDate"},"locationData":{}}

    response = requests.post(url, headers=headers,json=payload)
    data = response.json()
    data = (data["refineSearch"]["data"])

    all_jobs=[]
    for job in data["jobs"]:
        
        job_id = (job.get("reqId",[]))
        role = (job.get("title",[]))
        location = (job.get("city",[]))
        apply_link = (job.get("applyUrl",[]))
        posting_date = (job.get("postedDate",[]))
        date_created = (job.get("dateCreated",[]))
        JobFamily = (job.get("category",[]))
        
        all_jobs.append({
                "company": "ADOBE",
                "industry": 'FAANG',
                "job_id": job_id,
                "role": role,
                "description": 'description',
                "JobFunction" : 'JobFunction',
                "JobFamily" : JobFamily,
                "responsibilities": 'responsibilities',
                "qualifications": 'qualifications',
                "location": location,
                "posting_date": posting_date,
                "update_date" : 'Null',
                "apply_link": apply_link
            })
    #print(all_jobs)
    print(len(all_jobs))
    return all_jobs


def save_jobs(jobs):
    # Get current directory
    current_dir = os.getcwd()
    dbpath = os.path.join(current_dir, 'adobejobs.db')
    #dbpath = f'C:/Users/jdver/OneDrive/Desktop/py/JPMCjobs.db'
    #print('Jobs added to : ' , dbpath)
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    #print(jobs)
    for job in jobs:

        c.execute("SELECT * FROM jobs WHERE company=? AND job_id=?",
                  (job["company"], job["job_id"]))
        if not c.fetchone():
            c.execute("""INSERT INTO jobs 
                         (company,industry, job_id, role, description, responsibilities, qualifications, location, posting_date, job_family, job_function,update_date, apply_link) 
                         VALUES (?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?)""",
                      (job["company"],job["industry"], job["job_id"], job["role"], job["description"], job["responsibilities"], job["qualifications"], job["location"], job["posting_date"], job["JobFamily"], job["JobFunction"],job["update_date"],job["apply_link"])) ##
    conn.commit()
    conn.close()

def create_db():
    current_dir = os.getcwd()
    dbpath = os.path.join(current_dir, 'adobejobs.db')
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    #c.execute('''DROP Table jobs''')
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

    #print("Jobs table updated successfully.")

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
    jobs =scrape_adobe()
    save_jobs(jobs)
    
    print('Adobe Jobs saved to .db')
    #print("Running JPMC scraper...")

if __name__ == "__main__":
    main()
    


   
