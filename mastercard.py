import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import os

from datetime import datetime, timezone, timedelta

def get_ist_timestamp():
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")

def scrape_mastercard():
    url = "https://careers.mastercard.com/widgets"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "*/*"
    }
    payload = {"lang":"en_us","deviceType":"desktop","country":"us","pageName":"search-results","ddoKey":"eagerLoadRefineSearch","sortBy":"Most recent","subsearch":"","from":0,"jobs":'true',"counts":'true',"all_fields":["category","country","state","city","postalCode","jobType","phLocSlider"],"size":20,"clearAll":'false',"jdsource":"facets","isSliderEnable":'true',"pageId":"page11","siteType":"external","keywords":"","global":'true',"selected_fields":{"country":["India"]},"sort":{"order":"desc","field":"postedDate"},"locationData":{"sliderRadius":302,"aboveMaxRadius":'true',"LocationUnit":"kilometers"},"s":"1"}
    #response = requests.get()
    response = requests.post(url, headers=headers,json=payload)
    resp = response.json()
    hits= resp.get("eagerLoadRefineSearch",[]).get("data",[]).get("jobs",[])
    #print(hits)
    all_jobs=[]
    for hit in hits:
        #print(hit)
        job_id = hit.get("reqId")
        role = hit.get("title")
        skills = hit.get("ml_skills")
        description = hit.get("descriptionTeaser")
        responsibilities ='responsibilities'
        qualifications = 'qualifications'
        location=hit.get("city")
        timestamp =hit.get("postedDate")
        posting_date =datetime.strptime(timestamp , "%Y-%m-%dT%H:%M:%S.%f%z").date()
        created_date = hit.get("dateCreated")
        JobFunction = 'JobFunction'
        JobFamily = hit.get("category")
        #print(posting_date) 

        #print(title)
        all_jobs.append({
            "company": "MasterCard",
            "industry": 'IT Services and Consulting',
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
            "apply_link": 'https://careers.mastercard.com/us/en/job/'+ job_id                
            
        })
    
    print(len(all_jobs) , ' MasterCard jobs added')
    return all_jobs


def create_db():

    conn = sqlite3.connect("mastercardjobs.db")
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

    #print("Jobs table updated successfully.")

def save_jobs(jobs):
    #dbpath = f'C:/Users/jdver/OneDrive/Desktop/py/ZSjobs.db'
    current_dir = os.getcwd()
    #print(current_dir)
    dbpath = os.path.join(current_dir, 'mastercardjobs.db')
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    for job in jobs:

        c.execute("SELECT * FROM jobs WHERE company=? AND job_id=?",
                  (job["company"], job["job_id"]))
        if not c.fetchone():
            c.execute("""INSERT INTO jobs 
                         (company,industry, job_id, role, description, responsibilities, qualifications, location, posting_date, job_family, job_function, apply_link, update_date) 
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
    jobs = scrape_mastercard()
    save_jobs(jobs)
    print('masterCard Jobs saved to .db')  
if __name__ == "__main__":
    main()
    #scrape_mastercard()
