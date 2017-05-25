
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "LPAREN RPAREN LCOR RCOR LKEY RKEY COMMA SEMICOLON ID NUMBER STRING_LITERAL PLUS MINUS MULT DIVIDE EQUALS DIFFERENT GT GTE LT LTE MOD UMINUS OR AND NOT ASSIGN PLUSASSIGN MINUSASSIGN MULTASSIGN DIVIDEASSIGN MODASSIGN IF ELSE WHILE FOR RETURN STRING INT BOOLEAN TRUE FALSE BREAK READ WRITE\n    program : decSeq\n    \n    dec : varDec\n        | ID LPAREN paramList RPAREN LKEY block RKEY\n        | type ID LPAREN paramList RPAREN LKEY block RKEY\n    \n    varDec : type varSpecSeq SEMICOLON\n    \n    varSpec : ID\n            | ID ASSIGN literal\n            | ID LCOR NUMBER RCOR\n            | ID LCOR NUMBER RCOR ASSIGN LKEY literalSeq RKEY\n    \n    type : INT\n         | STRING\n         | BOOLEAN\n    \n    param : type ID\n          | type ID RCOR LCOR\n    \n    block : varDecList stmtList\n    \n    stmt : ifStmt\n         | whileStmt\n         | forStmt\n         | breakStmt\n         | returnStmt\n         | readStmt\n         | writeStmt\n         | assign SEMICOLON\n         | subCall SEMICOLON\n    \n    ifStmt : IF LPAREN exp RPAREN LKEY block RKEY\n           | IF LPAREN exp RPAREN LKEY block RKEY ELSE LKEY block RKEY\n    \n    whileStmt : WHILE LPAREN exp RPAREN LKEY block RKEY\n    \n    forStmt : FOR LPAREN assign SEMICOLON exp SEMICOLON assign RPAREN LKEY block RKEY\n    \n    breakStmt : BREAK SEMICOLON\n    \n    readStmt : READ var SEMICOLON\n    \n    writeStmt : WRITE expList SEMICOLON\n    \n    returnStmt : RETURN SEMICOLON\n               | RETURN exp SEMICOLON\n    \n    subCall : ID LPAREN expList RPAREN\n    \n    assign : var ASSIGN exp\n           | var PLUSASSIGN exp\n           | var MINUSASSIGN exp\n           | var MULTASSIGN exp\n           | var DIVIDEASSIGN exp\n           | var MODASSIGN exp\n    \n    exp : exp PLUS exp\n        | exp MINUS exp\n        | exp MULT exp\n        | exp DIVIDE exp\n        | exp MOD exp\n    \n    exp : exp EQUALS exp\n        | exp DIFFERENT exp\n        | exp LTE exp\n        | exp GTE exp\n        | exp GT exp\n        | exp LT exp\n    \n    exp : exp AND exp\n        | exp OR exp\n        | NOT exp\n        | UMINUS exp\n    \n    exp : exp '?' exp ':' exp\n    \n    exp : subCall\n    \n    exp : var\n    \n    exp : literal\n    \n    exp : LPAREN exp RPAREN\n    \n    var : ID\n        | ID LCOR exp RCOR\n    \n    literal : NUMBER\n            | STRING_LITERAL\n            | FALSE\n            | TRUE\n    \n    paramList : paramSeq\n              | empty\n    \n    program : empty\n    \n    paramSeq : param\n             | param COMMA paramSeq\n    \n    varDecList : varDec varDecList\n               | empty\n    \n    varSpecSeq : varSpec\n               | varSpec COMMA varSpecSeq\n    \n    decSeq : dec\n           | dec decSeq\n    \n    stmtList : stmt stmtList\n             | empty\n    \n    literalSeq : literal\n               | literal COMMA literalSeq\n    \n    expList : expSeq\n            | empty\n    \n    expSeq : exp\n           | exp COMMA expSeq\n    empty :"
    
_lr_action_items = {'$end':([0,1,2,3,4,5,11,24,51,105,],[-86,0,-1,-69,-76,-2,-77,-5,-3,-4,]),'ID':([0,4,5,7,8,9,10,20,24,25,38,44,45,46,47,49,51,53,55,56,57,58,59,60,61,68,69,71,73,77,78,79,80,81,82,83,85,86,90,93,94,95,96,97,98,103,104,105,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,129,136,137,144,164,165,167,170,172,173,177,178,181,182,],[6,6,-2,13,-10,-11,-12,28,-5,37,-86,72,-86,-73,37,-86,-3,72,-16,-17,-18,-19,-20,-21,-22,72,92,72,-72,-23,-24,72,72,92,-29,-32,72,72,72,72,72,72,72,72,72,72,72,-4,-33,72,72,72,72,72,72,72,72,72,72,72,72,72,72,-30,-31,72,72,-86,-86,72,92,-25,-27,-86,-86,-26,-28,]),'INT':([0,4,5,12,21,24,27,38,45,49,51,105,164,165,177,178,],[8,8,-2,8,8,-5,8,8,8,8,-3,-4,8,8,8,8,]),'STRING':([0,4,5,12,21,24,27,38,45,49,51,105,164,165,177,178,],[9,9,-2,9,9,-5,9,9,9,9,-3,-4,9,9,9,9,]),'BOOLEAN':([0,4,5,12,21,24,27,38,45,49,51,105,164,165,177,178,],[10,10,-2,10,10,-5,10,10,10,10,-3,-4,10,10,10,10,]),'LPAREN':([6,13,64,65,66,68,71,72,79,80,85,86,90,93,94,95,96,97,98,103,104,112,113,114,115,116,117,118,119,120,121,122,123,124,125,137,144,167,],[12,21,79,80,81,90,90,103,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,]),'RPAREN':([12,16,17,18,19,21,28,29,31,32,33,34,39,48,72,87,88,89,100,101,102,103,108,109,126,127,128,130,131,132,133,134,135,138,145,146,147,148,149,150,151,152,153,154,155,156,157,159,160,161,162,171,174,],[-86,26,-67,-68,-70,-86,-13,41,-63,-64,-65,-66,-71,-14,-61,-57,-58,-59,-82,-83,-84,-86,142,143,-54,-55,159,-35,-36,-37,-38,-39,-40,161,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-60,-85,-34,-62,-56,176,]),'COMMA':([13,15,19,28,30,31,32,33,34,37,42,48,72,87,88,89,102,107,126,127,140,145,146,147,148,149,150,151,152,153,154,155,156,157,159,161,162,171,],[-6,25,27,-13,-7,-63,-64,-65,-66,-6,-8,-14,-61,-57,-58,-59,137,141,-54,-55,-9,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-60,-34,-62,-56,]),'SEMICOLON':([13,14,15,30,31,32,33,34,36,37,42,62,63,67,68,71,72,84,87,88,89,91,92,99,100,101,102,110,126,127,130,131,132,133,134,135,140,145,146,147,148,149,150,151,152,153,154,155,156,157,159,160,161,162,166,171,],[-6,24,-74,-7,-63,-64,-65,-66,-75,-6,-8,77,78,82,83,-86,-61,111,-57,-58,-59,129,-61,136,-82,-83,-84,144,-54,-55,-35,-36,-37,-38,-39,-40,-9,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-60,-85,-34,-62,170,-56,]),'ASSIGN':([13,37,42,70,72,92,162,],[22,22,50,93,-61,-61,-62,]),'LCOR':([13,37,40,72,92,],[23,23,48,104,104,]),'NUMBER':([22,23,68,71,75,79,80,85,86,90,93,94,95,96,97,98,103,104,112,113,114,115,116,117,118,119,120,121,122,123,124,125,137,141,144,167,],[31,35,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,]),'STRING_LITERAL':([22,68,71,75,79,80,85,86,90,93,94,95,96,97,98,103,104,112,113,114,115,116,117,118,119,120,121,122,123,124,125,137,141,144,167,],[32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,]),'FALSE':([22,68,71,75,79,80,85,86,90,93,94,95,96,97,98,103,104,112,113,114,115,116,117,118,119,120,121,122,123,124,125,137,141,144,167,],[33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,]),'TRUE':([22,68,71,75,79,80,85,86,90,93,94,95,96,97,98,103,104,112,113,114,115,116,117,118,119,120,121,122,123,124,125,137,141,144,167,],[34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,]),'IF':([24,38,44,45,46,49,53,55,56,57,58,59,60,61,73,77,78,82,83,111,129,136,164,165,172,173,177,178,181,182,],[-5,-86,64,-86,-73,-86,64,-16,-17,-18,-19,-20,-21,-22,-72,-23,-24,-29,-32,-33,-30,-31,-86,-86,-25,-27,-86,-86,-26,-28,]),'WHILE':([24,38,44,45,46,49,53,55,56,57,58,59,60,61,73,77,78,82,83,111,129,136,164,165,172,173,177,178,181,182,],[-5,-86,65,-86,-73,-86,65,-16,-17,-18,-19,-20,-21,-22,-72,-23,-24,-29,-32,-33,-30,-31,-86,-86,-25,-27,-86,-86,-26,-28,]),'FOR':([24,38,44,45,46,49,53,55,56,57,58,59,60,61,73,77,78,82,83,111,129,136,164,165,172,173,177,178,181,182,],[-5,-86,66,-86,-73,-86,66,-16,-17,-18,-19,-20,-21,-22,-72,-23,-24,-29,-32,-33,-30,-31,-86,-86,-25,-27,-86,-86,-26,-28,]),'BREAK':([24,38,44,45,46,49,53,55,56,57,58,59,60,61,73,77,78,82,83,111,129,136,164,165,172,173,177,178,181,182,],[-5,-86,67,-86,-73,-86,67,-16,-17,-18,-19,-20,-21,-22,-72,-23,-24,-29,-32,-33,-30,-31,-86,-86,-25,-27,-86,-86,-26,-28,]),'RETURN':([24,38,44,45,46,49,53,55,56,57,58,59,60,61,73,77,78,82,83,111,129,136,164,165,172,173,177,178,181,182,],[-5,-86,68,-86,-73,-86,68,-16,-17,-18,-19,-20,-21,-22,-72,-23,-24,-29,-32,-33,-30,-31,-86,-86,-25,-27,-86,-86,-26,-28,]),'READ':([24,38,44,45,46,49,53,55,56,57,58,59,60,61,73,77,78,82,83,111,129,136,164,165,172,173,177,178,181,182,],[-5,-86,69,-86,-73,-86,69,-16,-17,-18,-19,-20,-21,-22,-72,-23,-24,-29,-32,-33,-30,-31,-86,-86,-25,-27,-86,-86,-26,-28,]),'WRITE':([24,38,44,45,46,49,53,55,56,57,58,59,60,61,73,77,78,82,83,111,129,136,164,165,172,173,177,178,181,182,],[-5,-86,71,-86,-73,-86,71,-16,-17,-18,-19,-20,-21,-22,-72,-23,-24,-29,-32,-33,-30,-31,-86,-86,-25,-27,-86,-86,-26,-28,]),'RKEY':([24,31,32,33,34,38,43,44,45,46,49,52,53,54,55,56,57,58,59,60,61,73,74,76,77,78,82,83,106,107,111,129,136,163,164,165,168,169,172,173,177,178,179,180,181,182,],[-5,-63,-64,-65,-66,-86,51,-86,-86,-73,-86,-15,-86,-79,-16,-17,-18,-19,-20,-21,-22,-72,105,-78,-23,-24,-29,-32,140,-80,-33,-30,-31,-81,-86,-86,172,173,-25,-27,-86,-86,181,182,-26,-28,]),'LKEY':([26,41,50,142,143,175,176,],[38,49,75,164,165,177,178,]),'RCOR':([28,31,32,33,34,35,72,87,88,89,126,127,139,145,146,147,148,149,150,151,152,153,154,155,156,157,159,161,162,171,],[40,-63,-64,-65,-66,42,-61,-57,-58,-59,-54,-55,162,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-60,-34,-62,-56,]),'PLUS':([31,32,33,34,72,84,87,88,89,102,108,109,126,127,128,130,131,132,133,134,135,139,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,161,162,166,171,],[-63,-64,-65,-66,-61,112,-57,-58,-59,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,-60,-34,-62,112,112,]),'MINUS':([31,32,33,34,72,84,87,88,89,102,108,109,126,127,128,130,131,132,133,134,135,139,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,161,162,166,171,],[-63,-64,-65,-66,-61,113,-57,-58,-59,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,-60,-34,-62,113,113,]),'MULT':([31,32,33,34,72,84,87,88,89,102,108,109,126,127,128,130,131,132,133,134,135,139,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,161,162,166,171,],[-63,-64,-65,-66,-61,114,-57,-58,-59,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,-60,-34,-62,114,114,]),'DIVIDE':([31,32,33,34,72,84,87,88,89,102,108,109,126,127,128,130,131,132,133,134,135,139,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,161,162,166,171,],[-63,-64,-65,-66,-61,115,-57,-58,-59,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,-60,-34,-62,115,115,]),'MOD':([31,32,33,34,72,84,87,88,89,102,108,109,126,127,128,130,131,132,133,134,135,139,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,161,162,166,171,],[-63,-64,-65,-66,-61,116,-57,-58,-59,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,-60,-34,-62,116,116,]),'EQUALS':([31,32,33,34,72,84,87,88,89,102,108,109,126,127,128,130,131,132,133,134,135,139,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,161,162,166,171,],[-63,-64,-65,-66,-61,117,-57,-58,-59,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,-60,-34,-62,117,117,]),'DIFFERENT':([31,32,33,34,72,84,87,88,89,102,108,109,126,127,128,130,131,132,133,134,135,139,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,161,162,166,171,],[-63,-64,-65,-66,-61,118,-57,-58,-59,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,-60,-34,-62,118,118,]),'LTE':([31,32,33,34,72,84,87,88,89,102,108,109,126,127,128,130,131,132,133,134,135,139,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,161,162,166,171,],[-63,-64,-65,-66,-61,119,-57,-58,-59,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,-60,-34,-62,119,119,]),'GTE':([31,32,33,34,72,84,87,88,89,102,108,109,126,127,128,130,131,132,133,134,135,139,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,161,162,166,171,],[-63,-64,-65,-66,-61,120,-57,-58,-59,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,-60,-34,-62,120,120,]),'GT':([31,32,33,34,72,84,87,88,89,102,108,109,126,127,128,130,131,132,133,134,135,139,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,161,162,166,171,],[-63,-64,-65,-66,-61,121,-57,-58,-59,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,-60,-34,-62,121,121,]),'LT':([31,32,33,34,72,84,87,88,89,102,108,109,126,127,128,130,131,132,133,134,135,139,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,161,162,166,171,],[-63,-64,-65,-66,-61,122,-57,-58,-59,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,-60,-34,-62,122,122,]),'AND':([31,32,33,34,72,84,87,88,89,102,108,109,126,127,128,130,131,132,133,134,135,139,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,161,162,166,171,],[-63,-64,-65,-66,-61,123,-57,-58,-59,123,123,123,123,123,123,123,123,123,123,123,123,123,123,123,123,123,123,123,123,123,123,123,123,123,123,123,-60,-34,-62,123,123,]),'OR':([31,32,33,34,72,84,87,88,89,102,108,109,126,127,128,130,131,132,133,134,135,139,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,161,162,166,171,],[-63,-64,-65,-66,-61,124,-57,-58,-59,124,124,124,124,124,124,124,124,124,124,124,124,124,124,124,124,124,124,124,124,124,124,124,124,124,124,124,-60,-34,-62,124,124,]),'?':([31,32,33,34,72,84,87,88,89,102,108,109,126,127,128,130,131,132,133,134,135,139,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,161,162,166,171,],[-63,-64,-65,-66,-61,125,-57,-58,-59,125,125,125,125,125,125,125,125,125,125,125,125,125,125,125,125,125,125,125,125,125,125,125,125,125,125,125,-60,-34,-62,125,125,]),':':([31,32,33,34,72,87,88,89,126,127,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,161,162,171,],[-63,-64,-65,-66,-61,-57,-58,-59,-54,-55,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,167,-60,-34,-62,-56,]),'NOT':([68,71,79,80,85,86,90,93,94,95,96,97,98,103,104,112,113,114,115,116,117,118,119,120,121,122,123,124,125,137,144,167,],[85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,]),'UMINUS':([68,71,79,80,85,86,90,93,94,95,96,97,98,103,104,112,113,114,115,116,117,118,119,120,121,122,123,124,125,137,144,167,],[86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,]),'PLUSASSIGN':([70,72,92,162,],[94,-61,-61,-62,]),'MINUSASSIGN':([70,72,92,162,],[95,-61,-61,-62,]),'MULTASSIGN':([70,72,92,162,],[96,-61,-61,-62,]),'DIVIDEASSIGN':([70,72,92,162,],[97,-61,-61,-62,]),'MODASSIGN':([70,72,92,162,],[98,-61,-61,-62,]),'ELSE':([172,],[175,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'decSeq':([0,4,],[2,11,]),'empty':([0,12,21,38,44,45,49,53,71,103,164,165,177,178,],[3,18,18,46,54,46,46,54,101,101,46,46,46,46,]),'dec':([0,4,],[4,4,]),'varDec':([0,4,38,45,49,164,165,177,178,],[5,5,45,45,45,45,45,45,45,]),'type':([0,4,12,21,27,38,45,49,164,165,177,178,],[7,7,20,20,20,47,47,47,47,47,47,47,]),'varSpecSeq':([7,25,47,],[14,36,14,]),'varSpec':([7,25,47,],[15,15,15,]),'paramList':([12,21,],[16,29,]),'paramSeq':([12,21,27,],[17,17,39,]),'param':([12,21,27,],[19,19,19,]),'literal':([22,68,71,75,79,80,85,86,90,93,94,95,96,97,98,103,104,112,113,114,115,116,117,118,119,120,121,122,123,124,125,137,141,144,167,],[30,89,89,107,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,107,89,89,]),'block':([38,49,164,165,177,178,],[43,74,168,169,179,180,]),'varDecList':([38,45,49,164,165,177,178,],[44,73,44,44,44,44,44,]),'stmtList':([44,53,],[52,76,]),'stmt':([44,53,],[53,53,]),'ifStmt':([44,53,],[55,55,]),'whileStmt':([44,53,],[56,56,]),'forStmt':([44,53,],[57,57,]),'breakStmt':([44,53,],[58,58,]),'returnStmt':([44,53,],[59,59,]),'readStmt':([44,53,],[60,60,]),'writeStmt':([44,53,],[61,61,]),'assign':([44,53,81,170,],[62,62,110,174,]),'subCall':([44,53,68,71,79,80,85,86,90,93,94,95,96,97,98,103,104,112,113,114,115,116,117,118,119,120,121,122,123,124,125,137,144,167,],[63,63,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,]),'var':([44,53,68,69,71,79,80,81,85,86,90,93,94,95,96,97,98,103,104,112,113,114,115,116,117,118,119,120,121,122,123,124,125,137,144,167,170,],[70,70,88,91,88,88,88,70,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,70,]),'exp':([68,71,79,80,85,86,90,93,94,95,96,97,98,103,104,112,113,114,115,116,117,118,119,120,121,122,123,124,125,137,144,167,],[84,102,108,109,126,127,128,130,131,132,133,134,135,102,139,145,146,147,148,149,150,151,152,153,154,155,156,157,158,102,166,171,]),'expList':([71,103,],[99,138,]),'expSeq':([71,103,137,],[100,100,160,]),'literalSeq':([75,141,],[106,163,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> decSeq','program',1,'p_program','analisadorSintatico.py',28),
  ('dec -> varDec','dec',1,'p_dec','analisadorSintatico.py',35),
  ('dec -> ID LPAREN paramList RPAREN LKEY block RKEY','dec',7,'p_dec','analisadorSintatico.py',36),
  ('dec -> type ID LPAREN paramList RPAREN LKEY block RKEY','dec',8,'p_dec','analisadorSintatico.py',37),
  ('varDec -> type varSpecSeq SEMICOLON','varDec',3,'p_varDec','analisadorSintatico.py',49),
  ('varSpec -> ID','varSpec',1,'p_varSpec','analisadorSintatico.py',56),
  ('varSpec -> ID ASSIGN literal','varSpec',3,'p_varSpec','analisadorSintatico.py',57),
  ('varSpec -> ID LCOR NUMBER RCOR','varSpec',4,'p_varSpec','analisadorSintatico.py',58),
  ('varSpec -> ID LCOR NUMBER RCOR ASSIGN LKEY literalSeq RKEY','varSpec',8,'p_varSpec','analisadorSintatico.py',59),
  ('type -> INT','type',1,'p_type','analisadorSintatico.py',73),
  ('type -> STRING','type',1,'p_type','analisadorSintatico.py',74),
  ('type -> BOOLEAN','type',1,'p_type','analisadorSintatico.py',75),
  ('param -> type ID','param',2,'p_param','analisadorSintatico.py',82),
  ('param -> type ID RCOR LCOR','param',4,'p_param','analisadorSintatico.py',83),
  ('block -> varDecList stmtList','block',2,'p_block','analisadorSintatico.py',93),
  ('stmt -> ifStmt','stmt',1,'p_stmt','analisadorSintatico.py',100),
  ('stmt -> whileStmt','stmt',1,'p_stmt','analisadorSintatico.py',101),
  ('stmt -> forStmt','stmt',1,'p_stmt','analisadorSintatico.py',102),
  ('stmt -> breakStmt','stmt',1,'p_stmt','analisadorSintatico.py',103),
  ('stmt -> returnStmt','stmt',1,'p_stmt','analisadorSintatico.py',104),
  ('stmt -> readStmt','stmt',1,'p_stmt','analisadorSintatico.py',105),
  ('stmt -> writeStmt','stmt',1,'p_stmt','analisadorSintatico.py',106),
  ('stmt -> assign SEMICOLON','stmt',2,'p_stmt','analisadorSintatico.py',107),
  ('stmt -> subCall SEMICOLON','stmt',2,'p_stmt','analisadorSintatico.py',108),
  ('ifStmt -> IF LPAREN exp RPAREN LKEY block RKEY','ifStmt',7,'p_ifStmt','analisadorSintatico.py',118),
  ('ifStmt -> IF LPAREN exp RPAREN LKEY block RKEY ELSE LKEY block RKEY','ifStmt',11,'p_ifStmt','analisadorSintatico.py',119),
  ('whileStmt -> WHILE LPAREN exp RPAREN LKEY block RKEY','whileStmt',7,'p_whileStmt','analisadorSintatico.py',129),
  ('forStmt -> FOR LPAREN assign SEMICOLON exp SEMICOLON assign RPAREN LKEY block RKEY','forStmt',11,'p_forStmt','analisadorSintatico.py',136),
  ('breakStmt -> BREAK SEMICOLON','breakStmt',2,'p_breakStmt','analisadorSintatico.py',143),
  ('readStmt -> READ var SEMICOLON','readStmt',3,'p_readStmt','analisadorSintatico.py',150),
  ('writeStmt -> WRITE expList SEMICOLON','writeStmt',3,'p_writeStmt','analisadorSintatico.py',157),
  ('returnStmt -> RETURN SEMICOLON','returnStmt',2,'p_returnStmt','analisadorSintatico.py',164),
  ('returnStmt -> RETURN exp SEMICOLON','returnStmt',3,'p_returnStmt','analisadorSintatico.py',165),
  ('subCall -> ID LPAREN expList RPAREN','subCall',4,'p_subCall','analisadorSintatico.py',175),
  ('assign -> var ASSIGN exp','assign',3,'p_assign','analisadorSintatico.py',182),
  ('assign -> var PLUSASSIGN exp','assign',3,'p_assign','analisadorSintatico.py',183),
  ('assign -> var MINUSASSIGN exp','assign',3,'p_assign','analisadorSintatico.py',184),
  ('assign -> var MULTASSIGN exp','assign',3,'p_assign','analisadorSintatico.py',185),
  ('assign -> var DIVIDEASSIGN exp','assign',3,'p_assign','analisadorSintatico.py',186),
  ('assign -> var MODASSIGN exp','assign',3,'p_assign','analisadorSintatico.py',187),
  ('exp -> exp PLUS exp','exp',3,'p_expArithmetic','analisadorSintatico.py',205),
  ('exp -> exp MINUS exp','exp',3,'p_expArithmetic','analisadorSintatico.py',206),
  ('exp -> exp MULT exp','exp',3,'p_expArithmetic','analisadorSintatico.py',207),
  ('exp -> exp DIVIDE exp','exp',3,'p_expArithmetic','analisadorSintatico.py',208),
  ('exp -> exp MOD exp','exp',3,'p_expArithmetic','analisadorSintatico.py',209),
  ('exp -> exp EQUALS exp','exp',3,'p_expComparison','analisadorSintatico.py',225),
  ('exp -> exp DIFFERENT exp','exp',3,'p_expComparison','analisadorSintatico.py',226),
  ('exp -> exp LTE exp','exp',3,'p_expComparison','analisadorSintatico.py',227),
  ('exp -> exp GTE exp','exp',3,'p_expComparison','analisadorSintatico.py',228),
  ('exp -> exp GT exp','exp',3,'p_expComparison','analisadorSintatico.py',229),
  ('exp -> exp LT exp','exp',3,'p_expComparison','analisadorSintatico.py',230),
  ('exp -> exp AND exp','exp',3,'p_expLogic','analisadorSintatico.py',248),
  ('exp -> exp OR exp','exp',3,'p_expLogic','analisadorSintatico.py',249),
  ('exp -> NOT exp','exp',2,'p_expLogic','analisadorSintatico.py',250),
  ('exp -> UMINUS exp','exp',2,'p_expLogic','analisadorSintatico.py',251),
  ('exp -> exp ? exp : exp','exp',5,'p_expTernary','analisadorSintatico.py',265),
  ('exp -> subCall','exp',1,'p_expSubCall','analisadorSintatico.py',272),
  ('exp -> var','exp',1,'p_expVar','analisadorSintatico.py',279),
  ('exp -> literal','exp',1,'p_expLiteral','analisadorSintatico.py',286),
  ('exp -> LPAREN exp RPAREN','exp',3,'p_expMultParent','analisadorSintatico.py',293),
  ('var -> ID','var',1,'p_var','analisadorSintatico.py',300),
  ('var -> ID LCOR exp RCOR','var',4,'p_var','analisadorSintatico.py',301),
  ('literal -> NUMBER','literal',1,'p_literal','analisadorSintatico.py',311),
  ('literal -> STRING_LITERAL','literal',1,'p_literal','analisadorSintatico.py',312),
  ('literal -> FALSE','literal',1,'p_literal','analisadorSintatico.py',313),
  ('literal -> TRUE','literal',1,'p_literal','analisadorSintatico.py',314),
  ('paramList -> paramSeq','paramList',1,'p_paramList','analisadorSintatico.py',321),
  ('paramList -> empty','paramList',1,'p_paramList','analisadorSintatico.py',322),
  ('program -> empty','program',1,'p_paramListNull','analisadorSintatico.py',330),
  ('paramSeq -> param','paramSeq',1,'p_paramSeq','analisadorSintatico.py',336),
  ('paramSeq -> param COMMA paramSeq','paramSeq',3,'p_paramSeq','analisadorSintatico.py',337),
  ('varDecList -> varDec varDecList','varDecList',2,'p_varDecList','analisadorSintatico.py',347),
  ('varDecList -> empty','varDecList',1,'p_varDecList','analisadorSintatico.py',348),
  ('varSpecSeq -> varSpec','varSpecSeq',1,'p_varSpecSeq','analisadorSintatico.py',356),
  ('varSpecSeq -> varSpec COMMA varSpecSeq','varSpecSeq',3,'p_varSpecSeq','analisadorSintatico.py',357),
  ('decSeq -> dec','decSeq',1,'p_decSeq','analisadorSintatico.py',367),
  ('decSeq -> dec decSeq','decSeq',2,'p_decSeq','analisadorSintatico.py',368),
  ('stmtList -> stmt stmtList','stmtList',2,'p_stmtList','analisadorSintatico.py',378),
  ('stmtList -> empty','stmtList',1,'p_stmtList','analisadorSintatico.py',379),
  ('literalSeq -> literal','literalSeq',1,'p_literalSeq','analisadorSintatico.py',387),
  ('literalSeq -> literal COMMA literalSeq','literalSeq',3,'p_literalSeq','analisadorSintatico.py',388),
  ('expList -> expSeq','expList',1,'p_expList','analisadorSintatico.py',398),
  ('expList -> empty','expList',1,'p_expList','analisadorSintatico.py',399),
  ('expSeq -> exp','expSeq',1,'p_expSeq','analisadorSintatico.py',407),
  ('expSeq -> exp COMMA expSeq','expSeq',3,'p_expSeq','analisadorSintatico.py',408),
  ('empty -> <empty>','empty',0,'p_empty','analisadorSintatico.py',417),
]
