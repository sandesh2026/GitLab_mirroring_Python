import requests
import json
import csv

def get_all_owned_project_id(access_token):
    #Return format
    #Array of dictonaries - each dict has the attributes "GitLab Project ID", "GitLab Path", "Project Name"
    #Exit Status
    return_array=[]
    url = "https://gitlab.com/api/v4/projects?owned=true"
    payload={}
    headers = {
    'Private-Token': access_token,
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        response_dict = json.loads(response.text)
        for i in response_dict:
            t_hash = {}
            t_hash['id'] = i['id']
            t_hash['gitlab_group'] = i['namespace']['path']
            t_hash['project_name'] = i['path']
            return_array.append(t_hash)
        return True,return_array
    else:
        return False,"Something went wrong. Here's the status code we got"+str(response.status_code)

#Get a CSV with the ProjectID, Group, Name 
gitlab_access_token = '<GITLAB_API_TOKEN>'
(exit_code,pid_list) = get_all_owned_project_id(gitlab_access_token)

with open('data_file.csv', mode='w') as data_file:
    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    data_writer.writerow(['GitLab Project ID', 'GitLab Group Name', 'GitLab Project Name'])
    for i in pid_list:
        data_writer.writerow([i['id'],i['gitlab_group'],i['project_name']])

