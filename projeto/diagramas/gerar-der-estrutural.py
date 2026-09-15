# -*- coding: utf-8 -*-
"""DER estrutural: entidades, relacionamentos e cardinalidades, sem os atributos
comuns (que ja estao nas tabelas da Secao 1.3). Emite .drawio e PDF via TikZ."""
import math, sys, html

COL = dict(A=160, B=470, C=780, D=1090)
def R(i): return 110 + 190*i

# fill, stroke
ACERVO=("DCE9F5","3D6E9E"); USER=("E4DEF2","6A5A94"); AVAL=("FAE3CE","B0703A")
PONTE=("E2EFD9","5A8542"); NEUT=("FFFFFF","5A6570"); ATTR=("FFFFFF","7A848C")

F_ENT,F_SUB,F_REL,F_ATTR,F_CARD = 23,21,19,19,16   # em unidades do layout
W_ENT,H_ENT = 168,84
W_SUB,H_SUB = 178,84
W_REL,H_REL = 196,132
W_RE2,H_RE2 = 224,152
W_ELL,H_ELL = 170,66
W_TRI,H_TRI = 96,78

N = {}   # nome -> dict
Ed = []

def put(name,kind,col,row,color,label=None,w=None,h=None,dashed=False):
    sz = dict(ent=(W_ENT,H_ENT),weak=(W_ENT,H_ENT),sub=(W_SUB,H_SUB),rel=(W_REL,H_REL),
              rel2=(W_RE2,H_RE2),attr=(W_ELL,H_ELL),tri=(W_TRI,H_TRI))[kind]
    N[name]=dict(name=name,kind=kind,x=COL[col] if col in COL else col,y=R(row) if isinstance(row,int) else row,
                 w=w or sz[0],h=h or sz[1],fill=color[0],stroke=color[1],
                 label=label if label is not None else name,dashed=dashed)
def E(a,b,lab="",pts=None): Ed.append(dict(a=a,b=b,lab=lab,pts=pts or []))

# ---- coluna A: acervo ----
put("genero","ent","A",0,ACERVO)
put("classifica","rel","A",1,NEUT)
put("serie","ent","A",2,ACERVO)
put("possui_temporada","rel2","A",3,NEUT)
put("temporada","weak","A",4,ACERVO)
put("possui_episodio","rel2","A",5,NEUT)
put("episodio","weak","A",6,ACERVO)
put("declara_estado","rel","A",7,PONTE)
put("comentario","ent","C",8,AVAL)
# ---- coluna B ----
put("pessoa","ent","B",0,ACERVO)
put("participa","rel","B",1,NEUT)
put("incide_serie","rel","B",2,NEUT)
put("numero_t","attr","B",3,ATTR,label="numero")
put("incide_temporada","rel","B",4,NEUT)
put("numero_e","attr","B",5,ATTR,label="numero")
put("incide_episodio","rel","B",6,NEUT)
put("registra","rel","B",7,PONTE)
put("responde","rel","B",8,NEUT)
put("comenta","rel","B",9,NEUT)
# ---- coluna C ----
put("avaliacao_serie","sub","C",2,AVAL)
put("avaliacao_temporada","sub","C",4,AVAL)
put("total_curtidas","attr","C",5,ATTR,dashed=True)
put("avaliacao_episodio","sub","C",6,AVAL)
put("recebe","rel","C",7,NEUT)
put("segue","rel","C",9,NEUT)
# ---- coluna D ----
put("tri","tri","D",5,AVAL,label="d")
put("avaliacao","ent","D",6,AVAL)
put("escreve","rel","D",7,NEUT)
put("usuario","ent","D",8,USER)
put("curte","rel","D",9,NEUT)

LANE = 0   # corredor vertical livre a esquerda da coluna A

E("genero","classifica","(0,N)");            E("classifica","serie","(1,N)")
E("serie","possui_temporada","(1,N)");       E("possui_temporada","temporada","(1,1)")
E("temporada","possui_episodio","(1,N)");    E("possui_episodio","episodio","(1,1)")
E("serie","participa","(0,N)");              E("participa","pessoa","(0,N)")
E("serie","incide_serie","(0,N)");           E("incide_serie","avaliacao_serie","(1,1)")
E("temporada","incide_temporada","(0,N)");   E("incide_temporada","avaliacao_temporada","(1,1)")
E("episodio","incide_episodio","(0,N)");     E("incide_episodio","avaliacao_episodio","(1,1)")
E("numero_t","temporada"); E("numero_e","episodio"); E("total_curtidas","avaliacao")
E("avaliacao_serie","tri"); E("avaliacao_temporada","tri"); E("avaliacao_episodio","tri")
E("avaliacao","tri")                                  # linha dupla = total
E("usuario","escreve","(0,N)");              E("escreve","avaliacao","(1,1)")
E("avaliacao","recebe","(0,N)");             E("recebe","comentario","(1,1)")
E("usuario","comenta","(0,N)");              E("comenta","comentario","(1,1)")
E("comentario","responde","(0,1) pai");      E("responde","comentario","(0,N) resp.")
E("episodio","registra","(0,N)");            E("registra","usuario","(0,N)")
E("serie","declara_estado","(0,N)", pts=[(LANE,R(2)),(LANE,R(7))])
E("declara_estado","usuario","(0,N)")
E("usuario","segue","(0,N) seguidor");       E("segue","usuario","(0,N) seguido")
E("usuario","curte","(0,N)");                E("curte","agregacao","(0,N)")

AGG=["avaliacao","escreve","usuario"]
_x=[N[m]["x"]-N[m]["w"]/2 for m in AGG]+[N[m]["x"]+N[m]["w"]/2 for m in AGG]
_y=[N[m]["y"]-N[m]["h"]/2 for m in AGG]+[N[m]["y"]+N[m]["h"]/2 for m in AGG]
M=30
N["agregacao"]=dict(name="agregacao",kind="agg",x=(min(_x)+max(_x))/2,y=(min(_y)+max(_y))/2,
    w=max(_x)-min(_x)+2*M,h=max(_y)-min(_y)+2*M,fill=None,stroke="6A5A94",label="",dashed=True)

# ---------------- verificacao ----------------
def bx(s): return (s["x"]-s["w"]/2,s["y"]-s["h"]/2,s["x"]+s["w"]/2,s["y"]+s["h"]/2)
prob=[]
ns=[n for n,s in N.items() if s["kind"]!="agg"]
for i in range(len(ns)):
    for j in range(i+1,len(ns)):
        a,b=bx(N[ns[i]]),bx(N[ns[j]]); pad=16
        if not (a[2]+pad<=b[0] or b[2]+pad<=a[0] or a[3]+pad<=b[1] or b[3]+pad<=a[1]):
            prob.append(f"SOBREPOSICAO {ns[i]} x {ns[j]}")
xs=[bx(s)[0] for s in N.values()]+[bx(s)[2] for s in N.values()]+[LANE-6]
ys=[bx(s)[1] for s in N.values()]+[bx(s)[3] for s in N.values()]
W,H=max(xs)-min(xs),max(ys)-min(ys)
sc=min(170/W,247/H)
print(f"formas={len(N)}  canvas {W:.0f} x {H:.0f}")
alt = 0.92*247
k = min(170/W, alt/H)
print(f"figura de pagina inteira -> entidade {23*2.84527*min(170/W,alt/H)*1:.1f} pt "
      f"| losango {19*2.84527*k:.1f} pt | cardinalidade {16*2.84527*k:.1f} pt")
if prob:
    for p in sorted(set(prob)): print("  ",p)
    sys.exit(1)
print("OK: sem sobreposicoes")

# ---------------- emissao TikZ (figura inteira ou recorte) ----------------
S = 0.030
def P(x,y): return f"({x*S:.3f},{-y*S:.3f})"
PT = lambda u: u*S*28.4527
def FS(u): return rf"\fontsize{{{PT(u):.2f}}}{{{PT(u)*1.18:.2f}}}\selectfont"
def two(lab):
    if "_" not in lab: return [lab]
    i = lab.find("_")
    return [lab[:i+1], lab[i+1:]]
def key(sh):
    m={"DCE9F5":"acervo","E4DEF2":"user","FAE3CE":"aval","E2EFD9":"ponte",
       "FFFFFF":"neut" if sh["kind"]!="attr" else "attr"}
    return m.get(sh["fill"],"neut")
def anchor(a,b):
    A,B=N[a],N[b]; dx,dy=B["x"]-A["x"],B["y"]-A["y"]
    if dx==0 and dy==0: return (A["x"],A["y"])
    t=min(A["w"]/2/abs(dx) if dx else 1e9, A["h"]/2/abs(dy) if dy else 1e9)
    return (A["x"]+dx*t, A["y"]+dy*t)

def build(sel, fname):
    L=[r"\documentclass[border=6pt]{standalone}",
       r"\usepackage[utf8]{inputenc}\usepackage[T1]{fontenc}\usepackage{lmodern}",
       r"\usepackage{tikz}\usetikzlibrary{shapes.geometric,calc}"]
    for nm,(f,st) in [("acervo",ACERVO),("user",USER),("aval",AVAL),("ponte",PONTE),
                      ("neut",NEUT),("attr",ATTR)]:
        L.append(rf"\definecolor{{f{nm}}}{{HTML}}{{{f}}}\definecolor{{s{nm}}}{{HTML}}{{{st}}}")
    L.append(r"\begin{document}\begin{tikzpicture}[line width=0.7pt]")
    if "agregacao" in sel:
        a=N["agregacao"]
        L.append(rf"\draw[dashed,draw=suser,line width=1.1pt] "
                 rf"{P(a['x']-a['w']/2,a['y']-a['h']/2)} rectangle {P(a['x']+a['w']/2,a['y']+a['h']/2)};")
    for nm in sel:
        sh=N[nm]
        if sh["kind"]=="agg": continue
        k=key(sh); w,h=sh["w"]*S,sh["h"]*S; c=P(sh["x"],sh["y"])
        fu = F_ENT if sh["kind"] in ("ent","weak") else (F_SUB if sh["kind"]=="sub" else
             (F_ATTR if sh["kind"]=="attr" else F_REL))
        lines=[l.replace("_",r"\_") for l in two(sh["label"])] if sh["label"]!="d" else ["d"]
        if sh["kind"] in ("ent","weak","sub"):
            L.append(rf"\draw[fill=f{k},draw=s{k}] ($ {c} + (-{w/2:.3f},-{h/2:.3f}) $) rectangle ($ {c} + ({w/2:.3f},{h/2:.3f}) $);")
            if sh["kind"]=="weak":
                d=0.11
                L.append(rf"\draw[draw=s{k}] ($ {c} + (-{w/2-d:.3f},-{h/2-d:.3f}) $) rectangle ($ {c} + ({w/2-d:.3f},{h/2-d:.3f}) $);")
        elif sh["kind"] in ("rel","rel2"):
            for kk,fill in ((0,1),(1,0)) if sh["kind"]=="rel2" else ((0,1),):
                d=kk*0.12
                L.append(rf"\draw[{'fill=f'+k+',' if fill else ''}draw=s{k}] "
                         rf"($ {c} + (0,{h/2-d:.3f}) $) -- ($ {c} + ({w/2-d:.3f},0) $) -- "
                         rf"($ {c} + (0,-{h/2-d:.3f}) $) -- ($ {c} + (-{w/2-d:.3f},0) $) -- cycle;")
        elif sh["kind"]=="attr":
            L.append(rf"\draw[{'dashed,' if sh['dashed'] else ''}fill=f{k},draw=s{k}] {c} ellipse ({w/2:.3f} and {h/2:.3f});")
        elif sh["kind"]=="tri":
            L.append(rf"\draw[fill=f{k},draw=s{k}] ($ {c} + (0,{h/2:.3f}) $) -- "
                     rf"($ {c} + ({w/2:.3f},-{h/2:.3f}) $) -- ($ {c} + (-{w/2:.3f},-{h/2:.3f}) $) -- cycle;")
        if sh["kind"]=="tri":
            L.append(rf"\node at {P(sh['x'],sh['y']+14)} {{{FS(F_ENT)}\bfseries d}};")
        else:
            lh=fu*1.18; y0=sh["y"]-lh*(len(lines)-1)/2.0
            for i,ln in enumerate(lines):
                L.append(rf"\node at {P(sh['x'],y0+lh*i)} {{{FS(fu)}\ttfamily {ln}}};")
    LBL=[]
    for e in Ed:
        a,b=e["a"],e["b"]
        if a not in sel or b not in sel: continue
        if e["pts"]:
            pts=[(N[a]["x"],N[a]["y"]+N[a]["h"]/2)]+e["pts"]+[(N[b]["x"]-N[b]["w"]/2,N[b]["y"])]
            L.append(r"\draw[draw=sneut] " + " -- ".join(P(x,y) for x,y in pts) + ";")
            continue
        p,q=anchor(a,b),anchor(b,a)
        loop = {a,b} in ({"usuario","segue"},{"comentario","responde"})
        if loop:
            dx,dy=q[0]-p[0],q[1]-p[1]; n_=math.hypot(dx,dy) or 1; ox,oy=-dy/n_*30,dx/n_*30
            sg = 1 if a<b else -1
            if p[0]>q[0] or (p[0]==q[0] and p[1]>q[1]): sg=-sg
            L.append(rf"\draw[draw=sneut] {P(p[0]+ox*sg,p[1]+oy*sg)} -- {P(q[0]+ox*sg,q[1]+oy*sg)};")
        elif (a,b)==("avaliacao","tri"):
            dx,dy=q[0]-p[0],q[1]-p[1]; n_=math.hypot(dx,dy) or 1; ox,oy=-dy/n_*5,dx/n_*5
            for sg in (1,-1):
                L.append(rf"\draw[draw=sneut] {P(p[0]+ox*sg,p[1]+oy*sg)} -- {P(q[0]+ox*sg,q[1]+oy*sg)};")
        else:
            L.append(rf"\draw[draw=sneut] {P(*p)} -- {P(*q)};")
        if e["lab"]:
            near = q if N[a]["kind"] in ("rel","rel2") else p
            far  = p if N[a]["kind"] in ("rel","rel2") else q
            lx,ly = near[0]+(far[0]-near[0])*0.26, near[1]+(far[1]-near[1])*0.26
            if loop:
                lx,ly = (p[0]+q[0])/2, (p[1]+q[1])/2
                dx,dy=q[0]-p[0],q[1]-p[1]; n_=math.hypot(dx,dy) or 1
                sg = 1 if a<b else -1
                if p[0]>q[0] or (p[0]==q[0] and p[1]>q[1]): sg=-sg
                lx += -dy/n_*30*sg; ly += dx/n_*30*sg
            LBL.append([lx,ly,e["lab"],lx,ly])
    lw=lambda t: len(t)*F_CARD*0.62+14
    for _ in range(200):
        mv=False
        for i in range(len(LBL)):
            for j in range(i+1,len(LBL)):
                A_,B_=LBL[i],LBL[j]
                hx=(lw(A_[2])+lw(B_[2]))/2; hy=F_CARD*1.5
                dx,dy=B_[0]-A_[0],B_[1]-A_[1]
                ox,oy=hx-abs(dx),hy-abs(dy)
                if ox>0 and oy>0:
                    mv=True
                    if ox/hx<oy/hy:
                        f_=(ox/2+1)*(1 if dx>=0 else -1); A_[0]-=f_; B_[0]+=f_
                    else:
                        f_=(oy/2+1)*(1 if dy>=0 else -1); A_[1]-=f_; B_[1]+=f_
        for l_ in LBL: l_[0]+=(l_[3]-l_[0])*0.06; l_[1]+=(l_[4]-l_[1])*0.06
        if not mv: break
    for x,y,t,_,_ in LBL:
        L.append(rf"\node[fill=white,inner sep=0.7pt] at {P(x,y)} {{{FS(F_CARD)}\itshape {t}}};")
    L += [r"\end{tikzpicture}\end{document}"]
    open(fname,"w",encoding="utf-8").write("\n".join(L))
    bs=[bx(N[n]) for n in sel]
    return (max(b[2] for b in bs)-min(b[0] for b in bs),
            max(b[3] for b in bs)-min(b[1] for b in bs))

ALL = set(N)
REGIOES = [
 ("der-estrutural", "DER estrutural completo", ALL),
 ("der-det1-acervo", "Acervo: series, temporadas e episodios",
  {"genero","classifica","serie","possui_temporada","temporada","possui_episodio",
   "episodio","numero_t","numero_e","pessoa","participa"}),
 ("der-det2-especializacao", "Especializacao de avaliacao",
  {"serie","temporada","episodio","incide_serie","incide_temporada","incide_episodio",
   "avaliacao_serie","avaliacao_temporada","avaliacao_episodio","tri","avaliacao","total_curtidas"}),
 ("der-det3-agregacao", "Agregacao: usuario, escreve e avaliacao",
  {"avaliacao","escreve","usuario","curte","agregacao","tri","total_curtidas"}),
 ("der-det4-social", "Camada social: comentarios",
  {"comentario","responde","recebe","comenta","avaliacao","usuario"}),
 ("der-det5-acompanhamento", "Acompanhamento e grafo de seguidores",
  {"serie","episodio","declara_estado","registra","usuario","segue"}),
]
print(f"{'figura':28} {'extensao':>13}  {'largura':>8} {'altura':>7}  entidade")
for fn, desc, sel in REGIOES:
    w,h = build(sel, fn+".tex")
    wmm, hmm = w*S*10, h*S*10
    k = min(170/wmm, 236/hmm)
    print(f"  {fn:26} {w:5.0f}x{h:5.0f}  {wmm*k:6.0f}mm {hmm*k:5.0f}mm  {PT(F_ENT)*k:5.1f} pt")
