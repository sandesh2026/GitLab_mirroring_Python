import requests
import json
import csv

def does_github_repo_exist(access_token,org_name,repo_name):
    payload={}
    url = "https://api.github.com/repos/"+org_name+"/"+repo_name
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': 'token '+access_token
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        return True
    else:
        return False

def read_csv_file(data_file):
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

def add_remote(github_access_token, gitlab_access_token, mirror_object, username):
    url="https://gitlab.com/api/v4/projects/"+mirror_object['GitLab Project ID']+"/remote_mirrors?enabled=true"
    payload = {
        "url":"https://"+username+":"+github_access_token+"@github.com/"+mirror_object['GitHub Org']+"/"+mirror_object['GitLab Project Name']+".git"
    }
    headers = {
        'Private-Token': gitlab_access_token,
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        return True
    else:
        return False

def create_github_repo(github_access_token,mirror_object):
    url="https://api.github.com/orgs/"+mirror_object['GitHub Org']+"/repos"
    #print(url)
    payload={}
    payload={
        "name":mirror_object['GitLab Project Name'],
        "private":"true"
    }
    print(payload)
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': 'token '+github_access_token
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    if response.status_code == 200:
        return True
    else:
        return False

gitlab_access_token = '<GITLAB_API_TOKEN>'
github_access_token = "<GITHUB_PAT>"
username="preacherlemon"
data_file = "data_file.csv"
data_objects=read_csv_file(data_file)
for i in data_objects:
    if does_github_repo_exist(github_access_token,i['GitHub Org'],i['GitLab Project Name']):
        i['GitHub exists'] = True
        print("Repo Exists")
        add_remote(github_access_token,gitlab_access_token,i,username)
    else:
        i['GitHub exists'] = False
        print("Repo doesn't exist")
        create_github_repo(github_access_token,i)
        add_remote(github_access_token,i['GitHub Org'],i,username)