"""
This file produces an organized, simplified table from raw behavioral .csv files generated by the ABET behavioral testing software. 
Using Pandas to generate a data frame from the raw data, we then use a series of functions to pull out relevant behavioral events within each trial

This code was written by Patrick Piantadosi & Kendall Coden, from the Laboratory of Behavioral and Genomic Neuroscience @ NIAAA.

"""

# Import relevant packages
import pandas as pd
import numpy as np

# read in behavioral data as .csv
# eventually will write this more flexibly as a function (so users can give a filename externally)
data = pd.read_csv("74 12042019.csv") 

#Time values < 0 are housekeeping variables reported by the software. Safe to filter these out so they do not get counted as trials, etc.
filter_time_zero = data.Evnt_Time != 0
filter_time_zero.values
data = data[filter_time_zero]

#logic for indicating new trials (which will later be used to groupby), adds a new column to the data frame (data) that counts the number of trials based on trial starts
is_new_trial = (data.Item_Name == "Forced-Choice Trials Begin") | (data.Item_Name == "Free-Choice Trials begin")
data["is_new_trial"] = is_new_trial
data["is_new_trial"].value_counts()
data["trial_num"] = np.cumsum(data["is_new_trial"])
data["trial_num"].max()

#make_table makes a table based upon input from the functions defined below
def make_table(data):
    # add new functions here
    BlockNum = get_block(data)
    trial_type = get_trial_type(data)
    rew_type = rew_size(data)
    shocker = shock(data)
    choice_time = choiceTime(data)
    collect_time = collectTime(data)
    start_time = startTime(data)


    return pd.Series({"BlockNum": BlockNum,
                     "trial_type": trial_type,
                     "rew_type": rew_type,
                     "shock": shocker,
                     "choice_time": choice_time,
                     "collect_time": collect_time,
                     "start_time": start_time})

"""
This function checks the data for which of the 3 trial blocks ("Sessions") the mouse is currently in, and then returns an 
integer value depending on the block of a specific trial

"""
def get_block(data):
    is_block_1 = data[data["Item_Name"] == "Session1"]["Arg1_Value"]
    is_block_2 = data[data["Item_Name"] == "Session2"]["Arg1_Value"]
    is_block_3 = data[data["Item_Name"] == "Session3"]["Arg1_Value"]
    
    if is_block_1.any():
        return 1
    elif is_block_2.any():
        return 2
    elif is_block_3.any():
        return 3
    
"""
This function checks what size reward the mouse selected for a given trial, 
and assigns the value (speed of the peristaltic pump, in ms) to the trial
"""

def rew_size(data):
    if len(data.loc[data["Item_Name"] == "Feeder #2"]["Arg1_Value"]) == 0:
        return np.nan
    elif len(data.loc[data["Item_Name"] == "Feeder #2"]["Arg1_Value"]) == 1:
        return (data.loc[data["Item_Name"] == "Feeder #2"]["Arg1_Value"]).values[0]
    else:
        raise ValueError(f"more than one reward {data.trial_num.iloc[0].values[0]}")

        
"""
Each trial block is made up of Forced-Choice or Free-Choice trials, this function checks which 
trial type the mouse is in, and assigns that value to the trial 
"""

def get_trial_type(data):
    if (data["Item_Name"] == "Forced-Choice Trials Begin").sum():
        return "Forced"
    elif (data["Item_Name"] == "Free-Choice Trials begin").sum():
        return "Free"
    

"""
Some trials result in a minor footshock, this function checks whether the 
footshock occured or not, and assigns that value to the trial
"""

def shock(data):
    if len(data.loc[data["Item_Name"] == "shock_on_off"]["Arg1_Value"]) == 0:
        return np.nan
    elif len(data.loc[data["Item_Name"] == "shock_on_off"]["Arg1_Value"]) == 1:
        return(data.loc[data["Item_Name"] == "shock_on_off"]["Arg1_Value"]).values[0]
    
"""
Events are timestamped in the behavioral software. This function returns the time at which a mouse initiates a trial.
"""

def startTime(data):
    if len(data.loc[data["Item_Name"].str.contains("Trials Begin" or "Trials begin")]) == 0:
        return np.nan
    elif len(data.loc[data["Item_Name"].str.contains("Trials Begin" or "Trials begin")]) == 1:
        return(data.loc[data["Item_Name"].str.contains("Trials Begin" or "Trials begin")]["Evnt_Time"]).values[0]

    
"""
Events are timestamped in the behavioral software. This function returns the time at which a mouse chooses the
large or small reward.
"""

def choiceTime(data):
    if len(data.loc[data["Item_Name"] == "Feeder #2"]["Arg1_Value"]) == 0:
        return np.nan
    elif len(data.loc[data["Item_Name"] == "Feeder #2"]["Arg1_Value"]) == 1:
        return(data.loc[data["Item_Name"] == "Feeder #2"]["Evnt_Time"]).values[0]
    
    
"""
Events are timestamped in the behavioral software. This function returns the time at which a mouse collects the reward.
"""
def collectTime(data):
    if len(data.loc[data["Item_Name"].str.contains("Reward Retrieved")]) == 0:
        return np.nan
    elif len(data.loc[data["Item_Name"].str.contains("Reward Retrieved")]) == 1:
        return(data.loc[data["Item_Name"].str.contains("Reward Retrieved")]["Evnt_Time"]).values[0]
    

grouped_data = data.groupby("trial_num")
result = grouped_data.apply(make_table)

result

"""
Will eventually need functions to filter based on data type, can use .loc method to accomplish this
The code below filters the newly generated table "result" by whether the mouse chose a large or small reward
"""
large_rew_only = result.loc[result["rew_type"] == 1.2]

large_rew_only
