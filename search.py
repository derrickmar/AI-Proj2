"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import sys
import logic

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostSearchProblem)
        """
        util.raiseNotDefined()

    def terminalTest(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionSearchProblem
        """
        util.raiseNotDefined()

    def result(self, state, action):
        """
        Given a state and an action, returns resulting state and step cost, which is
        the incremental cost of moving to that successor.
        Returns (next_state, cost)
        """
        util.raiseNotDefined()

    def actions(self, state):
        """
        Given a state, returns available actions.
        Returns a list of actions
        """        
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

    def getWidth(self):
        """
        Returns the width of the playable grid (does not include the external wall)
        Possible x positions for agents will be in range [1,width]
        """
        util.raiseNotDefined()

    def getHeight(self):
        """
        Returns the height of the playable grid (does not include the external wall)
        Possible y positions for agents will be in range [1,height]
        """
        util.raiseNotDefined()

    def isWall(self, position):
        """
        Return true if position (x,y) is a wall. Returns false otherwise.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def atLeastOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that at least one of the expressions in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"
    cnf_ans = expressions[0]
    if len(expressions) > 1:
        for e in expressions[1:]:
            cnf_ans = cnf_ans | e
    # print cnf_ans
    return cnf_ans

def atMostOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that at most one of the expressions in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)  --> A V B
    >>> model1 =  {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    False
    >>> model4 = {A:True, B:True, C:False}
    >>> print logic.pl_true(atleast1,model2)
    False
    """
    initial = expressions[0]
    cnf_ans = initial | ~initial
    for i in range(len(expressions)):
        for j in range(i, len(expressions)):
            if i == j:
                continue
            curr = ~expressions[i] | ~expressions[j]
            cnf_ans &= curr
    # print cnf_ans
    return cnf_ans

def exactlyOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that exactly one of the expressions in the list is true.
      >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 =    
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    False
    >>> model4 = {A:True, B:True, C:False}
    >>> print logic.pl_true(atleast1,model2)
    False
    """
    # xor implementation
    # cnf_ans = expressions[0]
    # if len(expressions) > 1:
    #     for e in expressions[1:]:
    #         cnf_ans = cnf_ans ^ e
    # print cnf_ans
    # return cnf_ans

    # CNF correct implementation
    initial = expressions[0]
    cnf_ans = initial | ~initial
    appendCantAllBeFalse = initial & ~initial
    for i in range(len(expressions)):
        appendCantAllBeFalse |= expressions[i]
        for j in range(i, len(expressions)):
            if i == j:
                continue
            curr = ~expressions[i] | ~expressions[j]
            cnf_ans &= curr
    # print appendCantAllBeFalse
    cnf_ans &= appendCantAllBeFalse
    # print cnf_ans
    return cnf_ans

def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', "", 'North']
    """
    # list_of_valid_actions = []
    # for key, value in model.iteritems():
    #     # some python data structure
    #     maximum = 0
    #     if value:
    #         action_and_info = logic.PropSymbolExpr.parseExpr(key)
    #         if action_and_info[0] in actions:
    #             current_timestep = 0
    #             if action_and_info[1] is tuple:
    #                 print "action and info is tuple!!"
    #                 print action_and_info[1]
    #                 current_timestep = action_and_info[1][2]
    #             else: 
    #                 current_timestep = action_and_info[1]
    #             if maximum < current_timestep:
    #                 maximum = current_timestep
    #             list_of_valid_actions.append(action_and_info)

    # for valids in list_of_valid_actions:
    list_of_valid_actions = []
    # iterate through the key and values of a model
    # logic.PropSymbolExpr.parseExpr(expr), which returns a tuple in the form of ("North", "3")
    for key, value in model.iteritems():
        # if the value is Tru
        if value:
            action_and_info = logic.PropSymbolExpr.parseExpr(key)
            if action_and_info[0] in actions:
                list_of_valid_actions.append(action_and_info)
    # [('South', '0'), ('West', '1')]
    # print list_of_valid_actions
    ans = []
    for num in range(len(list_of_valid_actions)):
        # print num
        for valid in list_of_valid_actions:
            if int(valid[1]) == num:
                ans.append(valid[0])
    return ans
    # are the P key and valuse even used

def positionLogicPlan(problem):
    """
    Given an instance of a PositionSearchProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    sym = logic.PropSymbolExpr
    time = 0
    time_max = 50
    kb = []
    initialState = problem.getStartState()
    goalState = problem.getGoalState()

    # get the legalStates (everything but walls)
    legalStates = []
    walls = problem.walls.asList()
    for x in range(1, problem.getWidth() + 1):
        for y in range(1, problem.getHeight() + 1):
            position = (x, y)
            if position not in walls:
                legalStates.append(position)

    initialConstraint = sym("P", initialState[0], initialState[1], time)

    # GENERATE AND APPEND INITIAL CONSTRAINT
    # P[2,2,0] & ~P[2,1,0] & ~P[1,2,0] & ~P[1,1,0]
    for legalState in legalStates:
        if legalState == initialState:
            continue
        else:
            initialConstraint &= ~sym("P", legalState[0], legalState[1], time)
    # kb.append(initialConstraint)
    kb.append(logic.to_cnf(initialConstraint))
    print "INITIAL CONSTRAINT"
    print initialConstraint

    #next_states = [ P[2,2,1] ]

    next_states = [initialState]
    for t in range(time, time_max):
        print "TTTTTTTTTTTTTTT"
        print t
        print "NEXT_STATES"
        print next_states

        symbolActions = []
        actions = ['North', 'South', 'East', 'West']
        for action in actions:
            symbolActions.append(sym(action, t))
        kbActions = exactlyOne(symbolActions)
        print "kbACTIONS"
        print kbActions
        # kb.append(kbActions)
        kb.append(logic.to_cnf(kbActions))

        # ADD GOAL STATE
        # (((P[1,1,0] & ~P[1,2,0]) & ~P[2,1,0]) & ~P[2,2,0])
        # goalConstraint = sym("P", goalState[0], goalState[1], t)
        # for legalState in legalStates:
        #     if legalState == goalState:
        #         continue
        #     else:
        #         # (((P[1,1,1] & ~P[1,2,0]) & ~P[2,1,0]) & ~P[2,2,0])
        #         goalConstraint &= ~sym("P", legalState[0], legalState[1], t)
        # # should already be in kb format
        # kb.insert(0, logic.to_cnf(goalConstraint))
        # print "GOAL CONSTRAINT"
        # print goalConstraint


        # Add successor axioms and generate children for next_states
        # add P[1,1,T] & ~P[2,1,T] & ~P[1,2,T] & ~P[1,1,T] & (P(2,2,0) & South[0] <=> P[2,1,1]) & 
        list_of_successors = {}
        # list_of_successor_state_axioms = []
        kb_successors = []

        for state in next_states:
            actions = problem.actions(state)

            # TODO: not sure if our existing exactlyOne method will work

            # another for loop to add successor constraints
            parent_state = sym("P", state[0], state[1], t)

            for action in actions:
                successor, cost = problem.result(state, action)

                kb_successor = sym("P", successor[0], successor[1], t + 1)
                kb_action = sym(action, t)

                if kb_successor in list_of_successors.keys():
                    list_of_successors[kb_successor].append((kb_action, parent_state))
                    print "list_of_successors"
                    print list_of_successors
                else:
                    kb_successors.append(kb_successor)
                    list_of_successors[kb_successor] = [(kb_action, parent_state)]
                    print "list_of_successors"
                    print list_of_successors

                # successor_state_axiom = logic.Expr('<=>', (parent_state & kb_action), kb_successor)
                # print successor_state_axiom
                # list_of_successor_state_axioms.append(successor_state_axiom)
                # kb.append(logic.to_cnf(successor_state_axiom))

        print "KB_SUCCESSORS"
        print kb_successors
        kb.append(logic.to_cnf(exactlyOne(kb_successors)))
        # attempt to add combinational ssa after you have all the actions
        # print 'YAY'
        for succ, actions_and_parents in list_of_successors.iteritems():
            if len(actions_and_parents) < 2:
                print "SUCCESSOR STATE AXIOM" # successor state axioms that has only one way to get to the goal
                s = logic.Expr('<=>', (actions_and_parents[0][1] & actions_and_parents[0][0]), succ)
                print s
                kb.append(logic.to_cnf(s))
            else:
                initial = (actions_and_parents[0][0] & actions_and_parents[0][1])
                # print initial
                for tup in actions_and_parents[1:]:
                    initial |= (tup[0] & tup[1])

                comb_ssa = logic.Expr('<=>', initial, succ)
                kb.append(logic.to_cnf(exactlyOne([comb_ssa])))
                # kb.append(logic.to_cnf(comb_ssa))
                print "COMB_SSA" # combinational successor state axioms
                print comb_ssa

            #  P(2,1,1) & North[1] V P(1,2,1) & East[1] <=> P[2,2,2]
        model = logic.pycoSAT(kb)
        print 'MODEL'
        print model
        if model:
            answer = extractActionSequence(model, ['North', 'South', 'East', 'West'])
            return answer
            # print 'answer'
            # print answer
            # if answer == []:
            #     continue
            # else:
            #     return answer
        else:
            next_states = []
            for successor, actions_and_parents in list_of_successors.iteritems():
                ns = (successor.getIndex()[0], successor.getIndex()[1])
                # if case here to remove dupicate states
                if ns not in next_states:
                    next_states.append(ns)
            kb.pop(0) # remove the goal constraint for this timeste[]

    return false


def foodLogicPlan(problem):
    """
    Given an instance of a FoodSearchProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    #  Initial Position of Pacman / Where he isn't
    # Food constraint, the food has been eaten if pacman has been there

    sym = logic.PropSymbolExpr
    time = 0
    time_max = 50
    kb = []
    initialState_w_food = problem.getStartState()
    initialState = initialState_w_food[0]
    foodList = initialState_w_food[1].asList()
    goalState = problem.getGoalState()

    # get the legalStates (everything but walls)
    legalStates = []
    walls = problem.walls.asList()
    for x in range(1, problem.getWidth() + 1):
        for y in range(1, problem.getHeight() + 1):
            position = (x, y)
            if position not in walls:
                legalStates.append(position)

    import pdb; pdb.set_trace()

    initialConstraint = sym("P", initialState[0], initialState[1], time)

    # GENERATE AND APPEND INITIAL CONSTRAINT
    # P[2,2,0] & ~P[2,1,0] & ~P[1,2,0] & ~P[1,1,0]
    for legalState in legalStates:
        if legalState == initialState:
            continue
        else:
            initialConstraint &= ~sym("P", legalState[0], legalState[1], time)
    # kb.append(initialConstraint)
    kb.append(logic.to_cnf(initialConstraint))
    print "INITIAL CONSTRAINT"
    print initialConstraint

    #next_states = [ P[2,2,1] ]

    next_states = [initialState]
    for t in range(time, time_max):
        print "TTTTTTTTTTTTTTT"
        print t
        print "NEXT_STATES"
        print next_states

        symbolActions = []
        actions = ['North', 'South', 'East', 'West']
        for action in actions:
            symbolActions.append(sym(action, t))
        kbActions = exactlyOne(symbolActions)
        print "kbACTIONS"
        print kbActions
        # kb.append(kbActions)
        kb.append(logic.to_cnf(kbActions))

        # ADD GOAL STATE
        # (((P[1,1,0] & ~P[1,2,0]) & ~P[2,1,0]) & ~P[2,2,0])
        if len(foodList) > 0:
            goalConstraint = foodList[0]

            for legalState in legalStates:
                if legalState not in foodList and legalState != foodList[0]:
                    continue
                else:
                    goalConstraint &= ~sym("F", legalState[0], legalState[1], t)

        # should already be in kb format
        kb.insert(0, logic.to_cnf(goalConstraint))
        print "GOAL CONSTRAINT"
        print goalConstraint
        # import pdb; pdb.set_trace()

        # Add successor axioms and generate children for next_states
        # add P[1,1,T] & ~P[2,1,T] & ~P[1,2,T] & ~P[1,1,T] & (P(2,2,0) & South[0] <=> P[2,1,1]) & 
        list_of_successors = {}
        # list_of_successor_state_axioms = []
        kb_successors = []

        for state in next_states:
            actions = problem.actions(state)

            # TODO: not sure if our existing exactlyOne method will work

            # another for loop to add successor constraints
            parent_state = sym("P", state[0], state[1], t)

            for action in actions:
                successor, cost = problem.result(state, action)

                kb_successor = sym("P", successor[0], successor[1], t + 1)
                kb_action = sym(action, t)

                if kb_successor in list_of_successors.keys():
                    list_of_successors[kb_successor].append((kb_action, parent_state))
                    print "list_of_successors"
                    print list_of_successors
                else:
                    kb_successors.append(kb_successor)
                    list_of_successors[kb_successor] = [(kb_action, parent_state)]
                    print "list_of_successors"
                    print list_of_successors

                # successor_state_axiom = logic.Expr('<=>', (parent_state & kb_action), kb_successor)
                # print successor_state_axiom
                # list_of_successor_state_axioms.append(successor_state_axiom)
                # kb.append(logic.to_cnf(successor_state_axiom))

        print "KB_SUCCESSORS"
        print kb_successors
        kb.append(logic.to_cnf(exactlyOne(kb_successors)))
        # attempt to add combinational ssa after you have all the actions
        # print 'YAY'
        for succ, actions_and_parents in list_of_successors.iteritems():
            if len(actions_and_parents) < 2:
                print "SUCCESSOR STATE AXIOM" # successor state axioms that has only one way to get to the goal
                s = logic.Expr('<=>', (actions_and_parents[0][1] & actions_and_parents[0][0]), succ)
                print s
                kb.append(logic.to_cnf(s))
            else:
                initial = (actions_and_parents[0][0] & actions_and_parents[0][1])
                # print initial
                for tup in actions_and_parents[1:]:
                    initial |= (tup[0] & tup[1])

                comb_ssa = logic.Expr('<=>', initial, succ)
                kb.append(logic.to_cnf(exactlyOne([comb_ssa])))
                # kb.append(logic.to_cnf(comb_ssa))
                print "COMB_SSA" # combinational successor state axioms
                print comb_ssa

            #  P(2,1,1) & North[1] V P(1,2,1) & East[1] <=> P[2,2,2]
        model = logic.pycoSAT(kb)
        print 'MODEL'
        print model
        if model:
            answer = extractActionSequence(model, ['North', 'South', 'East', 'West'])
            return answer
            # print 'answer'
            # print answer
            # if answer == []:
            #     continue
            # else:
            #     return answer
        else:
            next_states = []
            for successor, actions_and_parents in list_of_successors.iteritems():
                ns = (successor.getIndex()[0], successor.getIndex()[1])
                # if case here to remove dupicate states
                if ns not in next_states:
                    next_states.append(ns)
            kb.pop(0) # remove the goal constraint for this timeste[]

def foodGhostLogicPlan(problem):
    """
    Given an instance of a FoodGhostSearchProblem, return a list of actions that help Pacman
    eat all of the food and avoid patrolling ghosts.
    Ghosts only move east and west. They always start by moving East, unless they start next to
    and eastern wall. 
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan
fglp = foodGhostLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)



