from lxml.html import parse
from urllib2 import urlopen, Request
import os
import time
import os.path

def seperator():
    print  "----------------------------------------------"


def bountycheck(content):
        for ele in content:
                if ele[0] == "$" and ele[1:].isdigit():
                        return True
        return False
def main(companyName):

    if not os.path.exists(companyName):
        os.mkdir(companyName)
    
    for page in range(1, 10000):
        seperator()
        print "[*]  Parsing Page " + str(page)
        seperator()
        url = "https://hackerone.com/" + companyName.lower() + "?page=" + str(page)
        req = Request(url, None, headers)
        tree = parse(urlopen(req)).getroot()
        mydiv = tree.cssselect("div.hacktivity-container-subject-entry")
        if mydiv == []:
                return
        element = 0
        relevantElements = []
        listOne = []
        dates = []
        for x in mydiv:
            content = x.text_content().split()

            if "rewarded" in content:
                relevantElements.append(element)
                name = content[content.index("rewarded") + 1]
                url = ""
                if "for" in content:
					url = "https://hackerone.com" + x[3].attrib['href']
					vulnerablity= ' '.join(content[8:])
					#bounty= content[content.index("rewarded") + 4]
					listOne.append([name,url,vulnerablity])
            element += 1
        element = 0
        for y in tree.cssselect("a.hacktivity-timestamp-link"):
            if element not in relevantElements:
                element += 1
                continue
            for z in y:
                date = z.attrib['title']
                dates.append(" ".join(date.split()[:3]))
            element += 1
        blarg = 0
        for arr in listOne:
            with open(companyName + "\\" + companyName  + ".csv", "a") as myfile:
                myfile.write('"' + arr[0] + '"' + ',' + '"' + dates[blarg] + '"' + ',' + '"' + arr[1] + '"' + ','  + '"' + arr[2] + '"' + '\n')
            #print '"' + arr[0] + '"' + ','  + '"' + dates[blarg] + '"' + ',' + '"' + arr[1] + '"'  + ',' + '"' + arr[2] + '"'
            print 'Vulnerablity Name: "' + arr[2] + '"'
            print "Hunter: " + arr[0]
            print "Date: " + dates[blarg]
            print "URL: " + arr[1]
            #print "Bounty: " + arr[3]
            print "\n"
            blarg += 1
headers = { 'User-Agent' : 'Mozilla/5.0' }


if __name__=="__main__":
    try:
        companyName = raw_input("Company Name: ")
        path=companyName + "\\" + companyName  + ".csv"
        if os.path.isfile(path): 
            f=open(companyName + "\\" + companyName  + ".csv", "w+")
            f.close
        main(companyName)

        print "\n\nDone"
        print "\n Data saved in CSV file, open it with your favorite Text Editor"
    except KeyboardInterrupt:
        print "[*] Stopping"
        time.sleep(1)
        pass
