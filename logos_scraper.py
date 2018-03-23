from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as  uReq
import requests
import urllib.parse

urls = [#'https://en.wikipedia.org/wiki/Category:English_football_logos',
        #'https://en.wikipedia.org/w/index.php?title=Category:English_football_logos&filefrom=Chessington+%26+Hook+United+F.C.+logo.png#mw-category-media'
        #'https://en.wikipedia.org/w/index.php?title=Category:English_football_logos&filefrom=Hayling+United+logo.png#mw-category-media',
        #'https://en.wikipedia.org/w/index.php?title=Category:English_football_logos&filefrom=Norton-United-Logo.png#mw-category-media',
        #'https://en.wikipedia.org/w/index.php?title=Category:English_football_logos&filefrom=Swindon+town+fc+badge+1990.PNG'
        #'https://en.wikipedia.org/wiki/Category:Australian_soccer_logos',
        #'https://en.wikipedia.org/w/index.php?title=Category:Australian_soccer_logos&filefrom=South+Hobart+FC.png#mw-category-media'
        #'https://en.wikipedia.org/wiki/Category:Welsh_football_logos',
        #'https://en.wikipedia.org/wiki/Category:Scottish_football_logos',
        #'https://en.wikipedia.org/wiki/Category:Spanish_football_logos',
        #'https://en.wikipedia.org/w/index.php?title=Category:Spanish_football_logos&filefrom=CD+Masnou.png',#mw-category-media
        #'https://en.wikipedia.org/w/index.php?title=Category:Spanish_football_logos&filefrom=Lleida+Esportiu.svg',
        #'https://en.wikipedia.org/w/index.php?title=Category:Spanish_football_logos&filefrom=UE+Lleida+escudo.png#mw-category-media',
        #'https://en.wikipedia.org/wiki/Category:Northern_Irish_football_logos',
        #'https://en.wikipedia.org/wiki/Category:German_football_logos',
        #'https://en.wikipedia.org/w/index.php?title=Category:German_football_logos&filefrom=Danzig%2C+BuEV%0ABuEV+Danzig.png#mw-category-media'
        #'https://en.wikipedia.org/w/index.php?title=Category:German_football_logos&filefrom=Kastel%2C+FVgg%0AFVgg+Kastel.png#mw-category-media',
        #'https://en.wikipedia.org/w/index.php?title=Category:German_football_logos&filefrom=SpVgg+05+Bad+Homburg.gif#mw-category-media'
        #'https://en.wikipedia.org/wiki/Category:Italian_football_logos',
        #'https://en.wikipedia.org/w/index.php?title=Category:Italian_football_logos&filefrom=Modena+FC+logo.svg',
        #'https://en.wikipedia.org/wiki/Category:French_football_logos',
        #'https://en.wikipedia.org/wiki/Category:Portuguese_football_logos',
        #'https://en.wikipedia.org/w/index.php?title=Category:Brazilian_football_logos&filefrom=Real+Desportivo+Ariquemes+Futebol+Clube.png#mw-category-media',
        #'https://en.wikipedia.org/wiki/Category:Czech_football_logos',
        #'https://en.wikipedia.org/wiki/Category:Dutch_football_logos',
        #'https://en.wikipedia.org/wiki/Category:American_soccer_logos',
        #'https://en.wikipedia.org/wiki/Category:Russian_football_logos',
        #'https://en.wikipedia.org/wiki/Category:Mexican_football_logos',
        #'https://en.wikipedia.org/wiki/Category:Norwegian_football_logos',
        #'https://en.wikipedia.org/wiki/Category:Swedish_football_logos',
        #'https://en.wikipedia.org/wiki/Category:Slovak_football_logos',
        #'https://en.wikipedia.org/wiki/Category:Slovenian_football_logos',
        #'https://en.wikipedia.org/wiki/Category:Swiss_football_logos',
        #'https://en.wikipedia.org/wiki/Category:Polish_football_logos',
        #'https://en.wikipedia.org/wiki/Category:Serbian_football_logos',
        #'https://en.wikipedia.org/wiki/Category:Thai_football_logos',
        #'https://en.wikipedia.org/wiki/Category:Peruvian_football_logos',
        'https://en.wikipedia.org/wiki/Category:Greek_football_logos'
        ]

wiki = "https://en.m.wikipedia.org/wiki/"


print("itsok")

def get_club_name(string):
    name = string[5:len(string)]
    name = name.replace(".", "")
    retName = name[0:len(name)-7]
    return retName


for my_url in urls:
    all_links = []
    #data = data.encode('utf-8') # data should be bytes
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
                
                
    counter = 0
    for link in all_links:
       # print(all_links[counter])
        url = all_links[counter]
        url = urllib.parse.urlsplit(url)
        url = list(url)
        url[2] = urllib.parse.quote(url[2])
        url = urllib.parse.urlunsplit(url)
        uClient = uReq(url)
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
            
        print(counter)
        counter+=1
