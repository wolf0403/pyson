#!/usr/bin/python

from ply import lex, yacc
from jsonl import tokens

import sys

stack = []
value = {}

def p_obj (p):
  '''obj : O_BEGIN kvs O_END'''
  #print 'p_obj ' + str(p[2])
  global stack
  # since all object start with keys, we push at p_key
  #print "p_obj " + str(stack.pop ())

def p_valtype (p):
  '''valtype : value
             | obj
             | array'''

def p_avals (p):
  '''avals : valtype
           | avals COMMA valtype'''
  global stack
  i = int(stack.pop ())
  stack.append (str(i + 1))

def p_abegin (p):
  '''abegin : A_BEGIN'''
  global stack
  stack.append ('0')

def p_array (p):
  '''array : abegin avals A_END'''

def p_kvs (p):
  '''kvs : kv
         | kvs COMMA kv'''
  print "p_kvs"
  p[0] = ''

def p_kv (p):
  '''kv : key valtype'''
  global stack
  print "p_kv pop " + str(stack.pop()) + ' ' + str(stack)

def p_key (p):
  '''key : STR COLON'''
  global stack
  p[0] = p[1][1:-1]
  stack.append(p[0])
  print "p_key push " + str(p[0]) + " " + str(stack)

def p_value (p):
  '''value : STR
           | NUMBER
           | BOOLEAN
           | NULL'''
  p[0] = p[1]
  global value, stack
  k = '/' + '/'.join(stack)
  if k in value:
    if type (value[k]) != list:
      value[k] = [ value[k], p[0] ]
    else:
      value[k].append (p[0])
  else:
    value[k] = p[0]
  print "p_value " + str(p[0]) + ' ' + str(stack)

y = yacc.yacc (debug=0, outputdir='dbg')

if __name__ == '__main__' and len(sys.argv) > 1:
  for f in sys.argv[1:]:
    y.parse (open(f).read())
    print stack
    print value
