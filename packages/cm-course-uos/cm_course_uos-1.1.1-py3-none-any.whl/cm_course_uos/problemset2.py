"""
authors: Deniz M. Gun (dguen@uos.de)

This module contains helper and test functions for Problemset 2
 of the course "Cognitive Modeling" at the University of Osnabrueck.
 This module exists in order to load certain functionality into the
 assignment notebooks without involuntarily giving students access to
 solutions.
"""
import numpy as np
import random
import pandas as pd


def simulate_conditioning(stimuli, n_trials=10, alpha=0.5,
                          reward=1, title="Conditioning", plot_trials=True):
  """ Simulates how the valence of conditioned stimuli changes over time
  according to the principles of classical conditioning, using the Rescolra-Wagner
  Model.
  Arguments:
    stimuli (list):
      Each item in the list represents a stimulus.
      Each stimulus is a tuple:
        (stimulus_type,        : (str)  name of the stimulus
         salience,             : (float) salience [0-1]
         (start_trial,
          end_trial),          : (int,int) marks start and end of stimulus exposure
         initial_valence       : stimulus valence at trial 0
        )

    n_trials (int): Optional. The number of trials for which the experiment is run
    alpha (float):  Optional. Determines the learning rate
    reward (float): Optional. Reward magnitude. Fixed across trials.
  """
  if not stimuli:
    print("No stimuli provided")
    return

  # Initiate all stimuli values with initial valence v_0
  stimuli_values = {name: v_0 for name, _, _, v_0 in stimuli}
  # for example : {'light':0.5, 'sound':0, 'smell':0}

  # Initiates a DataFrame for storing trial data
  trial_data = pd.DataFrame({name: [v_0] for name, _, _, v_0 in stimuli})
  # may look like this later: {'light':[0, 0.1, 0.2], 'sound':[0, 0.5, 0.8], ...}

  # Start trials
  for t in range(n_trials):

    # The sum in formula (2) is the sum of all ~current~ stimulus valences.
    # Hence, for each trial we need to make a copy before we start updating
    # the valences. This ensures that we do not overwrite the current valences
    # before each one has been updated.
    values_all = stimuli_values.copy().values()

    # Stimuli is a list of tuples [ (name,salience,range,v_0), ... ].
    # In the for loop below we iterate through the list and unpack each
    # tuple.
    for name, salience, (start_trial, end_trial), _ in stimuli:

      # skip the value update of stimuli which are not part of the current trial
      if t not in range(start_trial, end_trial):
        continue

      # Just shortening variable names for readability in the assignment below
      # Could be done in one line but is split up for readability.
      v_cs = stimuli_values[name]      # valence of the current stimulus
      s_cs = salience                  # salience of the current stimulus
      sum_valences = sum(values_all)   # the sum of all stimulus valences

      ####### SUBTASK A. START #####
      # Compute the updated valence of the stimulus, v_cs, here
      v_cs_new = v_cs + s_cs * alpha * (reward - sum_valences)  # CODE
      ####### SUBTASK A. END #######
      stimuli_values[name] = v_cs_new

    # Logging the trial data
    trial_data.loc[t+1] = stimuli_values.values()  # adding a row

  if plot_trials:
    plot = plot_rw_trials(trial_data, stimuli, title=title)
  return trial_data, plot



def test_simulate_conditioning(student_function):
    n_trials=20

    stim_acq = ("light", 1, (0, n_trials), 0)
    stim_setup_acquisition = [stim_acq]
    td_acq = simulate_conditioning(stim_setup_acquisition,
                              reward=1,
                              n_trials = n_trials,
                             plot_trials=False)
    td_acq_student = student_function(stim_setup_acquisition,
                                reward=1,
                                n_trials=n_trials,
                                plot_trials=False)
    if not td_acq_student.equals(td_acq):
        print("simulate_conditioning does not generate expected trial data.")
    return

    stim_ext = ("light",1, (0, n_trials), 1)
    stim_setup_acquisition = [stim_acq]
    td_ext = simulate_conditioning(stim_setup_acquisition,
                              reward=0,
                              n_trials = n_trials,
                              plot_trials=False)
    td_ext_student = student_function(stim_setup_acquisition,
                              reward=0,
                              n_trials = n_trials,
                              plot_trials=False)
    if not td_ext_student.equals(td_ext):
        print("simulate_conditioning does not generate expected trial data.")
    return


    stim_conditioned = ("ligh",1,(0,n_trials),0)
    stim_blocked = ("sound",1,(3,n_trials),0)
    td_blocked = simulate_conditioning([stim_conditioned,stim_blocked],
                               n_trials=n_trials,
                               reward=1,
                               plot_trials=False)
    td_blocked_student = student_function([stim_conditioned,stim_blocked],
                               n_trials=n_trials,
                               reward=1,
                               plot_trials=False)
    if not td_blocked_student.equals(td_blocked):
        print("simulate_conditioning does not generate expected trial data.")
    return

    stim_conditioned = ("light",1,(0,n_trials),0)
    stim_oshadowed = ("sound",0.2,(0,n_trials),0)
    td_oshadowed = simulate_conditioning([stim_conditioned,stim_oshadowed],
                               n_trials=n_trials,
                               reward=1,
                               plot_trials=False)
    td_oshadowed_student = student_function([stim_conditioned,stim_oshadowed],
                               n_trials=n_trials,
                               reward=1,
                               plot_trials=False)
    if not td_oshadowed_student.equals(td_oshadowed):
        print("simulate_conditioning does not generate expected trial data.")
    return

    print("simulate_conditioning produces correct output.")