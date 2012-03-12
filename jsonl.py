#!/usr/bin/python

import sys
from ply import lex, yacc

tokens = (
   'NUMBER',
   'O_BEGIN',
   'O_END',
   'A_BEGIN',
   'A_END',
   'COLON',
   #'DBL_QUOTE',
   'STR',
   'COMMA',
   'BOOLEAN',
   'NULL',
)

# Regular expression rules for simple tokens
t_COMMA   = r','
t_O_BEGIN = r'\{'
t_O_END   = r'\}'
t_A_BEGIN = r'\['
t_A_END = r'\]'
t_COLON   = r':'
#t_DBL_QUOTE = r'\"'
t_STR = r'\"([^\\\n]|(\\.))*?\"'
t_BOOLEAN = r'(true|false)'
t_NULL = r'null'

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+((\.)\d+){0,1}'
    #print 'GROUP: ' + str(t.lexer.lexmatch.group(3))
    if t.lexer.lexmatch.group(3) == '.':
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def test (line):
  print "=============\n{0}\n".format (line)
  lexer.input (line)
  for f in lexer:
    print f

tests = [
  '{ "a" : "b" }',
  '{ "a" : 1 }',
  '{ "a" : 1.1 }',  
  '{ "a" : [ 1, 2, 3 ]}',
  '{ "escape" : "es\\"cape" }',
  '{ "escape" : "es\\"cape", "array" : [] }',
  '{ "escape" : "es\\"cape", "array" : [ { "obj" : "yes" } ] }'
]

#test (tests[0])

#for t in tests:
#test (tests[1])
#test (tests[2])
if __name__ == '__main__':
  if len (sys.argv) > 1:
    for f in sys.argv[1:]:
      content = open(f).read();
      #print lexer
      l = lexer.input (content)
      for f in lexer:
        print f
