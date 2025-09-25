import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from agent import groq

# ### 1. Calling groq and printing response
# print(groq.calling_groq("generate terraform code for adding user in aws. GIVE ME ONLY HCL CODE"))

### 2. Calling with right prompt and showing audiance about file seggregation
prompt = """
Role: You are a terraform expert
Context: Expecting ONLY HCL CODE NOTHING ELSE
Requirement: Need your help to generate the terraform code 
Output: Can you please generate terraform code for creating one vpc with one ec2 server in public subnet
Ensure you are generating it in main.tf,variables.tf and output.tf files properly and ensure you are naming them as 
Example:**main.tf**,**variables.tf**,**output.tf**
NOTE: Don't include ``` in the output. 
"""

response = groq.calling_groq(prompt)


### 3. Parsing the data and storing data to files. Teach them how to get it done
from agent import dataparsing
print(dataparsing.contentparsing(response))