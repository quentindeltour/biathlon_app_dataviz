import biathlonresults
import numpy as np
import pandas as pd


def get_individual_ski_shoot_plot(saison=2021, sex='M'):
     top = pd.DataFrame(biathlonresults.cup_results('BT{}SWRLCP__S{}TS'.format(saison, sex)).get('Rows'))
     top['ski'] = top['IBUId'].apply(lambda x:biathlonresults.cisbios(x).get('StatSkiing')[0])
     top['shoot'] = top['IBUId'].apply(lambda x:biathlonresults.cisbios(x).get('StatShooting')[0])
     top['standing'] = top['IBUId'].apply(lambda x:biathlonresults.cisbios(x).get('StatShootingStanding')[0])
     top['prone'] = top['IBUId'].apply(lambda x:biathlonresults.cisbios(x).get('StatShootingProne')[0])
     top.replace('%', '', inplace=True, regex=True)
     top.replace('', np.nan, inplace=True)
     top.dropna(subset=['ski', 'shoot', 'standing', 'prone'], inplace=True)
     top[['ski', 'shoot', 'prone', 'standing', 'Score']] = top[['ski', 'shoot', 'prone', 'standing', 'Score']].astype(int)
     top['shoot_demeaned'] = top["shoot"].apply(lambda x: x-top['shoot'].mean())
     top['ski'] = -top['ski']
     top = top.head(50)
     return top

def update_df():
    df_H = get_individual_ski_shoot_plot(sex='M')
    df_F = get_individual_ski_shoot_plot(sex='W')

    df_H['Rank_lettres'] = ['Premier', 'Second', 'Troisieme'] + ['Autres' for i in range(4, len(df_H)+1)]
    df_F['Rank_lettres'] = ['Première', 'Seconde', 'Troisieme'] + ['Autres' for i in range(4, len(df_F)+1)]
    df_F.at[df_F[df_F.Nat=="FRA"].index, 'Rank_lettres']= "Francaise"
    df_H.at[df_H[df_H.Nat=="FRA"].index, 'Rank_lettres']= "Francais"
    df_H.to_csv('./data/ski_shoot_2021_H.csv')
    df_F.to_csv('./data/ski_shoot_2021_F.csv')
    return df_H, df_F

if __name__ == '__main__':
    update_df()