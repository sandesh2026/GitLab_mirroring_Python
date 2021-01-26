import requests
import json
import csv


def get_gitlab_group_ids(access_token):
    # This module is designed to 
    # 1. list out all groups accessible to the token user
    # 2. Parse the payload and construct an array of hashes with fields - GroupID, Group Name
    # RETURNS: Exit Code, Array
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
    # This module is designed to 
    # 1. for each GroupID we got from get_gitlab_group_ids, we find out every project hosted within it and the Project IDs
    # 2. Parse the payload and construct an array of hashes with fields - ProjectID, GitLabGroup, GitLabProject, GitLab Group ID
    # RETURNS: Exit Code, Array
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
                    t_hash['gitlab_project_id'] = j['id']
                    t_hash['gitlab_group_name'] = j['namespace']['path']
                    t_hash['gitlab_group_id'] = i['id']
                    t_hash['gitlab_project_name'] = j['path']
                    return_array.append(t_hash)
            else:
                print("DEBUG: Something went wrong while getting the project id's. Here's the status code we got"+str(response.status_code)+" and the group object ID is "+str(i['id']))
                break
        return True, return_array
    else:
        print("DEBUG: Something went wrong while getting group_ids")

def read_csv_file(data_file):
    #Reads a CSV and returns an array of hashes for every row
    #For example:
    #   Col1    |   Col2    |   Col3
    #-----------|-----------|--------
    #   Val1    |   Val2    |   Val3    
    #   Val4    |   Val5    |   Val6 
    #Would return this:
    # [ 
    #   {"Col1":"Val1", "Col2":"Val2", "Col3":"Val3"},
    #   {"Col1":"Val4", "Col2":"Val5", "Col3":"Val6"}
    # ]

    return_array = []
    with open(data_file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count=line_count+1
            return_array.append(row)
            line_count = line_count+1
    return return_array

#Get a CSV with the ProjectID, Group, Name 
creds = read_csv_file("tokens.csv").pop(0)
gitlab_access_token = creds['GitLab Access Token']
(exit_code,pid_list) = get_gitlab_project_ids(gitlab_access_token)

with open('data_file.csv', mode='w') as data_file:
    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    data_writer.writerow(['GitLab Group ID', 'GitLab Group Name', 'GitLab Project ID', 'GitLab Project Name'])
    for i in pid_list:
        data_writer.writerow([i['gitlab_group_id'],i['gitlab_group_name'],i['gitlab_project_id'],i['gitlab_project_name']])

