###########################################
##Mark Fisher mark.aaron.fisher@gmail.com##
###########################################


import re
import urllib
import csv

#######################################################
##some modules for saving lists of lists as csv files##
#######################################################

def saveCsv(cols, filename, destination_directory):
        savefile=destination_directory
        savefile+=filename
        ofile=open(savefile, "wb")
        writer=csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)
        for row in cols:
                #print row
                #print cols.index(row)
                writer.writerow(row) #if it throws an escapechar error, inspect the spreadsheet for weird characters such as ,;*-
                #ofile.writelines(row)
        ofile.close()

def saveCsv_v2(cols, filename, destination_directory):
        savefile=destination_directory
        savefile+=filename
        ofile=open(savefile, "wb")
        writer=csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in cols:
                #rint row
                #print cols.index(row)
                writer.writerow(row) #if it throws an escapechar error, inspect the spreadsheet for weird characters such as ,;*-
                #ofile.writelines(row)
        ofile.close()

################################
##get some input from the user##
################################
        
ID=raw_input("Please enter your album ID (e.g., I_MFS)")
master_query=raw_input("Please enter the species or title you're looking for (e.g., moth). Otherwise, enter 'NONE'.")
link_q=re.compile(r'<img\ssrc="/mp/20p\?res=80&img=(.*)"\sh.*') #link_q=re.compile(r'<img\ssrc="(//mp/20p/?res=80/&img=I_MF.*)"')
page_1=int(raw_input("What's the first page of your album that you want to look at (e.g., enter 0 for 0000)?"))
page_last=int(raw_input("What's the last page of your album that you want to look at (e.g., enter 44 for 0044)?"))
notes_answer=raw_input("Will ALL of the images you're looking at contain notes? y/n")

##################################################
##turn the page range into an array called pages##
##################################################

pages=[]
for x in range(page_1,page_last+1):
    #print "x", x
    if len(str(x))==1:
        pages.append('000'+str(x))
    elif len(str(x))==2:
        pages.append('00'+str(x))
    elif len(str(x))==3:
        pages.append('0'+str(x))
    elif len(str(x))==4:
        pages.append(str(x))
    else:
        print "You must have entered a number >9999"
#print "pages", pages

#################################
##frame the final list of lists##
#################################
        
title_and_date=[['Picture_title','Date','Location','Album_page', 'Picture_number','Notes']]

###########################################################
##scrape through each album page designated by user input##
###########################################################

for entry in pages:
    print "album being scraped:", entry
    #print "site scraped:", "http://www.discoverlife.org/mp/20p?see="+ID+"/"+entry
    master_file=urllib.urlopen("http://www.discoverlife.org/mp/20p?see="+ID+"/"+entry)
    #print "master_file", master_file
    master_text=master_file.readlines()
    all_links=[]
    for line in master_text:
        #print "line", line
        try:
            l=re.search(link_q,line).group(1)
            all_links.append(l)
        except:
            pass

    #print "all links", all_links

    if master_query not in ['NONE','none','None']:
        title_q1=re.compile(r'<td>('+master_query+r')</td>')#"+master_query+"</td>")
    else:
        title_q=re.compile(r'<html><head><title>(.*)\simage</title>')#I'll have to figure out how to look for something in the previous line using regex
    date_q=re.compile(r'<td>(20.*)</td>')
    location_q=re.compile(r'<td>(\w.*)</td></tr>')
    notes_q=re.compile(r'<td>(\w.*)</td></tr>')

###################################################################################################################
##now that you've got a list of each of the images, scrape through each of those and extract relevant information##
###################################################################################################################

    for pic in all_links:
        #print "i", i
        print "pic", pic
        #print "http://www.discoverlife.org"+pic
        sub_htmlfile=urllib.urlopen("http://www.discoverlife.org/mp/20p?see="+pic+"&res=640") #http://www.discoverlife.org/mp/20p?see=I_MFS2&res=640
        #print "sub_htmlfile", sub_htmlfile
        sub_file_text=sub_htmlfile.readlines()
        for i, l in enumerate(sub_file_text):
            #print "line", l
            try:
                if master_query in ['NONE','none','None']:
                    #print "Entered standard"
                    title=re.search(title_q,l).group(1)#.replace("-","_")
                    #print "title worked", title
                else:
                    #print "Entered alt"
                    title=re.search(title_q1,l).group(1)#.replace("-","_")
                    #print "title alt worked", title
            except:
                pass
            try:
                if re.match("<tr><td><b>site/street/trail</b></td>",l):
                    #print "found a match here", l
                    #print "found a match two above"
                    #print "sub_file_text[i+1]", sub_file_text[i+1]
                    location=re.search(location_q,sub_file_text[i+1]).group(1)
                    #print "location", location
            except:
                pass
            if notes_answer in ['y','Y','yes','Yes','YES']:
                    try:
                        date=re.search(date_q,l).group(1)
                        #print "date worked with notes", date

                    except:
                        pass
                    try:
                        if re.match("<tr><td><b>notes</b></td>",l):
                            notes=re.search(notes_q,sub_file_text[i+1]).group(1)
                            #print "notes", notes
                            if title and date and location:
                                    title_and_date.append([title,date, location, entry, pic,notes])
                            title=""
                            date=""
                            location=""
                    except:
                            pass
            else:
                    try:
                            date=re.search(date_q,l).group(1)
                            if title and date and location:
                                    title_and_date.append([title,date, location, entry, pic,'NA'])
                            title=""
                            date=""
                            location=""
                            #print "date worked without notes", date

                    except:
                            pass

#######################
##now save the output##
#######################
                        
#print "title_and_date", title_and_date
saveCsv_v2(title_and_date, raw_input("What do you want to call the output file (e.g. save.csv)?"), raw_input("Where do you want to save (e.g., '/Users/mf/Desktop/')?"))
            
