from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as  uReq
import requests

urls = [#'https://en.wikipedia.org/wiki/Category:English_football_logos',
        #'https://en.wikipedia.org/w/index.php?title=Category:English_football_logos&filefrom=Chessington+%26+Hook+United+F.C.+logo.png#mw-category-media'
        #'https://en.wikipedia.org/w/index.php?title=Category:English_football_logos&filefrom=Hayling+United+logo.png#mw-category-media',
        #'https://en.wikipedia.org/w/index.php?title=Category:English_football_logos&filefrom=Norton-United-Logo.png#mw-category-media',
        'https://en.wikipedia.org/w/index.php?title=Category:English_football_logos&filefrom=Swindon+town+fc+badge+1990.PNG'
        ]

wiki = "https://en.m.wikipedia.org/wiki/"

def get_club_name(string):
    name = string[5:len(string)]
    name = name.replace(".", "")
    retName = name[0:len(name)-7]
    return retName


for my_url in urls:
    all_links = []
    https = "https:"
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    
    page_soup = soup(page_html, "html.parser")
    containers = page_soup.findAll("div", {"class":"mw-category-group"})
    links = page_soup.select(".mw-category-group > ul > li > a")
    
    for link in links:
        new_link = "" + wiki + link.text
        new_link = new_link.replace(" ", "_")
        all_links.append(new_link)
        
    #Removing invalid links, those that can't be opened 
    if my_url == 'https://en.wikipedia.org/wiki/Category:English_football_logos':    
        all_links.pop(3)
        all_links.pop(65)
        all_links.pop(128)
        all_links.pop(129)
        all_links.pop(148)
    elif my_url == "https://en.wikipedia.org/w/index.php?title=Category:English_football_logos&filefrom=Chessington+%26+Hook+United+F.C.+logo.png#mw-category-media" : 
        print("Here I am")
        all_links.pop(109)
        all_links.pop(110)     
        all_links.pop(111)
        all_links.pop(112)
    elif my_url == 'https://en.wikipedia.org/w/index.php?title=Category:English_football_logos&filefrom=Swindon+town+fc+badge+1990.PNG':
        #fourth link contains invalid link   
        all_links.pop(1)
        print("We will remove something else.")
    #Checking if a link is valid

    counter = 0
    for link in all_links:
        uClient = uReq(all_links[counter])
        link_html = uClient.read()
        uClient.close()
    
        page_soup = soup(link_html, "html.parser")
        
        div = page_soup.find_all("div", {"class":"fullImageLink"})
        imgUrl = div[0].a['href']
        r = requests.get(""+https+imgUrl) # create HTTP response object
        
        name = links[counter].text
        nLen = len(name)-1
        extension = name[nLen-2] + name[nLen-1] + name[nLen] 
        
        clubName = get_club_name(name)
        
        with open("{}.{}".format(clubName, extension),'wb') as f:
            #write the contents of the response (r.content)
            # to a new file in binary mode.
            f.write(r.content)
            print("finished writing")
            
        counter+=1
    
