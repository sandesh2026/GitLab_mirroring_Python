import requests
import json
import csv


def get_gitlab_group_ids(access_token):
    return_array=[]
    url = "https://gitlab.com/api/v4/groups"
    payload={}
    headers = {
        'Private-Token': access_token,
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    response_dict = json.loads(response.text)
    if response.status_code == 200:
        response_dict = json.loads(response.text)
        for i in response_dict:
            t_hash = {}
            t_hash['id'] = i['id']
            t_hash['gitlab_group'] = i['name']
            return_array.append(t_hash)
        return True,return_array
    else:
        return False,"Something went wrong. Here's the status code we got"+str(response.status_code)

def get_gitlab_project_ids(access_token):
    #Return format
    #Array of dictonaries - each dict has the attributes "GitLab Project ID", "GitLab Path", "Project Name"
    #Exit Status
    (exit_code,group_objects) = get_gitlab_group_ids(access_token)
    if exit_code:
        return_array=[]
        for i in group_objects:
            url = "https://gitlab.com/api/v4/groups/"+str(i['id'])+"/projects"
            payload={}
            headers = {
                'Private-Token': access_token,
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                response_dict = json.loads(response.text)
                for j in response_dict:
                    t_hash = {}
                    t_hash['id'] = j['id']
                    t_hash['gitlab_group'] = j['namespace']['path']
                    t_hash['project_name'] = j['path']
                    return_array.append(t_hash)
            else:
                print("DEBUG: Something went wrong while getting the project id's. Here's the status code we got"+str(response.status_code)+" and the group object ID is "+str(i['id']))
                break
        return True, return_array
    else:
        print("DEBUG: Something went wrong while getting group_ids")

#Get a CSV with the ProjectID, Group, Name 
gitlab_access_token = '<GITLAB_TOKEN>'
(exit_code,pid_list) = get_gitlab_project_ids(gitlab_access_token)
print(pid_list)

with open('data_file.csv', mode='w') as data_file:
    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    data_writer.writerow(['GitLab Project ID', 'GitLab Group Name', 'GitLab Project Name'])
    for i in pid_list:
        data_writer.writerow([i['id'],i['gitlab_group'],i['project_name']])

