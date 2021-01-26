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

def add_remote(github_access_token, gitlab_access_token, mirror_object, github_username):
    url="https://gitlab.com/api/v4/projects/"+mirror_object['GitLab Project ID']+"/remote_mirrors?enabled=true"
    payload = {
        "url":"https://"+github_username+":"+github_access_token+"@github.com/"+mirror_object['GitHub Org']+"/"+mirror_object['GitLab Project Name']+".git"
    }
    headers = {
        'Private-Token': gitlab_access_token,
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code >=200 and response.status_code<300:
        print("Mapped "+mirror_object['GitLab Group Name']+"/"+mirror_object['GitLab Project Name']+" with "+mirror_object['GitHub Org']+"/"+mirror_object['GitLab Project Name'])
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

def does_gitlab_mirror_exist(gitlab_access_token,mirror_object,github_username):
    url = "https://gitlab.com/api/v4/projects/"+mirror_object['GitLab Project ID']+"/remote_mirrors"
    payload={}
    headers = {
        'Private-Token': gitlab_access_token,
    }
    github_repo = mirror_object['GitHub Org']+"/"+mirror_object['GitLab Project Name']+".git"
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        response_dict = json.loads(response.text)
        for i in response_dict:
            if github_repo.lower() in i['url'].lower() and i['enabled']:
                return True
        else:
            return False
    else:
        print("DEBUG: Error getting remote mirror details"+str)

creds = read_csv_file("tokens.csv").pop(0)
gitlab_access_token = creds['GitLab Access Token']
github_access_token = creds['GitHub Access Token']
github_username = creds['GitHub Username']
data_objects=read_csv_file("data_file.csv")
for i in data_objects:
    if does_github_repo_exist(github_access_token,i['GitHub Org'],i['GitLab Project Name']):
        i['GitHub exists'] = True
        if not does_gitlab_mirror_exist(gitlab_access_token,i,github_username):
            if add_remote(github_access_token,gitlab_access_token,i,github_username):
                print("Successfully added mapping for "+str(i['GitLab Group Name'])+"/"+str(i['GitLab Project Name'])+"---> GitHub:"+str(i['GitHub Org'])+"/"+str(i['GitLab Project Name']))
            else:
                print("FAILED TO MAP - "+str(i['GitLab Group Name'])+"/"+str(i['GitLab Project Name'])+"---> GitHub:"+str(i['GitHub Org'])+"/"+str(i['GitLab Project Name']))
        else:
            print("Mapping of GitLab: "+str(i['GitLab Group Name'])+"/"+str(i['GitLab Project Name'])+"---> GitHub:"+str(i['GitHub Org'])+"/"+str(i['GitLab Project Name'])+" already exists! Skipping this!")
    else:
        i['GitHub exists'] = False
        if create_github_repo(github_access_token,i):
            if add_remote(github_access_token,i['GitHub Org'],i,github_username):
                print("Successfully added mapping for "+str(i['GitLab Group Name'])+"/"+str(i['GitLab Project Name'])+"---> GitHub:"+str(i['GitHub Org'])+"/"+str(i['GitLab Project Name']))
            else:
                print("FAILED TO MAP - "+str(i['GitLab Group Name'])+"/"+str(i['GitLab Project Name'])+"---> GitHub:"+str(i['GitHub Org'])+"/"+str(i['GitLab Project Name']))
        else:
            print("DEBUG: Error in creating the repo. Check the data_file.csv")
