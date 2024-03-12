import pandas as pd
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
    '1':'https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures', # premier league fixtures
    '2':'https://fbref.com/en/comps/12/schedule/La-Liga-Scores-and-Fixtures', # la liga fixtures
    '3':'https://fbref.com/en/comps/11/schedule/Serie-A-Scores-and-Fixtures', # serie a fixtures
    '4':'https://fbref.com/en/comps/20/schedule/Bundesliga-Scores-and-Fixtures', # bundesliga fixtures
    '5':'https://fbref.com/en/comps/13/schedule/Ligue-1-Scores-and-Fixtures', # ligue 1 fixtures
    '6':'https://fbref.com/en/comps/32/schedule/Primeira-Liga-Scores-and-Fixtures', # primeira liga fixtures
    '7':'https://fbref.com/en/comps/8/schedule/Champions-League-Scores-and-Fixtures', # champions league fixtures
    '8':'https://fbref.com/en/comps/19/schedule/Europa-League-Scores-and-Fixtures' # europa league fixtures
    }

# holding place function for the prediction of the score
def scrape_data(comp, team1, team2):
    
    url = data_source.get(comp) # get the correct URL from the dictionary
    
    # extract information for the matches using Pandas   
    df = pd.read_html(url,index_col=False)[0]
    df = df[df['Wk'].notna()] # remove Weeks with NaN values
    df = df[df['Score'].notna()] # remove games that have not occured yet
    df = df.rename(columns={'xG':'xGHome','xG.1':'xGAway'})
    
    # format the dataframe for output
    # output_df = df.drop(['Wk','Day','Date','Time','Venue','Referee','Attendance','Match Report','Notes'],axis=1) # display relevant info - keep all info in df
    
    
    name = get_comp_name(url)
    df.to_csv(f"{name}.csv", index=False) # format dataframe into a CSV file
    
    # data_list = output_df.to_dict(orient='records') # process data into a list of dictionaries
    prediction(name, team1, team2)
    
def prediction(name, team1, team2):
    
    # Read in the CSV with the match data
    match_data = pd.read_csv(f'{name}.csv')
    
    found_home = check_team(team1, match_data)
    found_away = check_team(team2, match_data)
            
    if found_home and found_away:
        print("Teams are valid")
    else:
        print("Teams are invalid")
    
        
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