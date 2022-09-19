from logging.config import valid_ident
import re
from urllib.parse import urljoin
import asyncio
from xml.etree.ElementInclude import include
import aiohttp
import requests
from aiohttp.client import ClientSession
import sys
from bs4 import BeautifulSoup
import subprocess
class colors:

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


print(colors.OKGREEN,colors.BOLD,"""
 
░█████╗░██████╗░██████╗░██╗░██████╗██╗░░██╗██╗░░░██╗░█████╗░
██╔══██╗██╔══██╗██╔══██╗██║██╔════╝██║░░██║╚██╗░██╔╝██╔══██╗
███████║██║░░██║██████╔╝██║╚█████╗░███████║░╚████╔╝░███████║
██╔══██║██║░░██║██╔══██╗██║░╚═══██╗██╔══██║░░╚██╔╝░░██╔══██║
██║░░██║██████╔╝██║░░██║██║██████╔╝██║░░██║░░░██║░░░██║░░██║
╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝╚═╝╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝

███████████████████████████████████
█─▄▄▄▄█▄─▄▄─█▄─▄█▄─▄▄▀█▄─▄▄─█▄─▄▄▀█
█▄▄▄▄─██─▄▄▄██─███─██─██─▄█▀██─▄─▄█
▀▄▄▄▄▄▀▄▄▄▀▀▀▄▄▄▀▄▄▄▄▀▀▄▄▄▄▄▀▄▄▀▄▄▀

                                               @kartikhunt3r


""",colors.ENDC)


target = input(colors.HEADER+colors.BOLD+"Enter Target URL: "+colors.ENDC)
if not target.startswith("http://") and not target.startswith("https://"):
    target="http://"+target

if target.endswith("/"):
    target=target[:-1]
print(colors.OKCYAN+colors.BOLD+"[+] Target: "+target+colors.ENDC)

try:
    requests.get(target)
except Exception as e:
    print(colors.FAIL+colors.BOLD+"Please Enter A Valid URL ex:https://example.com")
    sys.exit()

x = target.split("/")
y=x[2]
subprocess.call("mkdir "+y,shell=True)

invalid=True

while invalid:
    externals=input(colors.WARNING+colors.BOLD+"Do you Want to include External third Party Links?[Y/N]: ")
    if externals == "Y" or externals == "y" or externals == "N" or externals == "n":
        invalid=False
    else:
        print(colors.FAIL+colors.BOLD+"Please Answer In Y/N")

wayinvalid=True

while wayinvalid:
    waybacks=input(colors.WARNING+colors.BOLD+"Do you Want to include Way Back Urls?[Y/N]: ")
    if waybacks == "Y" or waybacks == "y" or waybacks == "N" or waybacks == "n":
        wayinvalid=False
    else:
        print(colors.FAIL+colors.BOLD+"Please Answer In Y/N")

target_url=[]
target_links = []
temp_links=[]
target_js=[]
target_form=[]
target_robo=[]
target_sitemaps=[]
ginti=[]
target_url.append(target)
target_url.append(target+"/sitemap.xml")
target_url.append(target+"/robots.txt")




async def link_extractor(url,session:ClientSession):
    async with session.get(url) as response:
        result = await response.text()
        href_links= re.findall('(?:href=")(.*?)"',str(result)) + re.findall("(?:href=')(.*?)'",str(result))
        js_links= re.findall('(?:src=")(.*?)"',str(result)) + re.findall("(?:src=')(.*?)'",str(result))
        form_links= re.findall('(?:action=")(.*?)"',str(result)) + re.findall("(?:action=')(.*?)'",str(result))
        xml_links= re.findall('(?:<loc>)(.*?)</loc>',str(result))
        robo_links= re.findall('(?:Disallow: )(.*?)\n',str(result))+re.findall('(?:Allow: )(.*?)\n',str(result))+re.findall('(?:sitemap: )(.*?)\n',str(result))


        for link in href_links:
            link = urljoin(url,link)
            # if "#" in link:
            #     link = link.split("#")[0]
            
            if target in link and link not in target_links:              
                temp_links.append(link)

            if externals=="y" or externals=="Y":

                if link not in target_links:
                    print(colors.OKGREEN+colors.BOLD+"[+] Link: "+link+colors.ENDC)
                    target_links.append(link)
                    ginti.append("[+] Link: "+link)
            
            elif externals=="n" or externals=="N":

                if target in link and link not in target_links:
                    print(colors.OKGREEN+colors.BOLD+"[+] Link: "+link+colors.ENDC)
                    target_links.append(link)
                    ginti.append("[+] Link: "+link)


            
        for limk in js_links:

            limk = urljoin(url,limk)
            
            if target in limk and limk not in target_js and limk.endswith(".json"):          
                temp_links.append(limk)

            if externals == "Y" or externals == "y":
                if limk not in target_js and limk.endswith(".js"):
                    target_js.append(limk)
                    print(colors.OKBLUE+colors.BOLD+"[+] JS file: "+limk+colors.ENDC)
                    ginti.append("[+] JS file: "+limk)
                elif limk not in target_js and limk not in target_form and limk not in target_links:
                    target_js.append(limk)
                    print(colors.OKGREEN+colors.BOLD+"[+] Link: "+limk+colors.ENDC)
                    ginti.append("[+] Link: "+limk)


            elif externals == "N" or externals == "n":
                if target in limk and limk not in target_js and limk.endswith(".js"):
                    target_js.append(limk)
                    print(colors.OKBLUE+colors.BOLD+"[+] JS file: "+limk+colors.ENDC)
                    ginti.append("[+] JS file: "+limk)
                elif target in limk and limk not in target_js and limk not in target_form and limk not in target_links:
                    target_js.append(limk)
                    print(colors.OKGREEN+colors.BOLD+"[+] Link: "+limk+colors.ENDC)
                    ginti.append("[+] Link: "+limk)
                    
        for limk in form_links:

            limk = urljoin(url,limk)

            if target in limk and limk not in target_form:              
                temp_links.append(limk)

            if externals == "Y" or externals == "y":
                if limk not in target_form:
                    target_form.append(limk)
                    print(colors.HEADER+colors.BOLD+"[+] Form: "+limk+colors.ENDC)
                    ginti.append("[+] Form: "+limk)
            
            elif externals == "N" or externals == "n":
                if target in limk and limk not in target_form:
                    target_form.append(limk)
                    print(colors.HEADER+colors.BOLD+"[+] Form: "+limk+colors.ENDC)
                    ginti.append("[+] Form: "+limk)
                    
        for limk in xml_links:

            limk = urljoin(url,limk)

            if externals == "Y" or externals == "y":
                if limk not in target_form:
                    target_form.append(limk)
                    print(colors.WARNING+colors.BOLD+"[+] Sitemap-Results: "+limk+colors.ENDC)
                    ginti.append("[+] Sitemap-Results: "+limk)
            
            elif externals == "N" or externals == "n":
                if target in limk and limk not in target_form:
                    target_form.append(limk)
                    print(colors.WARNING+colors.BOLD+"[+] Sitemap-Results: "+limk+colors.ENDC)
                    ginti.append("[+] Sitemap-Results: "+limk)
        
        
        
        for limk in robo_links:

            limk = urljoin(url,limk)

            if externals == "Y" or externals == "y":
                if limk not in target_robo:
                    target_robo.append(limk)
                    print(colors.OKCYAN+colors.BOLD+"[+] ROBOTS.TXT-Results: "+limk+colors.ENDC)
                    ginti.append("[+] ROBOTS.TXT-Results: "+limk)
            
            elif externals == "N" or externals == "n":
                if target in limk and limk not in target_robo:
                    target_robo.append(limk)
                    print(colors.OKCYAN+colors.BOLD+"[+] ROBOTS.TXT-Results: "+limk+colors.ENDC)
                    ginti.append("[+] ROBOTS.TXT-Results: "+limk)


                





async def crawl(urls):
    rocky=[]
    for i in urls:
        rocky.append(i)
    temp_links.clear()
    my_conn = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=my_conn) as session:
        tasks = []
        for url in rocky:
            task = asyncio.ensure_future(link_extractor(url=url,session=session))
            tasks.append(task)
        await asyncio.gather(*tasks,return_exceptions=True) # the await must be nest inside of the session

asyncio.run(crawl(target_url))

while True:
    try:
        asyncio.run(crawl(temp_links))
        if len(temp_links)<=0:
            print(colors.HEADER+colors.BOLD+"Finding Wayback Results ...")
            with open(y+'/results.txt', 'a') as the_file:
                for link in ginti:
                    the_file.write(link+'\n')
            if waybacks=="Y" or waybacks=="y":
                    url = 'http://web.archive.org/cdx/search/cdx?url=*.'+target+'/*&output=txt&fl=original&collapse=urlkey'
                    r = requests.get(url)
                    results = r.text
                    print(colors.OKBLUE+colors.BOLD+"------------- [+] Way Back Result ------------")
                    print (results)
                    with open(y+'/wayback.txt', 'a') as the_file:
                        the_file.write(results)
                        the_file.close()
            print(colors.HEADER+colors.BOLD+"[+] Done")
            print(colors.OKCYAN+colors.BOLD+"[+] Total Discoveries: "+(str(len(ginti))))
            sys.exit()
    except KeyboardInterrupt:
        print(colors.HEADER+colors.BOLD+"Finding Wayback Results ...")
        with open(y+'/results.txt', 'a') as the_file:
                for link in ginti:
                    the_file.write(link+'\n')
        if waybacks=="Y" or waybacks=="y":
            url = 'http://web.archive.org/cdx/search/cdx?url=*.'+target+'/*&output=txt&fl=original&collapse=urlkey'
            r = requests.get(url)
            results = r.text
            print(colors.OKBLUE+colors.BOLD+"------------- [+] Way Back Result ------------")
            print (results)
            with open(y+'/wayback.txt', 'a') as the_file:
                the_file.write(results)
                the_file.close()
        print(colors.FAIL+colors.BOLD+"[!] Scan Aborted By User.")
        print(colors.OKCYAN+colors.BOLD+"[+] Total Discoveries: "+str(len(ginti)))
        sys.exit()
