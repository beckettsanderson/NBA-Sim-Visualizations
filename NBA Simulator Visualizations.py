# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 10:30:34 2022

@author: Beckett Sanderson
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

PER_GAME = "Team Per Game Stats 2021-22.txt"
PER_100 = "Team Per 100 Possesions Stats 2021-22.txt"
ADVANCED = "Team Advanced Stats 2021-22.txt"
SHOOTING = "Team Shooting Stats 2021-22.txt"

def read_csv(filename, headers = None):
    """
    Reads in a csv with pandas to create a data frame

    Parameters
    ----------
    filename : string
        the location of the file to read in data from.
    headers : list
        the names for the headers of the columns

    Returns
    -------
    df : data frame
        a data frame containing all the data from the csv.

    """
    df = pd.read_csv(filename)
    
    # sets column headers if there are none already
    if headers != None:
        
        df.columns = headers
    
    #print(df.head(), "\n")
    
    return df


def understand(df):
    """
    Prints out the head, description, and shape of the data frame to get 
    a better idea of how it looks in spyder

    Parameters
    ----------
    df : data frame
        contains data pertaining to the topic of interest.

    Returns
    -------
    None.

    """
    # prints out info about data frame
    print(df.head(), "\n")
    print(df.describe(), "\n")
    print(df.shape, "\n")


def add_wins(df, wins):
    """
    Edits a data frame so if it does not have wins as a part of the data 
    frame it becomes a column to compare

    Parameters
    ----------
    df : data frame
        contains data pertaining to the topic of interest.
    wins : data frame
        contains each team and their corresponding wins

    Returns
    -------
    None.

    """
    df.insert(1, "W", wins["W"])


def plot_heatmap(df):
    """
    Plots a heatmap of the correlations between different variables in a 
    data frame

    Parameters
    ----------
    df : data frame
        contains data pertaining to the topic of interest.

    Returns
    -------
    None.

    """
    # calculates the correlations of all possible combinations in the dataset
    corr = df.corr()
    
    # prints out the correlation with wins for every other item in the df
    print(corr["W"], "\n")
    
    # prints out a heatmap of each of the correlations for easy visualization
    sns.heatmap(corr)
    plt.show()
    
    
def draw_plots(df):
    """
    Plots the stats that have the strongest correlation to wins

    Parameters
    ----------
    df : data frame
        contains data pertaining to the topic of interest.

    Returns
    -------
    None.

    """
    # calculates the correlations 
    corr = df.corr()
    
    # puts the indexes, the stats into a list
    columns = corr.index.tolist()
    
    # for each row, if the absolute value of the correlation is greater than 
    # 0.75 then plot the scatter plot between those two categories
    for i in range(len(corr)):
        
        # included does not equal one to excluded graphing same data
        if abs(corr['W'].iloc[i]) >= 0.75 and abs(corr['W'].iloc[i]) != 1:
            
            # plots data against wins for higher correlations
            plt.scatter(df[columns[i]], df['W'])
            
            # create data for line of best fit using numpy built in functions
            x = np.array(df[columns[i]])
            y = np.array(df['W'])
            m, b = np.polyfit(x, y, 1)
            
            # creates line of best fit as a string to allow it to be added to legend
            lobf_as_str = str(round(m, 2)) + " * x + " + str(round(b, 2))

            # plot line of best fit
            plt.plot(x, m * x + b, label = lobf_as_str)
            
            # labels the plot with the stat it is comparing to wins
            plt.title(columns[i] + " Compared to Wins")
            plt.xlabel(columns[i])
            plt.ylabel("Number of Wins")
            plt.legend()
            plt.show()


def Main():

    print("Welcome to our Data Club project\n")
    
    # reads in all of the data to data frames
    per_game_df = read_csv(PER_GAME)
    per_100_df = read_csv(PER_100)
    adv_df = read_csv(ADVANCED)
    shoot_df = read_csv(SHOOTING)
    
    # adds wins to each of the three df that don't have wins per team
    wins_df = adv_df[["Team", "W", "L"]]
    add_wins(per_game_df, wins_df)
    add_wins(per_100_df, wins_df)
    add_wins(shoot_df, wins_df)
    
    # plots a heatmap for each of the data frames to view which stats have 
    # the most correlation to winning
    plot_heatmap(per_game_df)
    plot_heatmap(per_100_df)
    plot_heatmap(adv_df)
    plot_heatmap(shoot_df)
    
    # plots all of the scatter plots for the strongest correlated stats
    draw_plots(per_game_df)
    draw_plots(per_100_df)
    draw_plots(adv_df)
    draw_plots(shoot_df)
    

if __name__ == "__main__":

  Main()
