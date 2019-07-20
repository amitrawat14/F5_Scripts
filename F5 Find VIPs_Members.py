import requests, re, getpass
import requests.packages
import urllib3
import json

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {'content-type': 'application/json'}
username = 'username'
password = 'secret password'

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Enter you virtual server IP here.
virtual_server = '10.1.2.3'

url = 'https://10.x.x.x/mgmt/tm/ltm/virtual'
r = requests.get(url=url,headers=headers,auth=(username,password),verify=False)
json_load = r.json()
#print(json.dumps((json_load),indent=2))

Virtual_Server_List = []
for item in range(len(json_load['items'])):
    item = int(item)
    vs_ip = json_load['items'][item]['destination']
    vs_ip_partition= vs_ip.split('/')
    vs_ip = vs_ip_partition[2]
   
    
    vs_ip = vs_ip.split(":")
    vs_ip = vs_ip[0]
    Virtual_Server_List.append(vs_ip)
    
#print(Virtual_Server_List)
    
if virtual_server in Virtual_Server_List:
    x_ind = Virtual_Server_List.index(virtual_server)
    print(x_ind)
    vs_name = json_load['items'][x_ind]['name']
    vs_ip = json_load['items'][x_ind]['destination']
    vs_ip_partition= vs_ip.split('/')
    vs_ip = vs_ip_partition[2] 
    vs_partition = vs_ip_partition[1]
    vs_pool = json_load['items'][x_ind]['pool']
    vs_pool = vs_pool.split('/')
    vs_pool = vs_pool[2]
    print (f"Virtual Server Name is {vs_name}")
    print (f"Virtual Server IP {vs_ip}")
    print (f"Virtual Server is in {vs_partition} partition and Pool Name is {vs_pool}")
    
else:
    print ("Virtual IP Address don't exist")

print ("*****************************************************************\n\n")

url = 'https://10.25.254.200/mgmt/tm/ltm/pool'
pool = requests.get(url=url,headers=headers,auth=(username,password),verify=False)
pool_data = pool.json()

####### Finding Pool details to provide input for members details

Vs_Pool_List = []

for item in range(len(pool_data['items'])):
    #print (item)
    item = int(item)
    pool_name = pool_data['items'][item]['name']
    Vs_Pool_List.append(pool_name)
    #vs_ip_partition= vs_ip.split('/')
    #vs_ip = vs_ip_partition[2]
   
    
    vs_ip = vs_ip.split(":")
    vs_ip = vs_ip[0]
    Virtual_Server_List.append(vs_ip)


## Condition checking if Pool exist then provide member url link to get member details..


if vs_pool in Vs_Pool_List:
    pool_ind = Vs_Pool_List.index(vs_pool)
    pool_member = pool_data['items'][pool_ind]['membersReference']['link']
    host = pool_member.split('https://localhost')
    host[0] = '10.x.x.x'
    member_url = host[0]+host[1]
    member_url = (f'https://{member_url}')
    #print(member_url)    


else:
   print ("Pool don't exist")

#Member details.

m_data = requests.get(url=member_url,headers=headers,auth=(username,password),verify=False)
member_data = m_data.json()
#print(json.dumps((member_data),indent=2))
for item in range(len(member_data['items'])):
    member_name = member_data['items'][item]['name']
    member_ip = member_data['items'][item]['address']
    print (f"member name is {member_name} and ip address is {member_ip}")

print ("\n\n*****************************************************************")
