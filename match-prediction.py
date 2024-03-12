import pandas as pd
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
def scrape_data(comp):
    
    url = data_source.get(comp) # get the correct URL from the dictionary
    
    # extract information for the matches using Pandas   
    df = pd.read_html(url,index_col=False)[0]
    df = df[df['Wk'].notna()] # remove Weeks with NaN values
    df = df[df['Score'].notna()] # remove games that have not occured yet
    df = df.rename(columns={'xG':'xGHome','xG.1':'xGAway'})
    output_df = df.drop(['Wk','Day','Date','Time','Venue','Referee','Attendance','Match Report','Notes'],axis=1) # display relevant info - keep all info in df
    pd.set_option('display.max_rows', None)
    name = get_comp_name(url)
    df.to_csv(f"{name}.csv", index=False) # format dataframe into a CSV file
    
    # print(output_df.iloc[0]) # selects a specific row from the data frame, places in a 2D list
    # print(output_df.iloc[0]['Home']) # gets the name of the home team
    data_list = output_df.to_dict(orient='records') # process data into a list of dictionaries
    prediction(name)
    
def prediction(name):
    
    # Read in the CSV with the match data
    match_data = pd.read_csv(f'{name}.csv')
    
    display(match_data)
        
def check_team(team):
    # add error handling to search the array to see if the team is currently in the league
    print('')
        
def get_comp_name(url):
    split_url = url.split('/')
    unformatted_name = split_url[-1].split('-')
    
    name = unformatted_name[0]+" "+unformatted_name[1]
    if name == 'Bundesliga Scores':
        name = 'Bundesliga'
        
    return name
    
def main():
    print('---- Welcome to the football match score predictor! ----')
    
    # team1 = input('Please enter the home team: ')
    # team2 = input('Please enter the away team: ')
    
    competition = input('Please select a competition for the match up: (1-8)\n\n1. Premier League\n2. La Liga\n3. Serie A\n4. Bundesliga\n5. Ligue 1\n6. Primeira Liga\n7. Champions League\n8. Europa League\n--> ')
    choices = ['1', '2', '3', '4', '5', '6', '7', '8']
    while competition not in choices:
        competition = input('Invalid choice, please select again (1-8): ')
    scrape_data(competition)



if __name__ == '__main__':
    main()