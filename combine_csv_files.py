###########################################
##Mark Fisher mark.aaron.fisher@gmail.com##
###########################################

####################################################################################################################################################################
##put all of the scraped csv files you want to combine in a single directory, change the dir_name and master_dir lines below accordingly, and this will combine them
####################################################################################################################################################################

import os
import csv
import re

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


dir_name="/Users/mf/2013_and_beyond/Discover_Life_PostDoc/Raw_data/Scraped_species_data/CAM/"
master_dir=os.listdir("/Users/mf/2013_and_beyond/Discover_Life_PostDoc/Raw_data/Scraped_species_data/CAM/")
#print master_dir

final_version=[]
##add header##
#print "master_dir[0]", master_dir[0]
a=open(dir_name+master_dir[1]).readlines()[0]
#print "a", a
final_version.append(a.split(','))
#print "final_version header", final_version

for f in master_dir:
    current_file=open(dir_name+f).readlines()
    for line in current_file[1:]:
        ##################################################################################################### 
        ##there were a few titles that had commas and numbers and other weirdness that had to be dealt with##
        #####################################################################################################
        line=re.sub(r'(\D),(\s\D)',r'\1_\2',line)#, count=1
        line=re.sub(r'(\d),(\s\d)',r'\1_\2',line)#, count=1
        #try:
#                xy=re.search(r'Cliniodes opalali(s,\s3)',line).group(1)
#                print "problem", line
#        except:
#                pass
        line=re.sub(r'(\D),(\s\d.*,[1,2][9,0])',r'\1_\2',line)#, count=1
        #print "line", line
        #print type(line)
        final_version.append(line.split(','))

#print "final_version at the end", final_version
saveCsv_v2(final_version, raw_input("File name? Don't forget .csv"), "/Users/mf/2013_and_beyond/Discover_Life_PostDoc/Raw_data/Scraped_species_data/Processed/")
