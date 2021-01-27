Can this script be done better? For sure. I wrote it really quick over a weekend :joy: 

### Dependencies:
I used these. 
  1. `Python3` 
  2. `requests`module for firing off API calls 
  3. `json` module for playing with JSON responses 
  4. `csv` cuz enterprises love Excel!
  5. Connectivity to `*.github.com`, `*.gitlab.com`
  
### TL:DR;
#### There are two programs here. Here's how the high level approach looks like:
1. Run the first script
2. Input data into the first scripts output
3. Run the second script!

  
### Procedure
1. Clone the repo to your local
2. :exclamation:Action Required:exclamation: Create a file called `tokens.csv` with this structure - `GitLab Access Token`, `GitHub Access Token`, `GitHub Username`. NOTE: GitHub Username here should be of the admin of the GitHub Org
3. Run the `1_get_gl_project_id.py` and it'll generate a CSV - `data_file.csv` in your local system with these fields - "GitLab Group ID", "GitLab Group Name", "GitHub Project ID", "GitLab Project Name"
4. :exclamation:Action Required:exclamation: Open `data_file.csv` and add a new column "GitHub Org" and add the GitHub Org to every row. If you want to limit the number of repos that will be mirrored, feel free to delete lines from this file. Basically, - whatever is in the `data_file.csv` will be used by the :point_down: script 
5. Run the `2_mirror_setup.py` next - here's what it does:
  (It assumes that the GitLab and GitHub repo names are same)
    ```
    5.1: Reads the CSV file you saved just now (`data_file.csv`)
    5.2: Instantiates an object for each row
    5.3: Checks if the repo exists in GitHub, if yes - sets up the mirror
    5.4: If the repo doesn't exist - it creates the repo for the Org you specified in the CSV file and then sets up the mirror
    ```
6. Spot check a few Projects in GitLab and see if the mirror is setup
7. TODO: The remote mirror update doesnt happen automatically. ~So a force update through the API could be done (for Paid plans); or maybe a dummy commit~ No APIs available to do this :( . We will instead use Tags. Creation of a tag would trigger a force update.
