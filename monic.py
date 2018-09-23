from collections import deque
from urlparse import urljoin
import requests
from lxml import html
import csv
import re
import sys



class crapper:
    base_url = "https://www.ibba.org"
    main_url = "https://www.ibba.org/texas-state/" 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
   

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

        self.visited = set([])
        self.links = deque([self.main_url])
        self.maill = None
    
        self.storage = []
    
       

    def crawl(self):
        while self.links:
            link = self.links.popleft()
            self.scrape(link)

    def scrape(self, link):
        if link in self.visited:
            return
       
        self.visited.add(link)
        print('Scraping Now: ' + link)

        

        try:

            self.response = self.session.get(link)

        except:

            pass
        
        try:

            self.tree = html.fromstring(self.response.text)

        except Exception:
            pass
        companies_links = self.tree.xpath("//div[@class='store col-md-3']//a/@href")
        
        
        

        # extracting the follow up links
             

        links = companies_links

        
       

        for link in links:
            link = urljoin(self.base_url, link)
            if link not in self.visited:
                self.links.append(link)
        
            

        # going to the main page of each companies link and harvest the record
        is_companies_links_page = self.tree.xpath("//div[@class='container']")
        
        if is_companies_links_page:
           
            try:

                name = self.tree.findtext(".//div[@class='member-profile']/h1")

            except IndexError:
                
                name = ""

            try:

                x = self.tree.xpath(".//table[@class='table']//tr[@class='address']//td[2]//text()")
                
                location =  " ".join(x[1:3])
               

            except IndexError:
                
                location = ""


            try:
 
                emailDirty = self.tree.xpath('//tr[5]/td[2]/a/@onclick')[0]
                d = re.findall(r"'(.*?)'", emailDirty, re.DOTALL)
                self.maill = d[0] + "@" + d[1]
                
            except IndexError:
                
                emailDirty = ""

            if self.maill not in self.storage:
                self.storage.append((name,location,self.maill))
                    
            

        #    self.storage.append((name,location,self.email))

        data = self.storage

        csvfile = "texac.csv"

        with open(csvfile, "w") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(data)
                     
        

if __name__ == '__main__':

    crawler = crapper()
    crawler.crawl()  
     
