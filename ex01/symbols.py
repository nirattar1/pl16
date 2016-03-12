"""
This module just contains the definitions of the terminals (tokens) and nonterminals.
"""

# EOF terminal
EOF = 'EOF'        # end of file marker

# terminals for the grammar from the recitation
LP = 'LP'          # (
RP = 'RP'          # )
ASSIGN = 'ASSIGN'  # :=
PLUS = 'PLUS'      # +
IF = 'IF'          # if
ELSE = 'ELSE'      # else
ID = 'ID'          # identifier


# nonterminals for the grammar from the recitation
P = 'P'
S = 'S'
E = 'E'
T = 'T'
EP = 'EP'


# terminals for JSON
LB = 'LB'          # {
RB = 'RB'          # }
LS = 'LS'          # [
RS = 'RS'          # ]
COMMA = 'COMMA'    # ,
COLON = 'COLON'    # :
INT = 'INT'        # an integer value
STRING = 'STRING'  # a string value


# nonterminals for JSON
obj = 'obj'
members = 'members'
keyvalue = 'keyvalue'
value = 'value'
obj_body = 'obj_body'
after_keyvalue = 'after_keyvalue'

#
# --- ADD MORE NONTERMINALS HERE IF NEEDED IN QUESTION 4
#
