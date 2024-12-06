import requests
import bs4 as bs
import xml.etree.ElementTree as ET

class XMLParser:
    ...
    
    
    
class XMLHandler:
    
    def __init__(self, ticker, cik):
        self.ticker = ticker
        self.cik = cik
        
        self.headers = {
            'User-Agent': 'aarnereime01@gmail.com',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'www.sec.gov'
        }


    def make_xml_link(self):
        # First get the Accession Number to the lastest 10-K
        url = f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={self.cik}&type=10-K&dateb=&owner=exclude&count=40&search_text='
        
        homepage = requests.get(url, headers=self.headers)
        
        # Parse the HTML
        soup = bs.BeautifulSoup(homepage.text, 'html.parser')
        
        # Find the first document link
        doc_link = soup.find('a', {'id': 'documentsbutton'})['href']
        
        # Get the document page
        doc_page = requests.get(f'https://www.sec.gov{doc_link}', headers=self.headers)
        
        # Get the the text that includes _lab, then get that href
        soup = bs.BeautifulSoup(doc_page.text, 'html.parser')
        link = soup.find('a', href=lambda x: x and '_lab.xml' in x)
        if link:
            xml_link = link['href']
            return f'https://www.sec.gov{xml_link}'
        
    
    def get_xml_labels(self, xml_link):
        response = requests.get(xml_link, headers=self.headers)
        
        root = ET.fromstring(response.content)
        
        namespace = {
            'link': 'http://www.xbrl.org/2003/linkbase',
            'xlink': 'http://www.w3.org/1999/xlink'
        }
        
        filing_entities = []
        for link_label in root.findall('.//link:label', namespace):
            xml_xlink_label = link_label.attrib.get(f'{{{namespace["xlink"]}}}label')
            
            taxonomy = xml_xlink_label.split('_')[1]
            
            if taxonomy in ['us-gaap', 'dei'] and xml_xlink_label not in filing_entities:
                filing_entities.append(xml_xlink_label)
                
        print(len(filing_entities))
        for entity in filing_entities:
            print(entity)
            
            
            
            
        ...

        
        
    def main(self):
        xml_link = self.make_xml_link()
        labels = self.get_xml_labels(xml_link)
        # print(labels)