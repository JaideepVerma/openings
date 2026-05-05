import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import os
from datetime import datetime, timezone, timedelta, date, time 

def days_from_posted(text):
    """
    Return integer number of days if 'day' appears, else None.
    Examples:
      'Posted 21 days ago' -> 21
      'Posted 1 day ago'  -> 1
      'Posted today'      -> 0 (optional handling below)
    """
    if not text:
        return None
    text = text.strip().lower()
    # direct match for "today"
    if 'today' in text:
        return 0
    m = re.search(r'(\d+)\s*day', text)
    return int(m.group(1)) if m else None


def get_date(dt):
    # Parse the string into a datetime object
    dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
     
    # Format it into DD-MM-YYYY
    formatted_date = dt.strftime("%d-%m-%Y")
    return formatted_date
def get_ist_timestamp():
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")

def scrape_wellsfargo():
    url = "https://wd1.myworkdaysite.com/wday/cxs/wf/WellsFargoJobs/jobs" # "https://careers.adobe.com/widgets"
    

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Origin": "https://wd1.myworkdaysite.com",
        #"Referer": urljoin(BASE, PAGE_URL),
        "Content-Type": "application/json"
    }
    limit = 20
    offset = 0
    all_jobs=[]
    while offset <=20:
        print('Limit and offset',limit,offset)
        payload =     {
            "appliedFacets":{"locationCountry":["c4f78be1a8f14da0ab49ce1162348a5e"],"workerSubType":["2d264dd4beb00100f05a7cc5745b0001"],"jobFamilyGroup":["b5c3287c76c20100b318a0e7d1fd0002","b5c3287c76c20100b3189b6fdb430000","b5c3287c76c20100b318a19542940001"]},"limit":limit,"offset":offset,
            "searchText":""}
        
        '''payload =     {
            "appliedFacets":{"locationCountry":["c4f78be1a8f14da0ab49ce1162348a5e"],"workerSubType":["2d264dd4beb00100f05a7cc5745b0001"]},"limit":20,"offset":10,
            "searchText":""}
        '''

        response = requests.post(url, headers=headers,json=payload)
        data = response.json()
        #print(data)
    
        data = (data["jobPostings"])
        #print(len(data))
        
        
        for job in data:
            #print(job)
            job_id = (job.get("bulletFields",[]))
            role = (job.get("title",[]))
            location = (job.get("locationsText",[]))
            apply_link = (job.get("externalPath",[]))
            posting_date = (job.get("postedOn",[]))
            #date_created = (job.get("dateCreated",[]))
            #JobFamily = (job.get("category",[]))
            posting_date = days_from_posted(posting_date)
            if posting_date == 0:
                posting_date = str(datetime.combine(date.today(), time()))
            else:
                posting_date = str(date.today() - timedelta(days=posting_date))

            #print(job_id[0], role,location,apply_link,posting_date)
            
            #print(get_date(posting_date))
            all_jobs.append({
                    "company": "Wells Fargo",
                    "industry": 'Financial Services',
                    "job_id": job_id[0],
                    "role": role,
                    "description": 'description',
                    "JobFunction" : 'JobFunction',
                    "JobFamily" : 'JobFamily',
                    "responsibilities": 'responsibilities',
                    "qualifications": 'qualifications',
                    "location": location,
                    "posting_date": get_date(posting_date),
                    "update_date" : 'Null',
                    "apply_link": apply_link
                })
        #print(all_jobs)
        
        #limit += 10
        offset += 20
    print(len(all_jobs))
    return all_jobs


def save_jobs(jobs):
    # Get current directory
    current_dir = os.getcwd()
    dbpath = os.path.join(current_dir, 'wellsfargojobs.db')
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
    dbpath = os.path.join(current_dir, 'wellsfargojobs.db')
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
    jobs =scrape_wellsfargo()
    save_jobs(jobs)
    
    print('WellsFargo Jobs saved to .db')
    #print("Running JPMC scraper...")

if __name__ == "__main__":
    main()
    


   
