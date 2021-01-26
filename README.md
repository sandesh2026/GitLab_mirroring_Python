### Dependencies:
  Python3, requests, json, csv
  
### Procedure
1. Clone the repo to your local
2. Create `tokens.csv` with this structure - `GitLab Access Token`, `GitHub Access Token`, `GitHub Username`. NOTE: GitHub Username here should be of the admin of the GitHub Org
3. Run the `1_get_gl_project_id.py` and it'll generate a CSV - `data_file.csv` with these fields - "GitLab Group ID", "GitLab Group Name", "GitHub Project ID", "GitLab Project Name"
4. Open `data_file.csv` and add a new column "GitHub Org" and add the GitHub Org to every row :man_shrugging:
5. Run the `2_mirror_setup.py` next - here's what it does:

  (It assumes that the GitLab and GitHub repo names are same)
  
    5.1: Reads the CSV file you saved just now
    5.2: Instantiates an object for each row
    5.3: Checks if the repo exists in GitHub, if yes - sets up the mirror
    5.4: If the repo doesn't exist - it creates the repo for the Org you specified in the CSV file and then sets up the mirror

6. Spot check a few Projects in GitLab and see if the mirror is setup
7. TODO: The Update should happen once every hour or so (confirm!), if not a force update through the API could be done (for Paid plans); or maybe a dummy commit
