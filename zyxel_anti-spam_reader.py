import pandas as pd
import sys
import re
import time
import getopt
import os.path
"""
parser = argparse.ArgumentParser(description='Clean Zyxel Anti-spam log')
parser.add_argument("-i", dest="inputFilename", required=True,
                    help="CSV input file", metavar="inputFile.csv",
                    type=lambda x: is_valid_file(parser, x))
parser.add_argument("-o", dest="outputFilename", required=True,
                    help="CSV input file", metavar="outputFile.csv",
                    type=lambda x: is_valid_file(parser, x))
args = parser.parse_args()

"""

def parse_df_to_dict( df ):
   """Parse DataFrame to dict
   Keys : email, subject, status, logtime
   """
   dict_list = []
   logs = {}
   for index, row in df.iterrows():
      logs['email'] = re.findall(r'[\w\.-]+@[\w\.-]+', row['msg'])
      logs['subject'] = row['msg']
      logs['status'] = row['note']
      logs['logtime'] = row['logTime']
      dict_list.append(dict(logs))
   return dict_list

def write_csv (myLogs, outputFileName):
   """Convert dict to CSV format
   """
   file = open(outputFileName, "w")

   for index in range(len(myLogs)):
      # Convert list to string
      email = ''.join(myLogs[index]['email'])
      # Remove extra char of email adress
      email = email.translate(None, "[]'")
      # Drop left part of Subject
      subject = myLogs[index]['subject'].split("Subject: ", 1)[-1]
      #
      status = myLogs[index]['status']
      #
      logtime = myLogs[index]['logtime']
      line_str = "'" + email + "','" + subject + "','" + logtime + "','" + status + "'\n"
      if email and email.endswith(".ch") and status == 'MAIL DROP':
         #file.write(line_str.split(',')[0] + "\n")
         file.write(line_str)
   file.close()

# definition des variables
inputfile = ''
outputfile = ''
quietMode = False
argv = sys.argv[1:]
# recupere les argements passes au script
try:
    opts, args = getopt.getopt(argv,"hqi:o:",["ifile=","ofile=","quiet"])
except getopt.GetoptError:
    print 'zywall_anti-spam_reader.py -i <inputfile> -o <outputfile>'
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print 'zywall_anti-spam_reader.py -i <inputfile> -o <outputfile>'
        sys.exit()
    elif opt in ("-q", "--quiet"):
        quietMode = True
    elif opt in ("-i", "--ifile"):
        inputfile = arg
    elif opt in ("-o", "--ofile"):
        outputfile = arg

# check si les noms de fichiers d entree et de sortie ne soient pas vide
if inputfile =='' or outputfile == '':
    print 'zywall_anti-spam_reader.py -i <inputfile> -o <outputfile>'
    sys.exit()

# check si le fichier d entree existe
try:
    os.path.isfile(inputfile)

except:
    print("Fichier source introuvable !")
    sys.exit(0)

if quietMode is not True:
    sys.stdout.write("\r" + "Processing ... ")
    sys.stdout.flush()
# Set fields to use from CSV file
fields = ['msg', 'note', 'logTime']

# Extract DataFrame from input file
df = pd.read_csv(inputfile, usecols=fields)

# Convert Dataframe to dict
myLogs=parse_df_to_dict( df )

write_csv (myLogs, outputfile)
if quietMode is not True:
    sys.stdout.write("\r" + "Complete successfully !\n")
