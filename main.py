from scraper import LinkedIn


""" SELENIUM """
# Version: 4.5.0
# pip3 install selenium==4.5.0 
# &
# pip3 install -r requirements.txt



job_scraper = LinkedIn(job_name="industrial engineer", currentJobId=3599754837, geoId=92000000, number_of_jobs=None, location="Worldwide")

job_scraper.run()



