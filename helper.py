import pandas as  pd
import numpy as np

results=pd.read_csv('results.csv')

def results_tally_og(results):
    results['winning_team'] = results.apply(
        lambda row: row['home_team'] if row['home_score'] > row['away_score']
        else row['away_team'] if row['away_score'] > row['home_score']
        else np.nan, axis=1
    )

    results['losing_team'] = results.apply(
        lambda row: row['home_team'] if row['away_score'] > row['home_score']
        else row['away_team'] if row['home_score'] > row['away_score']
        else np.nan, axis=1
    )

    results = results.fillna('Draw')
    results['total_goals'] = results['home_score'].fillna(0) + results['away_score'].fillna(0)
    results['year'] = results['date'].apply(get_year)

    return results
def results_tally(results):

    results['winning_team'] = results.apply(
        lambda row: row['home_team'] if row['home_score'] > row['away_score']
        else row['away_team'] if row['away_score'] > row['home_score']
        else np.nan, axis=1
    )

    results['losing_team'] = results.apply(
        lambda row: row['home_team'] if row['away_score'] > row['home_score']
        else row['away_team'] if row['home_score'] > row['away_score']
        else np.nan, axis=1
    )

    results = results.fillna('Draw')
    results['total_goals'] = results['home_score'].fillna(0) + results['away_score'].fillna(0)
    results['year'] = results['date'].apply(get_year)
    results['tournament'] = results['tournament'].apply(lambda x: 'Non Friendly' if x != 'Friendly' else 'Friendly')

    return results

def overall_results_tally(results,venue,country):
        results['year'] = results['date'].apply(get_year)

        results['winning_team'] = results.apply(
          lambda row: row['home_team'] if row['home_score'] > row['away_score']
          else row['away_team'] if row['away_score'] > row['home_score']
          else np.nan, axis=1
       )

        results['losing_team'] = results.apply(
          lambda row: row['home_team'] if row['away_score'] > row['home_score']
          else row['away_team'] if row['home_score'] > row['away_score']
          else np.nan, axis=1
        )

        results = results.fillna('Draw')

        results['tournament'] = results['tournament'].apply(lambda x: 'Non Friendly' if x != 'Friendly' else 'Friendly')

        win_df = results
        lose_df = results

        win_df = win_df[win_df['winning_team'] != 'Draw']
        lose_df = lose_df[lose_df['losing_team'] != 'Draw']

        win_counts = win_df['winning_team'].value_counts().reset_index()
        win_counts.columns = ['country', 'win_count']

        lose_counts = lose_df['losing_team'].value_counts().reset_index()
        lose_counts.columns = ['country', 'lose_count']

        draw_df = results

        draw_df = draw_df[draw_df['winning_team'] == 'Draw']

        home_draw_counts = draw_df['home_team'].value_counts().reset_index()
        home_draw_counts.columns = ['country', 'draw_count']
        away_draw_counts = draw_df['away_team'].value_counts().reset_index()
        away_draw_counts.columns = ['country', 'draw_count']

        total_draw_counts = pd.concat([home_draw_counts, away_draw_counts]).groupby('country').sum().reset_index()

        win_lose_draw_tally = pd.concat([win_counts, lose_counts]).groupby('country').sum().reset_index()

        results_tally = pd.concat([win_lose_draw_tally, total_draw_counts]).groupby('country').sum().reset_index()

        results_tally = results_tally.sort_values('win_count', ascending=False).reset_index()

        results_tally = results_tally.drop(['index'], axis=1)

        neutral_results = results[results['neutral'] == True]

        neutral_wins_losses = neutral_results[neutral_results['winning_team'] != 'Draw']

        neutral_win_df = neutral_wins_losses['winning_team'].value_counts().reset_index()
        neutral_win_df.columns = ['country', 'win_count']
        neutral_lose_df = neutral_wins_losses['losing_team'].value_counts().reset_index()
        neutral_lose_df.columns = ['country', 'lose_count']

        neutral_results_tally = pd.concat([neutral_win_df, neutral_lose_df]).groupby('country').sum().reset_index()

        neutral_draws = neutral_results[neutral_results['winning_team'] == 'Draw']

        neutral_results_home_draws = neutral_draws['home_team'].value_counts().reset_index()
        neutral_results_away_draws = neutral_draws['away_team'].value_counts().reset_index()
        neutral_results_home_draws.columns = ['country', 'draw_count']
        neutral_results_away_draws.columns = ['country', 'draw_count']

        neutral_draws_df = pd.concat([neutral_results_home_draws, neutral_results_away_draws]).groupby(
            'country').sum().reset_index()

        neutral_results_tally = pd.concat([neutral_results_tally, neutral_draws_df]).groupby(
            'country').sum().reset_index()
        neutral_results_tally = neutral_results_tally.sort_values('win_count', ascending=False).reset_index()

        neutral_results_tally = neutral_results_tally.drop(['index'], axis=1)

        non_neutral_results = results[results['neutral'] == False]

        non_neutral_home_wins = non_neutral_results[
            non_neutral_results['home_team'] == non_neutral_results['winning_team']]
        non_neutral_away_wins = non_neutral_results[
            non_neutral_results['away_team'] == non_neutral_results['winning_team']]

        home_wins_df = non_neutral_home_wins['winning_team'].value_counts().reset_index()
        home_wins_df.columns = ['country', 'win_count']
        away_wins_df = non_neutral_away_wins['winning_team'].value_counts().reset_index()
        away_wins_df.columns = ['country', 'win_count']

        non_neutral_home_losses = non_neutral_results[
            non_neutral_results['away_team'] == non_neutral_results['winning_team']]
        non_neutral_away_losses = non_neutral_results[
            non_neutral_results['home_team'] == non_neutral_results['winning_team']]

        home_losses_df = non_neutral_home_losses['losing_team'].value_counts().reset_index()
        home_losses_df.columns = ['country', 'lose_count']
        away_losses_df = non_neutral_away_losses['losing_team'].value_counts().reset_index()
        away_losses_df.columns = ['country', 'lose_count']

        non_neutral_draws = non_neutral_results[non_neutral_results['winning_team'] == 'Draw']

        home_draws_df = non_neutral_draws['home_team'].value_counts().reset_index()
        away_draws_df = non_neutral_draws['away_team'].value_counts().reset_index()
        home_draws_df.columns = ['country', 'draw_count']
        away_draws_df.columns = ['country', 'draw_count']

        home_results_tally = pd.concat([home_wins_df, home_losses_df]).groupby('country').sum().reset_index()
        home_results_tally = pd.concat([home_results_tally, home_draws_df]).groupby('country').sum().reset_index()

        away_results_tally = pd.concat([away_wins_df, away_losses_df]).groupby('country').sum().reset_index()
        away_results_tally = pd.concat([away_results_tally, away_draws_df]).groupby('country').sum().reset_index()

        home_results_tally = home_results_tally.sort_values('win_count', ascending=False).reset_index(drop=True)
        home_results_tally = home_results_tally.drop(columns=['index', 'level_0'], errors='ignore')

        away_results_tally = away_results_tally.sort_values('win_count', ascending=False).reset_index(drop=True)
        away_results_tally = away_results_tally.drop(columns=['index', 'level_0'], errors='ignore')


        if venue == 'Overall':
         overall_results_tally = results_tally
        elif venue =='Neutral':
         overall_results_tally = neutral_results_tally
        elif venue == 'Away':
         overall_results_tally =  away_results_tally
        elif venue == 'Home':
         overall_results_tally =  home_results_tally

        # overall_results_tally = overall_results_tally.merge(friendly_results_tally, on='country', how='outer')

        # overall_results_tally.columns = ['country', 'win_count', 'lose_count', 'draw_count', 'neutral_win_count',
        #                                  'neutral_lose_count', 'neutral_draw_count', 'home_win_count',
        #                                  'home_lose_count',
        #                                  'home_draw_count', 'away_win_count', 'away_lose_count', 'away_draw_count',
        #                                  'friendly_win_count', 'friendly_lose_count', 'friendly_draw_count']

        # overall_results_tally = overall_results_tally.merge(non_friendly_results_tally, on='country', how='outer')

        overall_results_tally.columns = ['country', 'win_count', 'lose_count', 'draw_count']
        overall_results_tally['total_matches_count']=overall_results_tally['win_count']+overall_results_tally['lose_count']+overall_results_tally['draw_count']
        overall_results_tally = overall_results_tally.fillna(0)
        overall_results_tally = overall_results_tally.sort_values('win_count', ascending=False).reset_index()

        if country!='Overall':
            overall_results_tally = overall_results_tally[overall_results_tally['country']==country]

        overall_results_tally.drop(columns=['index'],inplace=True)
        return overall_results_tally


def overall_goals_tally(results, venue, country):
        results['year'] = results['date'].apply(get_year)
        results = results.fillna('Draw')
        results['tournament'] = results['tournament'].apply(lambda x: 'Non Friendly' if x != 'Friendly' else 'Friendly')

        non_neutral_results_df = results[results['neutral'] == False]

        home_goals_df = non_neutral_results_df.groupby('home_team')['home_score'].sum().reset_index().sort_values(
            'home_score', ascending=False)
        home_goals_df.rename(columns={'home_team': 'country', 'home_score': 'home_goals_scored'}, inplace=True)

        home_goals_conceded_df = non_neutral_results_df.groupby('home_team')[
            'away_score'].sum().reset_index().sort_values('away_score', ascending=False)
        home_goals_conceded_df.rename(columns={'home_team': 'country', 'away_score': 'home_goals_conceded'},
                                      inplace=True)

        away_goals_df = non_neutral_results_df.groupby('away_team')['away_score'].sum().reset_index().sort_values(
            'away_score', ascending=False)
        away_goals_df.rename(columns={'away_team': 'country', 'away_score': 'away_goals_scored'}, inplace=True)

        away_goals_conceded_df = non_neutral_results_df.groupby('away_team')[
            'home_score'].sum().reset_index().sort_values('home_score', ascending=False)
        away_goals_conceded_df.rename(columns={'away_team': 'country', 'home_score': 'away_goals_conceded'},
                                      inplace=True)

        neutral_results_df = results[results['neutral'] == True]

        neutral_home_goals_df = neutral_results_df.groupby('home_team')['home_score'].sum().reset_index().sort_values(
            'home_score', ascending=False)
        neutral_home_goals_df.rename(columns={'home_team': 'country', 'home_score': 'neutral_home_goals_scored'},
                                     inplace=True)

        neutral_home_goals_conceded_df = neutral_results_df.groupby('home_team')[
            'away_score'].sum().reset_index().sort_values('away_score', ascending=False)
        neutral_home_goals_conceded_df.rename(
            columns={'home_team': 'country', 'away_score': 'neutral_home_goals_conceded'}, inplace=True)

        neutral_away_goals_df = neutral_results_df.groupby('away_team')['away_score'].sum().reset_index().sort_values(
            'away_score', ascending=False)
        neutral_away_goals_df.rename(columns={'away_team': 'country', 'away_score': 'neutral_away_goals_scored'},
                                     inplace=True)

        neutral_away_goals_conceded_df = neutral_results_df.groupby('away_team')[
            'home_score'].sum().reset_index().sort_values('home_score', ascending=False)
        neutral_away_goals_conceded_df.rename(
            columns={'away_team': 'country', 'home_score': 'neutral_away_goals_conceded'}, inplace=True)

        neutral_total_goals_df = pd.concat([neutral_home_goals_df, neutral_away_goals_df]).groupby(
            'country').sum().reset_index()
        neutral_total_goals_df['neutral_goals_scored'] = neutral_total_goals_df['neutral_home_goals_scored'] + \
                                                         neutral_total_goals_df['neutral_away_goals_scored']
        neutral_total_goals_df.drop(columns=['neutral_home_goals_scored', 'neutral_away_goals_scored'], inplace=True)

        neutral_total_goals_conceded_df = pd.concat(
            [neutral_home_goals_conceded_df, neutral_away_goals_conceded_df]).groupby('country').sum().reset_index()
        neutral_total_goals_conceded_df['neutral_goals_conceded'] = neutral_total_goals_conceded_df[
                                                                        'neutral_home_goals_conceded'] + \
                                                                    neutral_total_goals_conceded_df[
                                                                        'neutral_away_goals_conceded']
        neutral_total_goals_conceded_df.drop(columns=['neutral_home_goals_conceded', 'neutral_away_goals_conceded'],
                                             inplace=True)

        total_goals_df = pd.concat([home_goals_df, away_goals_df]).groupby('country').sum().reset_index()
        total_goals_df['total_goals_scored'] = total_goals_df['home_goals_scored'] + total_goals_df['away_goals_scored']

        total_goals_conceded_df = pd.concat([home_goals_conceded_df, away_goals_conceded_df]).groupby(
            'country').sum().reset_index()
        total_goals_conceded_df['total_goals_conceded'] = total_goals_conceded_df['home_goals_conceded'] + \
                                                          total_goals_conceded_df['away_goals_conceded']

        total_goals_df = pd.concat([total_goals_df, neutral_total_goals_df]).groupby('country').sum().reset_index()
        total_goals_df['total_goals_scored'] += total_goals_df['neutral_goals_scored']
        total_goals_df.drop(columns=['home_goals_scored', 'away_goals_scored', 'neutral_goals_scored'], inplace=True)

        total_goals_conceded_df = pd.concat([total_goals_conceded_df, neutral_total_goals_conceded_df]).groupby(
            'country').sum().reset_index()
        total_goals_conceded_df['total_goals_conceded'] += total_goals_conceded_df['neutral_goals_conceded']
        total_goals_conceded_df.drop(columns=['home_goals_conceded', 'away_goals_conceded', 'neutral_goals_conceded'],
                                     inplace=True)

        total_df = pd.merge(total_goals_df, total_goals_conceded_df, on='country')

        if venue == 'Overall':
            overall_goals_tally = total_df
        elif venue == 'Neutral':
            overall_goals_tally = neutral_total_goals_df
        elif venue == 'Away':
            overall_goals_tally = away_goals_df
        elif venue == 'Home':
            overall_goals_tally = home_goals_df

        overall_goals_tally = overall_goals_tally.fillna(0)
        overall_goals_tally = overall_goals_tally.sort_values('total_goals_scored', ascending=False).reset_index()

        if country != 'Overall':
            overall_goals_tally = overall_goals_tally[overall_goals_tally['country'] == country]

        overall_goals_tally.drop(columns=['index'], inplace=True)
        return overall_goals_tally


def goals_tally(results):
        results = results.fillna('Draw')
        results['total_goals'] = results['home_score'].fillna(0) + results['away_score'].fillna(0)
        results['year'] = results['date'].apply(get_year)
        results['tournament'] = results['tournament'].apply(lambda x: 'Non Friendly' if x != 'Friendly' else 'Friendly')

        return results

def fetch_goals_tally(results, year, country, venue, type):
    if (year == 'Overall') & (country == 'Overall') & (venue == 'Overall') & (type == 'Overall'):
        temp_df = results
    elif (year != 'Overall') & (country == 'Overall') & (venue == 'Overall') & (type == 'Overall'):
        temp_df = results[results['year'] == int(year)]
    elif (year == 'Overall') & (country != 'Overall') & (venue == 'Overall') & (type == 'Overall'):
        temp_df = results[(results['home_team'] == country) | (results['away_team'] == country)]
    elif (year == 'Overall') & (country == 'Overall') & (venue != 'Overall') & (type == 'Overall'):
        temp_df = results
    elif (year == 'Overall') & (country == 'Overall') & (venue == 'Overall') & (type != 'Overall'):
        temp_df = results[results['tournament'] == type]
    elif (year != 'Overall') & (country != 'Overall') & (venue == 'Overall') & (type == 'Overall'):
        temp_df = results[((results['home_team'] == country) | (results['away_team'] == country)) & (results['year'] == int(year))]
    elif (year == 'Overall') & (country != 'Overall') & (venue != 'Overall') & (type == 'Overall'):
        temp_df = results[(results['home_team'] == country) | (results['away_team'] == country)]
    elif (year == 'Overall') & (country == 'Overall') & (venue != 'Overall') & (type != 'Overall'):
        temp_df = results[results['tournament'] == type]
    elif (year != 'Overall') & (country == 'Overall') & (venue != 'Overall') & (type == 'Overall'):
        temp_df = results[results['year'] == int(year)]
    elif (year != 'Overall') & (country == 'Overall') & (venue == 'Overall') & (type != 'Overall'):
        temp_df = results[(results['year'] == int(year)) & (results['tournament'] == type)]
    elif (year == 'Overall') & (country != 'Overall') & (venue == 'Overall') & (type != 'Overall'):
        temp_df = results[((results['home_team'] == country) | (results['away_team'] == country)) & (results['tournament'] == type)]
    elif (year == 'Overall') & (country != 'Overall') & (venue != 'Overall') & (type != 'Overall'):
        temp_df = results[((results['home_team'] == country) | (results['away_team'] == country)) & (results['tournament'] == type)]
    elif (year != 'Overall') & (country == 'Overall') & (venue != 'Overall') & (type != 'Overall'):
        temp_df = results[(results['year'] == int(year)) & (results['tournament'] == type)]
    elif (year != 'Overall') & (country != 'Overall') & (venue != 'Overall') & (type == 'Overall'):
        temp_df = results[((results['home_team'] == country) | (results['away_team'] == country)) & (results['year'] == int(year))]
    elif (year != 'Overall') & (country != 'Overall') & (venue == 'Overall') & (type != 'Overall'):
        temp_df = results[(results['year'] == int(year)) & (results['tournament'] == type) & ((results['home_team'] == country) | (results['away_team'] == country))]
    elif (year != 'Overall') & (country != 'Overall') & (venue != 'Overall') & (type != 'Overall'):
        temp_df = results[(results['year'] == int(year)) & (results['tournament'] == type) & ((results['home_team'] == country) | (results['away_team'] == country))]

    final_df = overall_goals_tally(temp_df,venue,country)

    return final_df


def get_year(date):
        my_str=date[:4]
        res=int(my_str)
        return res

def country_year_list(results):

        results['year'] = results['date'].apply(get_year)
        years = results['year'].unique().tolist()
        years.sort()
        years.insert(0, 'Overall')
        overall_results_tally =  results_tally(results)
        countries = overall_results_tally['country'].unique().tolist()
        countries.sort()
        countries.insert(0, 'Overall')

        return years,countries

def fetch_results_tally(results, year, country, venue, type):
    if (year == 'Overall') & (country == 'Overall') & (venue == 'Overall') & (type == 'Overall'):
        temp_df = results
    elif (year != 'Overall') & (country == 'Overall') & (venue == 'Overall') & (type == 'Overall'):
        temp_df = results[results['year'] == int(year)]
    elif (year == 'Overall') & (country != 'Overall') & (venue == 'Overall') & (type == 'Overall'):
        temp_df = results[(results['home_team'] == country) | (results['away_team'] == country)]
    elif (year == 'Overall') & (country == 'Overall') & (venue != 'Overall') & (type == 'Overall'):
        temp_df = results
    elif (year == 'Overall') & (country == 'Overall') & (venue == 'Overall') & (type != 'Overall'):
        temp_df = results[results['tournament'] == type]
    elif (year != 'Overall') & (country != 'Overall') & (venue == 'Overall') & (type == 'Overall'):
        temp_df = results[((results['home_team'] == country) | (results['away_team'] == country)) & (results['year'] == int(year))]
    elif (year == 'Overall') & (country != 'Overall') & (venue != 'Overall') & (type == 'Overall'):
        temp_df = results[(results['home_team'] == country) | (results['away_team'] == country)]
    elif (year == 'Overall') & (country == 'Overall') & (venue != 'Overall') & (type != 'Overall'):
        temp_df = results[results['tournament'] == type]
    elif (year != 'Overall') & (country == 'Overall') & (venue != 'Overall') & (type == 'Overall'):
        temp_df = results[results['year'] == int(year)]
    elif (year != 'Overall') & (country == 'Overall') & (venue == 'Overall') & (type != 'Overall'):
        temp_df = results[(results['year'] == int(year)) & (results['tournament'] == type)]
    elif (year == 'Overall') & (country != 'Overall') & (venue == 'Overall') & (type != 'Overall'):
        temp_df = results[((results['home_team'] == country) | (results['away_team'] == country)) & (results['tournament'] == type)]
    elif (year == 'Overall') & (country != 'Overall') & (venue != 'Overall') & (type != 'Overall'):
        temp_df = results[((results['home_team'] == country) | (results['away_team'] == country)) & (results['tournament'] == type)]
    elif (year != 'Overall') & (country == 'Overall') & (venue != 'Overall') & (type != 'Overall'):
        temp_df = results[(results['year'] == int(year)) & (results['tournament'] == type)]
    elif (year != 'Overall') & (country != 'Overall') & (venue != 'Overall') & (type == 'Overall'):
        temp_df = results[((results['home_team'] == country) | (results['away_team'] == country)) & (results['year'] == int(year))]
    elif (year != 'Overall') & (country != 'Overall') & (venue == 'Overall') & (type != 'Overall'):
        temp_df = results[(results['year'] == int(year)) & (results['tournament'] == type) & ((results['home_team'] == country) | (results['away_team'] == country))]
    elif (year != 'Overall') & (country != 'Overall') & (venue != 'Overall') & (type != 'Overall'):
        temp_df = results[(results['year'] == int(year)) & (results['tournament'] == type) & ((results['home_team'] == country) | (results['away_team'] == country))]

    final_df = overall_results_tally(temp_df,venue,country)

    return final_df

def football_matches_over_time(results):
    matches_per_year_over_time = results['year'].value_counts().reset_index()
    matches_per_year_over_time.rename(columns={'year': 'Year', 'count': 'Number of Matches'}, inplace=True)

    matches_per_year_over_time = matches_per_year_over_time.sort_values('Year')
    return matches_per_year_over_time

def football_goals_over_time(results):
    goals_per_year_over_time = results.groupby('year')['total_goals'].sum().reset_index()
    goals_per_year_over_time.rename(columns={'year': 'Year', 'total_goals': 'Number of Goals'}, inplace=True)

    return goals_per_year_over_time

def yearwise_goal_tally(results,country):
    temp_df = results[(results['home_team'] == country)]
    temp_df = temp_df.groupby('year').count()['home_score'].reset_index()

    temp_df_ = results[(results['away_team'] == country)]
    temp_df_ = temp_df_.groupby('year').count()['away_score'].reset_index()

    total_df = pd.concat([temp_df, temp_df_]).groupby('year').sum().reset_index()

    total_df['total_goals'] = total_df['home_score'] + total_df['away_score']
    total_df = total_df.apply(lambda x: x.astype(int) if x.dtype == 'float' else x)

    return total_df

def overall_yearwise_goal_tally(results):
    temp_df = results
    temp_df = temp_df.groupby('year').count()['total_goals'].reset_index()
    temp_df = temp_df.apply(lambda x: x.astype(int) if x.dtype == 'float' else x)

    return temp_df

def yearwise_concede_tally(results,country):
    temp_df_conceded_home = results[(results['home_team'] == country)]
    temp_df_conceded_home = temp_df_conceded_home.groupby('year').sum()['away_score'].reset_index()

    temp_df_conceded_away = results[(results['away_team'] == country)]
    temp_df_conceded_away = temp_df_conceded_away.groupby('year').sum()['home_score'].reset_index()

    total_df_conceded = pd.concat([temp_df_conceded_home, temp_df_conceded_away]).groupby('year').sum().reset_index()

    total_df_conceded['total_goals_conceded'] = total_df_conceded['away_score'] + total_df_conceded['home_score']
    total_df_conceded = total_df_conceded.apply(lambda x: x.astype(int) if x.dtype == 'float' else x)

    return total_df_conceded

def goals_scored_opp(results,country):
    home_goals_opp_wise = results[(results['home_team'] == country)].groupby('away_team')['home_score'].sum().reset_index().sort_values('home_score', ascending=False)
    away_goals_opp_wise = results[(results['away_team'] == country)].groupby('home_team')['away_score'].sum().reset_index().sort_values('away_score', ascending=False)
    away_goals_opp_wise = away_goals_opp_wise.rename(columns={'home_team': 'country', 'away_score': 'goals_scored'})
    home_goals_opp_wise = home_goals_opp_wise.rename(columns={'away_team': 'country', 'home_score': 'goals_scored'})
    total_goals_opp_wise = pd.concat([away_goals_opp_wise, home_goals_opp_wise]).groupby('country').sum().reset_index().sort_values('goals_scored', ascending=False)
    return total_goals_opp_wise

def goals_conceded_opp(results,country):
    home_goals_conceded_opp_wise = results[(results['home_team'] == country)].groupby('away_team')['away_score'].sum().reset_index().sort_values('away_score', ascending=False)
    away_goals_conceded_opp_wise = results[(results['away_team'] == country)].groupby('home_team')['home_score'].sum().reset_index().sort_values('home_score', ascending=False)
    away_goals_conceded_opp_wise = away_goals_conceded_opp_wise.rename(columns={'home_team': 'country', 'home_score': 'goals_conceded'})
    home_goals_conceded_opp_wise = home_goals_conceded_opp_wise.rename(columns={'away_team': 'country', 'away_score': 'goals_conceded'})
    total_goals_conceded_opp_wise = pd.concat([away_goals_conceded_opp_wise, home_goals_conceded_opp_wise]).groupby('country').sum().reset_index().sort_values('goals_conceded', ascending=False)
    return total_goals_conceded_opp_wise
