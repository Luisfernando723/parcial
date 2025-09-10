import re

class Log:
    def __init__(s): s.err=[]
    def add(s,m): s.err.append(m)
    def show(s): [print(e) for e in s.err]

class Lexer:
    def __init__(s,txt,log):
        s.txt=txt; s.log=log
        s.reg=re.compile(r"(?P<FUNC>func)|(?P<PRINT>print)|(?P<NUM>\d+)|(?P<ID>[A-Za-z_]\w*)|(?P<PLUS>\+)|(?P<MINUS>-)|(?P<MUL>\*)|(?P<DIV>/)|(?P<POW>\^)|(?P<LP>\()|(?P<RP>\))|(?P<COMMA>,)|(?P<EQ>=)|(?P<SEMI>;)|(?P<WS>[ \t\n]+)|(?P<ERR>.)")
    def run(s):
        toks=[]
        for m in s.reg.finditer(s.txt):
            t=m.lastgroup; v=m.group()
            if t in("WS",): continue
            if t=="ERR": s.log.add("Error: símbolo desconocido "+v)
            else: toks.append((t,v))
        toks.append(("EOF","")); return toks

class Parser:
    def __init__(s,toks,log): s.t=toks; s.i=0; s.log=log; s.funcs={}
    def cur(s): return s.t[s.i]
    def eat(s,k):
        if s.cur()[0]==k: s.i+=1
        else: s.log.add("Error: se esperaba "+k+" y llegó "+s.cur()[1]); s.i+=1
    def program(s):
        p=[]
        while s.cur()[0]!="EOF":
            if s.cur()[0]=="FUNC": p.append(("FUNC",s.func()))
            elif s.cur()[0]=="PRINT": p.append(("PRINT",s.print()))
            else: s.log.add("Error: token inesperado "+s.cur()[1]); s.i+=1
        return p
    def func(s):
        s.eat("FUNC"); n=s.cur()[1]; s.eat("ID"); s.eat("LP")
        ps=[]
        if s.cur()[0]=="ID":
            ps.append(s.cur()[1]); s.eat("ID")
            while s.cur()[0]=="COMMA": s.eat("COMMA"); ps.append(s.cur()[1]); s.eat("ID")
        s.eat("RP"); s.eat("EQ"); e=s.expr(); s.eat("SEMI")
        s.funcs[n]=(ps,e); return (n,ps,e)
    def print(s): s.eat("PRINT"); c=s.call(); s.eat("SEMI"); return c
    def call(s):
        n=s.cur()[1]; s.eat("ID"); s.eat("LP"); a=[]
        if s.cur()[0]!="RP": a.append(s.expr()); 
        while s.cur()[0]=="COMMA": s.eat("COMMA"); a.append(s.expr())
        s.eat("RP"); return ("CALL",n,a)
    def expr(s):
        x=s.term()
        while s.cur()[0] in("PLUS","MINUS"): o=s.cur()[0]; s.eat(o); x=(o,x,s.term())
        return x
    def term(s):
        x=s.fact()
        while s.cur()[0] in("MUL","DIV"): o=s.cur()[0]; s.eat(o); x=(o,x,s.fact())
        return x
    def fact(s):
        x=s.base()
        if s.cur()[0]=="POW": s.eat("POW"); x=("POW",x,s.fact())
        return x
    def base(s):
        t,v=s.cur()
        if t=="NUM": s.eat("NUM"); return ("NUM",int(v))
        if t=="ID":
            if s.t[s.i+1][0]=="LP": return s.call()
            s.eat("ID"); return ("VAR",v)
        if t=="LP": s.eat("LP"); x=s.expr(); s.eat("RP"); return x
        s.log.add("Error: token inesperado "+v); s.i+=1; return None

class Exec:
    def __init__(s,p,f,log): s.p=p; s.f=f; s.log=log
    def run(s):
        for st in s.p:
            if st[0]=="PRINT":
                v=s.call(st[1])
                if v!=None: print(v)
    def call(s,c,e={}):
        _,n,a=c
        if n not in s.f: s.log.add("Error: función no definida "+n); return None
        ps,b=s.f[n]
        if len(a)!=len(ps): s.log.add("Error: número de parámetros en "+n); return None
        vals=[s.eval(x,{}) for x in a]; env=dict(zip(ps,vals))
        return s.eval(b,env)
    def eval(s,n,e):
        if n==None: return None
        t=n[0]
        if t=="NUM": return n[1]
        if t=="VAR":
            if n[1] in e: return e[n[1]]
            s.log.add("Error: variable no definida "+n[1]); return None
        if t=="CALL": return s.call(n,e)
        if t in("PLUS","MINUS","MUL","DIV","POW"):
            l=s.eval(n[1],e); r=s.eval(n[2],e)
            if l==None or r==None: return None
            if t=="PLUS": return l+r
            if t=="MINUS": return l-r
            if t=="MUL": return l*r
            if t=="DIV": 
                if r==0: s.log.add("Error: división por cero"); return None
                return l//r
            if t=="POW": return l**r

def main():
    log=Log(); src=open("codigo.txt").read()
    toks=Lexer(src,log).run(); p=Parser(toks,log)
    prog=p.program(); Exec(prog,p.funcs,log).run(); log.show()

if __name__=="__main__": main()
