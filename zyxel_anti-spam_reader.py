import pandas as pd
import sys
import re
import time
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
      if email and email.endswith(".ch"):
         file.write(line_str)
   file.close() 

# Set output file name
output_csv_file = sys.argv[2]

# Set fields to use from CSV file
fields = ['msg', 'note', 'logTime']

# Extract DataFrame from CSV file 
df = pd.read_csv(sys.argv[1], usecols=fields)

# Convert Dataframe to dict
myLogs=parse_df_to_dict( df )

write_csv (myLogs, output_csv_file)