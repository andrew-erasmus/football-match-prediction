import pandas as pd
import requests
from bs4 import BeautifulSoup
pd.set_option('display.max_rows', None)
from IPython.display import display
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

# Steps: 
# 1- Web scrape to collect data 
# 2- Machine learning models to predict results on data that was scraped
# 3- Evaluation of detection models
# 4- Displaying of information

data_source={
    '1':'https://fbref.com/en/comps/9/Premier-League-Stats', # premier league fixtures
    '2':'https://fbref.com/en/comps/12/La-Liga-Stats', # la liga fixtures
    '3':'https://fbref.com/en/comps/11/Serie-A-Stats', # serie a fixtures
    '4':'https://fbref.com/en/comps/20/Bundesliga-Stats', # bundesliga fixtures
    '5':'https://fbref.com/en/comps/13/Ligue-1-Stats', # ligue 1 fixtures
    '6':'https://fbref.com/en/comps/32/Primeira-Liga-Stats', # primeira liga fixtures
    '7':'https://fbref.com/en/comps/8/Champions-League-Stats', # champions league fixtures
    '8':'https://fbref.com/en/comps/19/Europa-League-Stats' # europa league fixtures
    }

# holding place function for the prediction of the score
def scrape_data(comp, team1, team2):
    
    url = data_source.get(comp) # get the correct URL from the dictionary
    
    # extract information for the matches using requests library
    data = requests.get(url)
    soup  = BeautifulSoup(data.text)
    
    # get the table of standings with all team information
    standings = soup.select('table.stats_table')[0]
    
    # find the anchor for all team stats
    links = standings.find_all('a')
    
    links = [l.get('href') for l in links]
    links =  [l for l in links if '/squads/' in l] # if squads is not in the link - get rid of it
    
    team_urls = [f"https://fbref.com{l}" for l in links] # formats the string to have absolute links
    
    # get team match information
    team_url = team_urls[0]
    data = requests.get(team_url) # get the data for the matches for 1 team
    
    matches = pd.read_html(data.text, match="Scores & Fixtures")
    
    # get information about shooting   
    soup = BeautifulSoup(data.text)
    links = soup.find_all('a') # find all links
    links = [l.get('href') for l in links] # get the actual url
    links = [l for l in links if l and 'all_comps/shooting/' in l] # get the shooting link
    
    data = requests.get(f"https://fbref.com{links[0]}") # get data from shootings
    
    shooting = pd.read_html(data.text, match="Shooting")[0] # get shooting information
    
    shooting.columns = shooting.columns.droplevel() # take away multilevel index - the first header
    
    # merge the match and shooting dataframes
    team_data = matches.merge(shooting[['Date', 'Sh', 'SoT','Dist', 'FK', 'PK','PKAtt']], on='Date')
    
    # prediction(name, team1, team2)
    
def prediction(name, team1, team2):
    
    # Read in the CSV with the match data
    match_data = pd.read_csv(f'{name}.csv', index_col=0)
    print(match_data)
    
    # Cleaning date data for processing
    match_data["date"] = pd.to_datetime(match_data["date"])
    
    # found_home = check_team(team1, match_data)
    # found_away = check_team(team2, match_data)
            
    # if found_home and found_away:
    #     print("Teams are valid")
    # else:
    #     print("Teams are invalid")
    
        
def check_team(team, output_df):
    # add error handling to search the array to see if the team is currently in the league
    found = False
    
    # Account for differences in file formatting
    if 'United' in team or 'united' in team:
        team = team.rstrip("United").strip()
        team = team +" Utd"
        
    for i in range(len(output_df)):
        # iterate through the dataframe
        home_team = output_df.iloc[i]['Home']
        away_team = output_df.iloc[i]['Away']
        
        # check if the team played in a certain game
        if (team == home_team) or (team == away_team):
            found = True
            break
            
    return found
            
        
# function that will get the name of the competition selected for formatting purposes
def get_comp_name(url):
    split_url = url.split('/')
    unformatted_name = split_url[-1].split('-')
    
    # account for difference in bundesliga name from URL
    name = unformatted_name[0]+" "+unformatted_name[1]
    if name == 'Bundesliga Scores':
        name = 'Bundesliga'
        
    return name
    
def main():
    print('---- Welcome to the football match score predictor! ----')
       
    competition = input('Please select a competition for the match up: (1-8)\n\n1. Premier League\n2. La Liga\n3. Serie A\n4. Bundesliga\n5. Ligue 1\n6. Primeira Liga\n7. Champions League\n8. Europa League\n--> ')
    choices = ['1', '2', '3', '4', '5', '6', '7', '8']
    while competition not in choices:
        competition = input('Invalid choice, please select again (1-8): ')
    
    team1 = input('Please enter the home team: ')
    team2 = input('Please enter the away team: ')
    
    scrape_data(competition, team1, team2)



if __name__ == '__main__':
    main()