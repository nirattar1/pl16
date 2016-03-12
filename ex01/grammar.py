"""
This module contains functions for analyzing a grammar, finding
its NULLABLE, FIRST, FOLLOW and SELECT sets, and determining if it is
LL(1).

A grammar is represented as a list of rules of the form (head, body)
where head is the goal non-terminal, and body is a tuple of symbols,
or the empty tuple () for an epsilon rule.

The start symbol is always the head of the first rule in the list.
"""

from symbols import *


grammar_recitation = [
    (S, (ID, ASSIGN, E)),              # S -> id := E
    (S, (IF, LP, E, RP, S, ELSE, S)),  # S -> if (E) S else S
    (E, (T, EP)),                      # E -> T EP
    (T, (ID,)),                        # T -> id
    (T, (LP, E, RP)),                  # T -> (E)
    (EP, ()),                          # EP -> epsilon
    (EP, (PLUS, E)),                   # EP -> + E
]


#### test grammar - E has nullable start (T)
##grammar_recitation = [
##    (S, (ID, ASSIGN, E)),              # S -> id := E
##    (S, (IF, LP, E, RP, S, ELSE, S)),  # S -> if (E) S else S
##    (E, (T, EP)),                      # E -> T EP
##    (T, (ID,)),                        # T -> id
##    (T, (LP, E, RP)),                  # T -> (E)
##    (T, ()),                           # T -> epsilon
##    (EP, ()),                          # EP -> epsilon
##    (EP, (PLUS, E)),                   # EP -> + E
##]



def calculate_nullable(terminals, nonterminals, grammar):
    """
    Return the set of nullable nonterminals in the given grammar.

    terminals and nonterminals are sets, grammer is a list of rules as
    explained above.

    --- DO NOT MODIFY THIS FUNCTION ---
    """
    nullable = set()
    for head, body in grammar:
        if body == ():
            nullable.add(head)
    changing = True
    while changing:
        changing = False
        for head, body in grammar:
            if set(body) <= nullable and head not in nullable:
                nullable.add(head)
                changing = True
    return nullable


def calculate_first(terminals, nonterminals, grammar, nullable):
    """
    Return a dictionary mapping terminals and nonterminals to their FIRST set
    """
    first = dict()
    for t in terminals:
        first[t] = {t}
    for a in nonterminals:
        first[a] = set()
    changing = True
    while changing:
        changing = False
        
	#for each rule A -> A1, ... , An
        for head, body in grammar:
  
            #try iterating on all nullable starts .
            for i in range(0, len(body)) :
                #print body [0:i]
                my_set = set (body [0:i])
                #add first(i) to first (A), if all starts before i are nullable
                #this includes the first symbol.
                if (my_set <= nullable and len(my_set)>0) or (i==0):

##                    #debug print
##                    if (i>0):
##                        print "this start is nullable" , my_set
##                        
		    #add 'first' of next token to first of this rule.
##                    print "add to first of group : ", head , ". group is:",  first[head]
##                    print "new member is : ", first [body[i]]
                    if not (first [body[i]] <= first[head]):
                        first[head] = first[head] | first [body[i]]
##                        print "set after change : ",  first[head]
                        changing = True
        				
            
    return first


def calculate_follow(terminals, nonterminals, grammar, nullable, first):
    """
    Return a dictionary mapping terminals and nonterminals to their FOLLOW set
    """
    follow = dict()
    for a in nonterminals:
        follow[a] = set()
    start_nonterminal = grammar[0][0]
    follow[start_nonterminal] = {EOF}
    changing = True
    while changing:
        changing = False
        
        #for each rule A -> A1, ... , An
        for head, body in grammar:

            #iterate on all possible endings of rule A.
            #if ending is nullable then follow(A) can be added to Ai
            for i in range(0, len(body)) :
                ending = set (body [i+1:len(body)])
                #print ending
                
                if (ending <= nullable ) :
                    #print "the ending " , ending , "is nullable"
                    #add follow (A) to follow (Ai)
                    if (body[i] in nonterminals) and not (follow[head] <= follow [body[i]]):
                        #print "adding", follow[head]
                        follow [body[i]] = follow [body[i]] | follow[head]
                        changing = True
                    
            #iterate on all starts
            n = len(body)
            for i in range(0, n-1) :   #0 to n-2
                #print "i:",i
                for j in range (i+1, n):
                    #print "j:",j
                    null_prefix = set (body [i+1:j])
                    #print "rule:" , body
                    #print "prefix: " , null_prefix
                    if (null_prefix <= nullable):
                        #add first (Aj) to follow (Ai)
                        #print "body[j]", body[j]
                        #print "body[i]", body[i]
                        if (body[i] in nonterminals) and not (first[body[j]] <= follow [body[i]]):
                            follow [body[i]] = follow [body[i]] | first[body[j]]
                            changing = True

    return follow


def calculate_select(terminals, nonterminals, grammar, nullable, first, follow):
    """
    Return a dictionary mapping rules to their SELECT (a.k.a. PREDICT) set
    """
    select = dict()
    #print "nullable: ", nullable
    for head, body in grammar:
        #print body

        
        #calculate "first" of body.
        firstbody = set()
        for i in range(0,len(body)):
            prefix = set (body [0:i])
            #add first(Ai) to first of body, if all starts before Ai are nullable
            #this includes the first symbol.
            if (prefix <= nullable and len(prefix)>0) or (i==0):
                firstbody = firstbody | first [body[i]]

                
        if not (set(body) <= nullable):
            #print "body is not nullable"
            select [(head, body)] = firstbody
        else:
            select [(head, body)] = firstbody | follow [head]
            #print "body is nullable"
        
    return select


def format_rule(r):
    """
    --- DO NOT MODIFY THIS FUNCTION ---
    """
    return "{} -> {}".format(r[0], ' '.join(r[1]))


def find_terminals_and_nonterminals(grammar):
    """
    Find the terminals and nonterminals appearing in the given grammar.

    --- DO NOT MODIFY THIS FUNCTION ---
    """
    symbols = set()
    nonterminals = set()
    for head, body in grammar:
        nonterminals.add(head)
        symbols.update(body)
    terminals = symbols - nonterminals
    return terminals, nonterminals


def analyze_grammar(grammar):
    """
    Use other functions in this module to analyze the grammar and
    check if it is LL(1).

    --- DO NOT MODIFY THIS FUNCTION ---
    """
    print "Analyzing grammar:"
    for r in grammar:
        print "    " + format_rule(r)
    print

    terminals, nonterminals = find_terminals_and_nonterminals(grammar)
    print "terminals = ", terminals
    print "nonterminals = ", nonterminals
    print

    nullable = calculate_nullable(terminals, nonterminals, grammar)
    print "nullable = ", nullable
    print

    first = calculate_first(terminals, nonterminals, grammar, nullable)
    for k in sorted(first.keys()):
        print "first({}) = {}".format(k, first[k])
    print

    follow = calculate_follow(terminals, nonterminals, grammar, nullable, first)
    for k in sorted(follow.keys()):
        print "follow({}) = {}".format(k, follow[k])
    print

    select = calculate_select(terminals, nonterminals, grammar, nullable, first, follow)
    for k in sorted(select.keys()):
        print "select({}) = {}".format(format_rule(k), select[k])
    print

    ll1 = True
    n = len(grammar)
    for i in range(n):
        for j in range(i+1, n):
            r1 = grammar[i]
            r2 = grammar[j]
            if r1[0] == r2[0] and len(select[r1] & select[r2]) > 0:
                ll1 = False
                print "Grammar is not LL(1), as the following rules have intersecting SELECT sets:"
                print "    " + format_rule(r1)
                print "    " + format_rule(r2)
    if ll1:
        print "Grammar is LL(1)."
    print


grammar_json_4a = [
   (obj, (LB, RB)),
   (obj, (LB, members, RB)),
   (members, (keyvalue,)),
   (members, (members, COMMA, members)),
   (keyvalue, (STRING, COLON, value)),
   (value, (STRING,)),
   (value, (INT,)),
   (value, (obj,))
]

grammar_json_4b = [
   (obj, (LB, obj_body)),
   (obj_body, (members, RB)),
   (obj_body, (RB,)),
   (members, (keyvalue, after_keyvalue)),
   (after_keyvalue, ()),
   (after_keyvalue, (COMMA, members)),
   (keyvalue, (STRING, COLON, value)),
   (value, (STRING,)),
   (value, (INT,)),
   (value, (obj,))
]

grammar_json_4c = [
   (obj, (LB, obj_body)),
   (obj_body, (members, RB)),
   (obj_body, (RB,)),
   (members, (keyvalue, after_keyvalue)),
   (after_keyvalue, ()),
   (after_keyvalue, (COMMA, members)),
   (keyvalue, (STRING, COLON, value)),
   (value, (STRING,)),
   (value, (INT,)),
   (value, (obj,))
]

grammar_json__6 = [
    #
    # --- FILL IN HERE IN QUESTION 6 ---
    #
]



def main():
    
    analyze_grammar(grammar_recitation)
    print

    analyze_grammar(grammar_json_4a)
    print
    
    analyze_grammar(grammar_json_4b)
    print
    
    analyze_grammar(grammar_json_4c)
    print
    
    # analyze_grammar(grammar_json_6)
    # print

    #
    # --- ADD MORE TEST CASES HERE ---
    #


if __name__ == '__main__':
    main()
