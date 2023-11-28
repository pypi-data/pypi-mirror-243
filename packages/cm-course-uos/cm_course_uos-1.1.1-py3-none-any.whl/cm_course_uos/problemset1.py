"""
authors: Sebastian Musslick (smusslick@uos.de),
         Deniz M. Gun (dguen@uos.de)

This module contains helper and test functions for Problemset 1
 of the course "Cognitive Modeling" at the University of Osnabrueck.
 This module exists in order to load certain functionality into the 
 assignment notebooks without involuntarily giving students access to
 solutions.
"""
import numpy as np
import random
import pandas as pd


def compute_valence(deck_result, w):
    '''
    This function computes the valence as denoted in the notebook script.

    Input arguments:
      deck_result: The result of the selected deck (in points)
      W: The valence parameter
    '''

    # first compute win and loss depending on points received
    if deck_result > 0:
        win = deck_result
        loss = 0
    else:
        win = 0
        loss = deck_result

    # compute valence term
    valence = w * win + (1-w) * loss  # YOUR ANSWER GOES HERE

    return valence


def test_compute_valence(student_valence, print_feedback=True):
    """ Returns True if The student implemented 
    valence function returns same values as the correct solution.

    Args
        student_valence (method) :  
            The compute_valence method defined in the notebook and edited by students.
        print_feedback (bool) : 
            If True, this method prints feedback to the console.
    Returns
        correct (bool): 
            True, if student_valence returns the same values as compute_valence
    """

    correct = True

    # Search for all reck rewards between -25 and 10
    for deck_result in range(-25, 10, 1):
        for w in range(11):
            w = w/10  # scaling w to [0,1]
            student_result = student_valence(deck_result, w)
            correct_result = compute_valence(deck_result, w)

            if student_result != correct_result:
                correct = False
                break

        if not correct:
            break  # exit search

    if not print_feedback:
        return correct

    if correct:
        print("Your compute_valence function creates correct outputs!")
    else:
        print(
            "Your compute_valence function generates incorrect outputs. Check for mistakes.")
    return correct


def compute_expectancy(previous_expectancy, alpha, valence):
    '''
    This function computes the expectancy as denoted above.

    Input arguments:
      previous_expectancy: expectancy of current deck on previous trial
      alpha: update parameter
      valence: valence of current deck on current trial
    '''

    # compute expectancy term
    new_expectancy = (1-alpha) * previous_expectancy + \
        alpha * valence  # YOUR ANSWER GOES HERE
    return new_expectancy


def test_compute_expectancy(student_expectancy, print_feedback=True):
    """ Returns True if The student implemented
    expectancy function returns same values as the correct solution.

    Args
        student_expectancy (method) :
            The compute_expectancy method defined in the notebook and edited by students.
        print_feedback (bool) :
            If True, this method prints feedback to the console.
    Returns
        correct (bool):
            True, if student_expectancy returns the same values as compute_expectancy
    """

    correct = True

    for previous_expectancy in range(-10, 10, 1):
        for alpha in range(11):
            alpha = alpha / 10  # scaling to [0,1]
            for valence in range(11):
                valence = valence/10  # scaling to [0,1]
                student_result = student_expectancy(
                    previous_expectancy, alpha, valence)
                correct_result = compute_expectancy(
                    previous_expectancy, alpha, valence)

                if student_result != correct_result:
                    correct = False
                    break

        if not correct:
            break  # exit search

    if not print_feedback:
        return correct

    if correct:
        print("Your compute_expectancy function creates correct outputs!")
    else:
        print(
            "Your compute_expectancy function generates incorrect outputs. Check for mistakes.")
    return correct


def compute_choice_probabilities(expectancies, trial_number, c):
    '''
    This function computes the choice probabilities for each deck based on the
    current expectancies

    Input arguments:
      expectancies: a list of expectancies for all four decks
      trial_number: number of the current trial
      c: parameter used to compute beta
    '''
    # compute beta
    beta = pow((trial_number+1)/10, c)

    # compute softmaxed choice proabbilities
    # YOUR ANSWER GOES HERE
    choice_probs = np.exp(expectancies * beta) / \
        np.sum(np.exp(expectancies * beta))

    return choice_probs


def test_compute_choice_probs(student_choice_probabilities, print_feedback=True):
    """ Returns True if The student implemented
    choice probability function returns same values as the correct solution.

    Args
        student_choice_probabilities (method) :
            The compute_choice_probabilities method defined in the notebook and edited by students.
        print_feedback (bool) :
            If True, this method prints feedback to the console.
    Returns
        correct (bool):
            True, if student_choice_probabilities returns the same values as compute_choice_probabilities
    """

    correct = True

    for expectancy_idx in range(11):
        for trial_number in range(11):
            for c in np.linspace(-2, 2, 11):

                expectancies = np.array([np.random.randint(-5, 5),
                                        np.random.randint(-5, 5),
                                        np.random.randint(-5, 5),
                                         np.random.randint(-5, 5)])
                student_result = student_choice_probabilities(
                    expectancies, trial_number, c)
                correct_result = compute_choice_probabilities(
                    expectancies, trial_number, c)

                for choice in range(len(student_result)):
                    if np.round(student_result[choice], decimals=8) != np.round(correct_result[choice], decimals=8):
                        correct = False
                        break

        if not correct:
            break  # exit search

    if not print_feedback:
        return correct

    if correct:
        print("Your compute_choice_probabilities function creates correct outputs!")
    else:
        print(
            "Your compute_choice_probabilities function generates incorrect outputs. Check for mistakes.")
    return correct


def compute_choice(expectancies, trial_number, c):
    '''
    This function computes the index of the chosen deck for the next trial

    Input arguments:
      expectancies: a list of expectancies for all four decks
      trial_number: number of the current trial
      c: parameter used to compute beta
    '''

    # compute softmaxed choice proabbilities
    choice_probs = compute_choice_probabilities(expectancies, trial_number, c)

    # compute cumulated sums
    cumulated_choice_probs = np.cumsum(choice_probs)

    # draw random number between 0 and 1
    random_number = random.random()

    # choose deck index depending on choice probabilities
    index = 0

    # Iterate through the cumulative sums to find the first index where the random number exceeds the cumulative sum
    while index < len(cumulated_choice_probs) and random_number > cumulated_choice_probs[index]:
        index += 1

    return index


def observe_deck_result(wins, losses, win_probability, choice):
    '''
    This function returns the outcome of choosing a deck.

    Input arguments:
      wins: wins for Decks A, B, C, and D
      losses: losses for Decks A, B, C, and D
      win_probability: chance of obtaining a win from a deck
      choice: the index of the chosen deck (0: A, 1: B, 2: C, 3: D)
    '''
    random_number = random.random()
    if random_number <= win_probability:
        return wins[choice]
    else:
        return losses[choice]


def log_data(df, trial_number, expectancies, choice, wins, losses, deck_result):
    '''
    This function logs several outcomes of the simulation into a data frame.

    Input arguments:
      df: a Pandas dataframe in which we write the data
      trial_index: current trial number
      expectancies: expectancies of all decks
      choice: the index of the chosen deck (0: A, 1: B, 2: C, 3: D)
      wins: wins for Decks A, B, C, and D
      losses: losses for Decks A, B, C, and D
      deck_result: the value obtained from choosing the deck
    '''
    if wins[choice] == np.min(wins):
        type = "safe"
    else:
        type = "risky"

    new_row = pd.DataFrame({'trial_index': trial_number,
                            'E(A)': expectancies[0],
                            'E(B)': expectancies[1],
                            'E(C)': expectancies[2],
                            'E(D)': expectancies[3],
                            'choice_index': choice,
                            'type': type,
                            'reward': wins[choice],
                            'penalty': losses[choice],
                            'value': deck_result}, index=[0])

    df = pd.concat([df, new_row], axis=0, ignore_index=True)
    return df


def simulate_model(num_trials, wins, losses, win_probability, W, alpha, c):
    '''
    This function simulates the expectancy valence model for a certain number of trials.
    It returns a dataframe with simulation results.

    Input arguments:
      wins: wins for Decks A, B, C, and D
      losses: losses for Decks A, B, C, and D
      win_probability: chance of obtaining a win from a deck
      W: the valence parameter
      alpha: the update parameter
      c: parameter used to compute the softmax parameter beta
    '''
    # initialize the model
    expectancies = np.zeros(4)

    # we will log the entire simulation in a dataframe
    df = pd.DataFrame(columns=['trial_index', 'E(A)', 'E(B)',
                      'E(C)', 'E(D)', 'choice_index', 'type', 'value'])

    for trial_number in range(num_trials):

        # make a choice
        chosen_deck_index = compute_choice(expectancies, trial_number, c)

        # REPLACE: problemset1.compute_choice
        # YOUR ANSWER GOES HERE
        # Hint: You may use the functions observe_deck_result, compute_valence, and compute_expectancy
        # If your compute_valence and compute_expectancy don't pass the tests above, then you may use
        # the problemset1.compute_valence and problemset1.compute_expectancy functions instead (they have
        # the same inputs and outputs).

        # observe an outcome
        deck_result = observe_deck_result(
            wins, losses, win_probability, chosen_deck_index)

        # compute valence
        valence = compute_valence(deck_result, W)

        # update expectancy of chosen deck
        expectancies[chosen_deck_index] = compute_expectancy(
            expectancies[chosen_deck_index], alpha, valence)

        # log results
        df = log_data(df, trial_number, expectancies,
                      chosen_deck_index, wins, losses, deck_result)

    return df


def test_simulate_model(student_simulate_model, print_feedback=True):
    """ Returns True if The student implemented
    simulate model function returns same values as the correct solution.

    Args
        simulate_model (method) :
            The simulate_models method defined in the notebook and edited by students.
        print_feedback (bool) :
            If True, this method prints feedback to the console.
    Returns
        correct (bool):
            True, if simulate_model returns the same values as simulate_model
    """

    correct = True

    wins = [5, 10, 10, 5]  # wins for Decks A, B, C, and D
    losses = [-5, -25, -25, -5]  # losses for Decks A, B, C, and D
    win_probability = 0.5  # chance of obtaining a win from a deck
    num_trials = 20

    for W in np.linspace(0, 1, 4):
        for alpha in np.linspace(0, 1, 4):
            for c in np.linspace(-1, 1, 4):

                random.seed(1)
                student_result = student_simulate_model(
                    num_trials, wins, losses, win_probability, W, alpha, c)
                random.seed(1)
                correct_result = simulate_model(
                    num_trials, wins, losses, win_probability, W, alpha, c)

                if student_result.equals(correct_result) is False:
                    correct = False
                    break

        if not correct:
            break  # exit search

    if not print_feedback:
        return correct

    if correct:
        print("Your simulate_model function creates correct outputs!")
    else:
        print(
            "Your simulate_model function generates incorrect outputs. Check for mistakes.")
    return correct


def compute_log_likelihood(df, W, alpha, c):
    '''
    This function computes the log likelihood for a given set of model parameters

    Input arguments:
      df: data frame
      W: the valence parameter
      alpha: the update parameter
      c: parameter used to compute the softmax parameter beta
    '''
    # initialize log likelihood
    LL = 0

    # initialize the model
    expectancies = np.zeros(4)

    num_trials = len(df)

    for trial_number in range(num_trials):

        # when computing the likelihood, we don't need to make a choice
        # instead, we observe the choice from the data
        chosen_deck_index = df['choice_index'][trial_number]

        # next, we compute the log likelihood of that choice given the model and its parameters
        # the log likelihood is simply the log of the probability of choosing the current deck

        choice_probabilities = compute_choice_probabilities(
            expectancies, trial_number, c)

        # YOUR ANSWER GOES HERE
        LL = LL + np.log(choice_probabilities[chosen_deck_index])

        # next, we observe the result obtained from that trial and compute the valence
        deck_result = df['value'][trial_number]

        # compute valence
        valence = compute_valence(deck_result, W)

        # update expectancy of chosen deck
        expectancies[chosen_deck_index] = compute_expectancy(
            expectancies[chosen_deck_index], alpha, valence)

    return LL


def test_compute_log_likelihood(student_compute_log_likelihood, print_feedback=True):
    """ Returns True if The student implemented
    a compute_log_likelihood function that returns same values as the correct solution.

    Args
        compute_log_likelihood (method) :
            The student_compute_log_likelihood method defined in the notebook and edited by students.
        print_feedback (bool) :
            If True, this method prints feedback to the console.
    Returns
        correct (bool):
            True, if student_compute_log_likelihood returns the same values as compute_log_likelihood
    """

    correct = True

    wins = [5, 10, 10, 5]  # wins for Decks A, B, C, and D
    losses = [-5, -25, -25, -5]  # losses for Decks A, B, C, and D
    win_probability = 0.5  # chance of obtaining a win from a deck
    num_trials = 20

    for W in np.linspace(0, 1, 4):
        for alpha in np.linspace(0, 1, 4):
            for c in np.linspace(-1, 1, 4):

                wins = [5, 10, 10, 5]  # wins for Decks A, B, C, and D
                losses = [-5, -25, -25, -5]  # losses for Decks A, B, C, and D
                win_probability = 0.5  # chance of obtaining a win from a deck
                num_trials = 20
                random.seed(1)
                df = simulate_model(num_trials, wins, losses,
                                    win_probability, W, alpha, c)

                student_result = student_compute_log_likelihood(
                    df, W, alpha, c)
                correct_result = compute_log_likelihood(df, W, alpha, c)

                if np.round(student_result, decimals=8) != np.round(correct_result, decimals=8):
                    correct = False
                    break

        if not correct:
            break  # exit search

    if not print_feedback:
        return correct

    if correct:
        print("Your compute_log_likelihood function creates correct outputs!")
    else:
        print(
            "Your compute_log_likelihood function generates incorrect outputs. Check for mistakes.")
    return correct


def test_parameter_fit(df,
                       c_values,
                       W_values,
                       alpha_values,
                       student_LL,
                       student_c,
                       student_W,
                       student_alpha,
                       print_feedback=True):
    """ Returns True if computed the correct likelihood values for their data.

    Args
        df (pandas.DataFrame) :
            Student's data.
        c_values (list) :
            List of c values to test.
        W_values (list) :
            List of W values to test.
        alpha_values (list) :
            List of alpha values to test.
        student_LL (pandas.DataFrame) :
            Student's data.
        student_LL (float) :
            Student's log likelihood value
        student_c (float) :
            Student's fitted c value
        student_W (float) :
            Student's fitted W value
        student_alpha (float) :
            Student's fitted alpha value
        print_feedback (bool) :
            If True, this method prints feedback to the console.
    Returns
        correct (bool):
            True, if the student's likelihood and parameter values are correct.
    """

    correct = True

    # initialize log-likelihood and fitted parameters
    best_LL = -10000
    best_c = 0
    best_W = 0
    best_alpha = 0

    for c_idx, c in enumerate(c_values):
        for W_idx, W in enumerate(W_values):
            for alpha_idx, alpha in enumerate(alpha_values):

                LL = compute_log_likelihood(df, W, alpha, c)
                if LL > best_LL:
                    best_c = c
                    best_W = W
                    best_alpha = alpha
                    best_LL = LL

    if np.round(student_LL, decimals=8) != np.round(best_LL, decimals=8):
        correct = False
        print("Your log likelihood is incorrect.")
    if np.round(student_c, decimals=8) != np.round(best_c, decimals=8):
        correct = False
        print("Your c value is incorrect.")
    if np.round(student_W, decimals=8) != np.round(best_W, decimals=8):
        correct = False
        print("Your W value is incorrect.")
    if np.round(student_alpha, decimals=8) != np.round(best_alpha, decimals=8):
        correct = False
        print("Your alpha value is incorrect.")

    if not print_feedback:
        return correct

    if correct:
        print("Your compute_log_likelihood function creates correct outputs!")
    else:
        print(
            "Your compute_log_likelihood function generates incorrect outputs. Check for mistakes.")
    return correct
