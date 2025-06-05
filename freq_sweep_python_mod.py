# this module will be imported in the into your flowgraph
f1 = 40000000
f2 = 47000000
f = f1

step = 1000000

def sweeper(prop_lvl):
 global f1,f2,f,step
 if prop_lvl:
   f +=step
 if f>= f2:f=f1
return f

