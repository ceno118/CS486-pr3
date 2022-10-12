# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        '''
        I'm defining self.bestActions to hold the best action for a given state, so it can be more easily accessed later
        '''

        self.bestActions = {state:None for state in self.mdp.getStates()}

        for i in range(self.iterations):
            new_vals = util.Counter() #added based on source below
            '''
            https://github.com/YidaYin/Berkeley-CS188-Project-3/blob/master/valueIterationAgents.py
            I was originally just updating self.values whenever the q was greater than the current max (lines 70-73) but this
            wasn't working and I wasn't sure why. I found this and saw why I needed to reset the values each time using
            a new util.Counter (new_vals). As this source is a complete solution to the project, I plan to only use it
            if I'm completely stuck.
            '''
            states = self.mdp.getStates()
            for state in states:
                legalActions = self.mdp.getPossibleActions(state)
                max = float("-inf")
                for action in legalActions:
                    q = self.computeQValueFromValues(state, action)
                    if q > max:
                        max = q
                        new_vals[state] = max #used source described above to change from self.values[state] to new_vals[state]
                        self.bestActions[state] = action
            self.values = new_vals #added based on above source
    

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        q = 0
        tStatesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
        for successor, p in tStatesAndProbs:
            q += p * (self.mdp.getReward(state, action, successor) + self.values[successor] * self.discount)
        return q


        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        # because self.actions stores the best action for a state, we can just return from it

        return self.bestActions[state]

        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
