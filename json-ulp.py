#!/usr/bin/env python
# json-ulp.py - generate json.ulp, which exports Eagle to JSON
# http://github.com/ajray/schematic-file-converter
# Alex Ray (2011) <ajray@ncsu.edu>
# TODO handle loop members
from eaglet import eagle, types, basic
def t(a): # Return the name of the type of 'a'
  if a in basic: return a
  if a in types: return types[a]
  return "UL_"+a.upper()

header = """// json.ulp - Export an EagleCAD file into JSON
// Generated by the codez in this wonderful github repo:
// http://github.com/ajray/schematic-file-converter
// Alex Ray (2011) <ajray@ncsu.edu>"""
misc = """string esc(string s) { // JSON string escapes
    string out = "\\""; // open quote
    for (int i = 0; s[i]; ++i) {
        switch(s[i]) {
            case '"': out += "\\\""; break;
            case '\\\\': out += "\\\\\\\\"; break;
            case '/': out += "\\\\/"; break;
            case '\\b': out += "\\\\b"; break;
            case '\\f': out += "\\\\f"; break;
            case '\\n': out += "\\\\n"; break;
            case '\\r': out += "\\\\r"; break;
            case '\\t': out += "\\\\t"; break;
            default: out += s[i];
        }
    }
    out += "\\""; // close quote
    return out;
}
void n()          { printf("\\n"); }     // newline
void cn()         { printf(",\\n"); }    // comma & newline
void po(string a) { printf("%s:{",a); } // start of an object
void on()         { printf("}"); }      // end of an object
void pl(string a) { printf("%s:[",a); } // start of a list
void ln()         { printf("]"); }      // end of a list
void print_string (string a, string b)  { printf("%s:%s",a,esc(b)); }
void print_int    (string a, int b)     { printf("%s:%d",a,b); }
void print_real   (string a, real b)    { printf("%s:%g",esc(a),b); }"""

def printfunc(name,members):
  """ Make a print_<type>() function """
  fun = 'print_%s'%name   # print function name
  typ = t(name)           # Eagle type being printed
  A   = name+'i'          # name of the instance
  print 'void %s(%s %s) {' % (fun, typ, A)
  print '\tint a; po("%s");' % (name)
  com = False           # Keeping track of commas
  for mem,mtyp in members.items(): # Member fields of each type
    if not com: com = True # Taking care of commas
    else: print 'cn();'
    if mtyp not in basic and mem != mtyp: # loop member
      B = mem+'l'
      print '\tpl(%s);a=0;%s.%s(%s)'%(mem,A,mem,B),
      print '{if(a==0)a=1;else cn();%s("%s",%s);}'%(fun,member.upper())
    else: # Normal data member
      print '\tprint_%s("%s",%s.%s);'%(mtyp,mem,A,mem), # data member
  print 'on();}'

if __name__ == "__main__":
  print header
  print misc
  for name,members in eagle.items(): printfunc(name,members)
