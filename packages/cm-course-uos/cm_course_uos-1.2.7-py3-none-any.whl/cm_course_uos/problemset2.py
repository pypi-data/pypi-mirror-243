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



def simulate_conditioning(stimuli, n_trials=10, e=0.5,
                          reward=1, title="Conditioning",
                          plot_function = None,
                          plot_trials = False):
    if not stimuli:
        print("No stimuli provided")
        return
        
    f=reward
    a = {b: v_0 for b, _, _, v_0 in stimuli}
    trial_data = pd.DataFrame({name: [v_0] for name, _, _, v_0 in stimuli})
    for t in range(n_trials):
        g = sum(a.copy().values())
        for b, d, (start_trial, end_trial), _ in stimuli:
            if t not in range(start_trial, end_trial):
                continue  
            h = a[b] + d * e * (f - g)  
            a[b] = h
        trial_data.loc[t+1] = a.values()
    if plot_trials:
        plot_function(trial_data, stimuli, title=title)
    return trial_data
    

def test_simulate_conditioning(student_function):
    n_trials = 20

    stim_acq = ("light", 1, (0, n_trials), 0)
    stim_setup_acquisition = [stim_acq]
    td_acq = simulate_conditioning(stim_setup_acquisition,
                                   reward=1,
                                   n_trials=n_trials)
    td_acq_student = student_function(stim_setup_acquisition,
                                      reward=1,
                                      n_trials=n_trials,
                                      plot_trials=False)
    if not td_acq_student.equals(td_acq):
        print("simulate_conditioning does not generate expected trial data.")
        return

    stim_ext = ("light", 1, (0, n_trials), 1)
    stim_setup_acquisition = [stim_acq]
    td_ext = simulate_conditioning(stim_setup_acquisition,
                                   reward=0,
                                   n_trials=n_trials)
    td_ext_student = student_function(stim_setup_acquisition,
                                      reward=0,
                                      n_trials=n_trials,
                                      plot_trials=False)
    if not td_ext_student.equals(td_ext):
        print("simulate_conditioning does not generate expected trial data.")
        return

    stim_conditioned = ("ligh", 1, (0, n_trials), 0)
    stim_blocked = ("sound", 1, (3, n_trials), 0)
    td_blocked = simulate_conditioning([stim_conditioned, stim_blocked],
                                       n_trials=n_trials,
                                       reward=1)
    td_blocked_student = student_function([stim_conditioned, stim_blocked],
                                          n_trials=n_trials,
                                          reward=1,
                                          plot_trials=False)
    if not td_blocked_student.equals(td_blocked):
        print("simulate_conditioning does not generate expected trial data.")
        return

    stim_conditioned = ("light", 1, (0, n_trials), 0)
    stim_oshadowed = ("sound", 0.2, (0, n_trials), 0)
    td_oshadowed = simulate_conditioning([stim_conditioned, stim_oshadowed],
                                         n_trials=n_trials,
                                         reward=1)
    td_oshadowed_student = student_function([stim_conditioned, stim_oshadowed],
                                            n_trials=n_trials,
                                            reward=1,
                                            plot_trials=False)
    if not td_oshadowed_student.equals(td_oshadowed):
        print("simulate_conditioning does not generate expected trial data.")
        return
    print("simulate_conditioning generates correct trial data.")


def test_1b_acq(stim_acq, reward):
    reward_ok = reward > 0
    salience_ok = stim_acq[1] > 0
    trials_ok = stim_acq[2][0] + 2 < stim_acq[2][1]
    initial_valence_ok = stim_acq[3] < reward

    if reward_ok and salience_ok and trials_ok and initial_valence_ok:
        print("Plausible stimulus setup for acquisition")
    else:
        print("Incorrect Stimulus Setup")


def test_1b_ext(stim_ext, reward):
    reward_ok = reward < stim_ext[3]
    salience_ok = stim_ext[1] > 0
    trials_ok = stim_ext[2][0] < stim_ext[2][1]
    initial_valence_ok = stim_ext[3] > reward

    if reward_ok and salience_ok and trials_ok and initial_valence_ok:
        print("Plausible stimulus setup for extinction")
    else:
        print("Incorrect Stimulus Setup")


def test_1b_block(stim_cs, stim_blocked, reward):
    reward_ok = reward > stim_cs[3] and reward > stim_blocked[3]
    salience_ok = stim_cs[1] > 0 and stim_cs[1] == stim_blocked[1]
    if not salience_ok:
        print("Saliences must be equal")
    trials_ok = stim_cs[2][0] < stim_cs[2][1] and stim_blocked[2][0] > stim_cs[2][0]
    # higher initial valence
    trials_ok = trials_ok or stim_cs[3] > stim_blocked[3]
    initial_valence_ok = stim_cs[3] >= stim_blocked[3]

    if reward_ok and salience_ok and trials_ok and initial_valence_ok:
        print("Plausible stimulus setup for blocking")
    else:
        print("Incorrect Stimulus Setup")


def test_1b_oshadow(stim_cs, stim_oshadowed, reward):
    reward_ok = reward > stim_cs[3] and reward > stim_oshadowed[3]
    salience_ok = stim_cs[1] > 0 and stim_cs[1] > stim_oshadowed[1] and stim_oshadowed[1] > 0
    trials_ok = stim_cs[2][0] < stim_cs[2][1] and stim_oshadowed[2][0] < stim_oshadowed[2][1]
    initial_valence_ok = stim_cs[3] == stim_oshadowed[3]
    if not initial_valence_ok:
        print("Initial valences must be equal")
    if reward_ok and salience_ok and trials_ok and initial_valence_ok:
        print("Plausible stimulus setup for overshadowing")
    else:
        print("Incorrect stimulus Setup")


def compute_delta(a, b, c, d, e, f):
  if e:
    g = d * b - a
  else:
    g = d * (b + c) - a
  return g


def test_compute_delta(student_function):
  correct = True
  for t in (True, False):
      for c in range(10):
          for a in range(10):
              student_delta = student_function(a, 1, c, 0.9, t, "")
              correct_delta = compute_delta(a, 1, c, 0.9, t, "")
              if student_delta != correct_delta:
                  print("compute_delta generates wrong outputs")
                  return
  print("compute_delta generates correct outputs")
  return



def choose_action(a, b, c):
    d = [0,1,2,3]
    if np.random.uniform(0, 1) < c:
      e = np.random.choice(d)
    else:
      e = np.argmax(a[b])  
    return e



def test_choose_action(student_function):
    np.random.seed(1)
    Q = np.array([[0,1,1,0]])
    eps = 0.5
    n = 100000
    actions = np.array([choose_action(Q,0,eps) for _ in range(n)])
    student_actions = np.array([student_function(Q,0,eps) for _ in range(n)])

    dist = np.bincount(actions)/n
    stud_dist = np.bincount(student_actions)/n

    if not np.allclose(dist, stud_dist, atol=0.02):
      print("choose_action produces incorrect outputs")
    else:
      print("choose_action produces correct outputs")
    return
              
              
def update_q(a, b, c, d, e, f=0.2, g=0.6):

  h = np.argmax(a[d])
  i =  e + g * a[d][h] - a[b][c]
  j = a[b][c] + f * i
  a[b][c] = j
  return a

def test_update_q(student_function):
    Q = np.random.normal(size=(16,4))
    states = np.random.randint(0,15,1000)
    actions = np.random.randint(0,3,1000)
    rewards = np.random.randint(0,1,1000)
    next_states = np.random.randint(0,15,1000)
    state_action_pairs = list(zip(states,actions,rewards,next_states))
    
    Q_correct = Q.copy()
    Q_student = Q.copy()
    for state,action,reward,next_state in state_action_pairs:
        Q_correct = update_q(Q_correct,state,action,next_state,reward)
        Q_student = student_function(Q_student,state,action,next_state,reward)
        if not np.array_equal(Q_student,Q_correct):
            print("update_q creates incorrect updates")
            break
    if np.array_equal(Q_student, Q_correct):
      print("update_q creates correct updates")
    return