#pip install git+https://github.com/JustAnotherArchivist/snscrape.git

#importing required libraries
import pandas as pd
import snscrape.modules.twitter as sntwitter
from datetime import date, timedelta
import itertools

position_list = ['CEO', 'vice-president', 'president', 'director', 'partner', 'chief', 'founder', 'co-founder', 'CTO', 'Congress Women', 'Congress men', 'senator', 'MP', 'parliament', 'head', 'senior', 'Activist', 'creator', 'board member', 'Chairman', 'VP', 'minister', 'politician']
# country_list = ['India', 'Maldives', 'Bangladesh', 'Pakistan', 'Afghanistan', 'Nepal', 'Bhutan', 'Sri Lanka']
country_list = ["Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia", "China", "Cyprus", "Georgia", "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan", "Jordan", "Kazakhstan", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", "Maldives", "Mongolia", "Myanmar", "Nepal", "North Korea", "Oman", "Pakistan", "Palestine", "Philippines", "Qatar", "Russia", "Saudi Arabia", "Singapore", "South Korea", "Sri Lanka", "Syria", "Taiwan", "Tajikistan", "Thailand", "Timor-Leste", "Turkey", "Turkmenistan", "United Arab Emirates", "Uzbekistan", "Vietnam", "Yemen"]

# creating a function to fetch tweet data by country and append to dataframe
# we shall filter location after joining all the country wise dataframes

def fetch_user_data_to_csv(country, positions, req_no_of_usernames=10):
    # fetch the raw data; filters applied near, min_faves = 1000 and since/until
    from_time = date.today() - timedelta(days=14)
    search_query = 'lang:en near:"{0}" since:"{1}" until:"{2}" min_faves:1000'.format(country, from_time, date.today())
    raw_df = pd.DataFrame(itertools.islice(sntwitter.TwitterSearchScraper(search_query).get_items(), req_no_of_usernames))

    try:
        # transforming_raw_data
        trns_df = transforming_raw_data(raw_df)

        # filtering data by followers count and bio
        filtered_df = filtering_user_data(trns_df, positions, followers_thres=10000)

        # saving as csv file...uncomment if you need country wise scraped username as csv files
        #filtered_df.to_csv(f'./data/{country}_usernames.csv', index=False)

        # printing completion status
        print(f'{country} usernames export complete:: {filtered_df.shape[0]} records exported')

        return filtered_df
    except KeyError:
        return pd.DataFrame(columns=['username','bio', 'profile_url', 'website', 'location', 'followers_count'])


# function to clean raw scraped data into required user data after cleaning and filtering
# output dataframe will only contain columns like username, bio, profile_url, website, location, followers_count
def transforming_raw_data(raw_df):
    clean_df = raw_df[['user']]
    clean_df['username'] = clean_df.user.apply(lambda x: x['username'])
    clean_df.drop_duplicates(subset=['username'], inplace=True)
    clean_df['bio'] = clean_df.user.apply(lambda x: x['renderedDescription'])
    clean_df['profile_url'] = clean_df.user.apply(lambda x: f"https://twitter.com/{x['username']}")
    clean_df['website'] = clean_df.user.apply(lambda x: '' if x['link'] is None else x['link']['url'])
    clean_df['location'] = clean_df.user.apply(lambda x: x['location'])
    clean_df['followers_count'] = clean_df.user.apply(lambda x: x['followersCount'])
    clean_df.drop(['user'], axis=1, inplace=True)
    return clean_df


# function to filter data by followers_count, bio
# input dataframe of this func is the output dataframe from transforming_raw_data function
def filtering_user_data(cleaned_df, positions, followers_thres=10000):
    follower_filter = (cleaned_df.followers_count >= followers_thres)
    bio_filter = cleaned_df.bio.apply(lambda x: bio_check(x, positions))
    filtered_df = cleaned_df[follower_filter & bio_filter]
    return filtered_df

#function for checking bio
def bio_check(bio, positions):
    for position in positions:
        if position.lower() in bio.lower():
            return True
    return False

#looping for all countries
def regionwise_scraping(countries, positions, raw_user_num_per_country, region = 'south_asia'):
    df_south_asia_usernames = pd.DataFrame()
    #starting the loop
    for country in countries:
        #assigning to a temp dataframe
        df = fetch_user_data_to_csv(country, positions, raw_user_num_per_country)
        #appending to main dataframe
        df_south_asia_usernames = pd.concat([df_south_asia_usernames, df])

    #removing duplicates by username
    df_south_asia_usernames.drop_duplicates(subset=['username'], inplace=True)
    #saving as csv
    df_south_asia_usernames.to_csv(f'./data/{region}_usernames.csv', index=False)

    return df_south_asia_usernames

#enter your
df_asia = regionwise_scraping(country_list,position_list, 50000, 'asia')
print(df_asia)