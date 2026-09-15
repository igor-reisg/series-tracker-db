# -*- coding: utf-8 -*-
"""Diagrama logico: 17 tabelas em pe de galinha. Emite PDF vetorial via TikZ."""
import math, sys

ACERVO=("DCE9F5","3D6E9E"); USER=("E4DEF2","6A5A94"); AVAL=("FAE3CE","B0703A")
PONTE=("E2EFD9","5A8542")

F_TAB, F_COL, F_KEY = 21, 18, 15
WT, HHDR, HROW = 268, 44, 29
S = 0.030

T = {}   # tabela -> dict
FK = []  # (tabela_filha, coluna, tabela_pai)

def tab(nome, x, y, cor, cols):
    """cols: lista de (marcador, nome). marcador em {PK, FK, PF, UK, ''}"""
    T[nome] = dict(nome=nome, x=x, y=y, cor=cor, cols=cols,
                   w=WT, h=HHDR + HROW*len(cols))
def fk(filha, col, pai): FK.append((filha, col, pai))

CA, CB, CC = 190, 640, 1090

# ---- coluna A: acervo periferico + acompanhamento ----
tab("genero", CA, 90, ACERVO, [("PK","id_genero"),("UK","nome")])
tab("serie_genero", CA, 268, ACERVO, [("PF","id_serie"),("PF","id_genero")])
tab("pessoa", CA, 470, ACERVO,
    [("PK","id_pessoa"),("","nome"),("","data_nascimento"),("","nacionalidade")])
tab("participacao", CA, 730, ACERVO,
    [("PF","id_pessoa"),("PF","id_serie"),("PK","funcao"),("","personagem")])
tab("estado_serie", CA, 958, PONTE,
    [("PF","id_usuario"),("PF","id_serie"),("","estado"),("","data_atualizacao")])
tab("registro", CA, 1286, PONTE,
    [("PK","id_registro"),("FK","id_usuario"),("FK","id_episodio"),("UK","data_assistido")])

# ---- coluna B: cadeia do acervo + subclasses ----
tab("serie", CB, 120, ACERVO,
    [("PK","id_serie"),("","titulo"),("","titulo_original"),("","sinopse"),
     ("","ano_estreia"),("","situacao"),("","pais_origem")])
tab("temporada", CB, 460, ACERVO,
    [("PK","id_temporada"),("FK","id_serie"),("UK","numero"),("","titulo"),("","data_estreia")])
tab("episodio", CB, 740, ACERVO,
    [("PK","id_episodio"),("FK","id_temporada"),("UK","numero"),("","titulo"),
     ("","duracao_min"),("","data_exibicao"),("","sinopse")])
tab("avaliacao_serie", CB, 1050, AVAL, [("PF","id_avaliacao"),("FK","id_serie")])
tab("avaliacao_temporada", CB, 1230, AVAL, [("PF","id_avaliacao"),("FK","id_temporada")])
tab("avaliacao_episodio", CB, 1410, AVAL, [("PF","id_avaliacao"),("FK","id_episodio")])

# ---- coluna C: usuario, avaliacao e social ----
tab("usuario", CC, 120, USER,
    [("PK","id_usuario"),("UK","username"),("UK","email"),("","nome_exibicao"),
     ("","bio"),("","data_cadastro")])
tab("segue", CC, 400, USER, [("PF","id_seguidor"),("PF","id_seguido"),("","data_inicio")])
tab("avaliacao", CC, 610, AVAL,
    [("PK","id_avaliacao"),("FK","id_usuario"),("","nota"),("","texto"),
     ("","contem_spoiler"),("","data_publicacao"),("","tipo_alvo"),("","total_curtidas")])
tab("curtida", CC, 950, AVAL, [("PF","id_usuario"),("PF","id_avaliacao"),("","data_curtida")])
tab("comentario", CC, 1160, AVAL,
    [("PK","id_comentario"),("FK","id_avaliacao"),("FK","id_usuario"),
     ("FK","id_comentario_pai"),("","texto"),("","data_publicacao")])

fk("serie_genero","id_serie","serie");      fk("serie_genero","id_genero","genero")
fk("participacao","id_pessoa","pessoa");    fk("participacao","id_serie","serie")
fk("temporada","id_serie","serie");         fk("episodio","id_temporada","temporada")
fk("estado_serie","id_usuario","usuario");  fk("estado_serie","id_serie","serie")
fk("registro","id_usuario","usuario");      fk("registro","id_episodio","episodio")
fk("avaliacao","id_usuario","usuario")
fk("avaliacao_serie","id_avaliacao","avaliacao");         fk("avaliacao_serie","id_serie","serie")
fk("avaliacao_temporada","id_avaliacao","avaliacao");     fk("avaliacao_temporada","id_temporada","temporada")
fk("avaliacao_episodio","id_avaliacao","avaliacao");      fk("avaliacao_episodio","id_episodio","episodio")
fk("curtida","id_usuario","usuario");       fk("curtida","id_avaliacao","avaliacao")
fk("comentario","id_avaliacao","avaliacao");fk("comentario","id_usuario","usuario")
fk("comentario","id_comentario_pai","comentario")
fk("segue","id_seguidor","usuario");        fk("segue","id_seguido","usuario")

# ---------------- verificacao ----------------
def bx(t): return (t["x"], t["y"], t["x"]+t["w"], t["y"]+t["h"])
prob=[]
ns=list(T)
for i in range(len(ns)):
    for j in range(i+1,len(ns)):
        a,b=bx(T[ns[i]]),bx(T[ns[j]]); pad=26
        if not (a[2]+pad<=b[0] or b[2]+pad<=a[0] or a[3]+pad<=b[1] or b[3]+pad<=a[1]):
            prob.append(f"SOBREPOSICAO {ns[i]} x {ns[j]}")
for f_,c,p_ in FK:
    if f_ not in T or p_ not in T: prob.append(f"FK invalida {f_}.{c} -> {p_}")
    elif c not in [n for _,n in T[f_]["cols"]]: prob.append(f"coluna inexistente {f_}.{c}")
xs=[v for t in T.values() for v in (bx(t)[0],bx(t)[2])]
ys=[v for t in T.values() for v in (bx(t)[1],bx(t)[3])]
W,H=max(xs)-min(xs),max(ys)-min(ys)
print(f"tabelas={len(T)} colunas={sum(len(t['cols']) for t in T.values())} fks={len(FK)}")
print(f"canvas {W:.0f} x {H:.0f}  ->  fonte da tabela "
      f"{F_TAB*2.84527*min(170/W,236/H):.1f} pt | coluna {F_COL*2.84527*min(170/W,236/H):.1f} pt")
if prob:
    for x in sorted(set(prob)): print("  ",x)
    sys.exit(1)
print("OK: sem sobreposicoes, todas as FK validas")

# ---------------- TikZ ----------------
def P(x,y): return f"({x*S:.3f},{-y*S:.3f})"
PT=lambda u: u*S*28.4527
def FS(u): return rf"\fontsize{{{PT(u):.2f}}}{{{PT(u)*1.2:.2f}}}\selectfont"

def rowy(t,i): return t["y"]+HHDR+HROW*i+HROW/2      # centro vertical da linha i
def colrow(t,c):
    for i,(m,n) in enumerate(T[t]["cols"]):
        if n==c: return i
    return 0

def build(sel, fname):
    L=[r"\documentclass[border=6pt]{standalone}",
       r"\usepackage[utf8]{inputenc}\usepackage[T1]{fontenc}\usepackage{lmodern}",
       r"\usepackage{tikz}\usetikzlibrary{calc}"]
    for nm,(f,st) in [("acervo",ACERVO),("user",USER),("aval",AVAL),("ponte",PONTE)]:
        L.append(rf"\definecolor{{f{nm}}}{{HTML}}{{{f}}}\definecolor{{s{nm}}}{{HTML}}{{{st}}}")
    L.append(r"\definecolor{linha}{HTML}{5A6570}\definecolor{cinza}{HTML}{8A939A}")
    L.append(r"\begin{document}\begin{tikzpicture}[line width=0.7pt]")
    k={"DCE9F5":"acervo","E4DEF2":"user","FAE3CE":"aval","E2EFD9":"ponte"}
    for nm in sel:
        t=T[nm]; c=k[t["cor"][0]]
        x0,y0,x1,y1 = bx(t)
        L.append(rf"\draw[fill=white,draw=s{c}] {P(x0,y0)} rectangle {P(x1,y1)};")
        L.append(rf"\draw[fill=f{c},draw=s{c}] {P(x0,y0)} rectangle {P(x1,y0+HHDR)};")
        esc_nm = nm.replace("_", "\\_")
        L.append(rf"\node[anchor=west] at {P(x0+14, y0+HHDR/2)} "
                 rf"{{{FS(F_TAB)}\ttfamily\bfseries {esc_nm}}};")
        for i,(mk,cn) in enumerate(t["cols"]):
            yy=rowy(t,i)
            if i: L.append(rf"\draw[draw=cinza,line width=0.25pt] {P(x0,y0+HHDR+HROW*i)} -- {P(x1,y0+HHDR+HROW*i)};")
            if mk: L.append(rf"\node[anchor=west] at {P(x0+12,yy)} {{{FS(F_KEY)}\ttfamily {mk}}};")
            und = r"\underline" if mk in ("PK","PF") else ""
            esc_cn = cn.replace("_", "\\_")
            L.append(rf"\node[anchor=west] at {P(x0+62,yy)} "
                     rf"{{{FS(F_COL)}\ttfamily {und}{{{esc_cn}}}}};")
    # ---- roteador: corredores verticais verificados contra as caixas ----
    boxes = {n: bx(T[n]) for n in sel}
    def livre(seg, ign):
        (ax,ay),(bx_,by) = seg
        x0,x1 = sorted((ax,bx_)); y0,y1 = sorted((ay,by))
        for n,(bx0,by0,bx1,by1) in boxes.items():
            if n in ign: continue
            if x1 >= bx0-8 and bx1+8 >= x0 and y1 >= by0-8 and by1+8 >= y0: return False
        return True
    ocupado = {}
    xs_all = sorted({v for b in boxes.values() for v in (b[0],b[2])})
    cands = [x for x in range(int(min(xs_all))-140, int(max(xs_all))+150, 12)
             if all(not (b[0]-30 < x < b[2]+30) for b in boxes.values())]
    for f_,cn,p_ in FK:
        if f_ not in sel or p_ not in sel: continue
        ch,pa = T[f_],T[p_]
        ry = rowy(ch,colrow(f_,cn)); py = rowy(pa,0)
        if f_ == p_:
            x1 = ch["x"]+ch["w"]; lane = x1+58
            L.append(rf"\draw[draw=linha] {P(x1,ry)} -- {P(lane,ry)} -- {P(lane,py)} -- {P(x1,py)};")
            for dy in (-13,0,13):
                L.append(rf"\draw[draw=linha,line width=0.5pt] {P(x1,ry)} -- {P(x1+24,ry+dy)};")
            L.append(rf"\draw[draw=linha,line width=0.5pt] {P(x1+16,py-13)} -- {P(x1+16,py+13)};")
            continue
        alvo = (ch["x"]+ch["w"]/2 + pa["x"]+pa["w"]/2)/2
        escolhido = None
        for lane in sorted(cands, key=lambda v: abs(v-alvo)):
            cx = ch["x"]+ch["w"] if lane > ch["x"]+ch["w"]/2 else ch["x"]
            px = pa["x"]+pa["w"] if lane > pa["x"]+pa["w"]/2 else pa["x"]
            if not livre(((cx,ry),(lane,ry)), {f_}): continue
            if not livre(((lane,ry),(lane,py)), set()): continue
            if not livre(((lane,py),(px,py)), {p_}): continue
            lo,hi = sorted((ry,py))
            if any(not (hi < a-15 or b_ < lo-15) for a,b_ in ocupado.get(lane,[])): continue
            escolhido = (lane,cx,px); break
        if not escolhido:
            print("  SEM ROTA:", f_, cn, "->", p_); continue
        lane,cx,px = escolhido
        ocupado.setdefault(lane,[]).append(tuple(sorted((ry,py))))
        L.append(rf"\draw[draw=linha] {P(cx,ry)} -- {P(lane,ry)} -- {P(lane,py)} -- {P(px,py)};")
        d = 24 if lane > cx else -24
        for dy in (-13,0,13):
            L.append(rf"\draw[draw=linha,line width=0.5pt] {P(cx,ry)} -- {P(cx+d,ry+dy)};")
        e = 16 if lane > px else -16
        L.append(rf"\draw[draw=linha,line width=0.5pt] {P(px+e,py-13)} -- {P(px+e,py+13)};")
    L.append(r"\end{tikzpicture}\end{document}")
    open(fname,"w",encoding="utf-8").write("\n".join(L))
    bs=[bx(T[n]) for n in sel]
    return (max(b[2] for b in bs)-min(b[0] for b in bs),
            max(b[3] for b in bs)-min(b[1] for b in bs))

REG=[("der-logico","completo",set(T)),
     ("der-log-det1-acervo","acervo",{"genero","serie_genero","serie","temporada","episodio","pessoa","participacao"}),
     ("der-log-det2-avaliacao","avaliacao",{"avaliacao","avaliacao_serie","avaliacao_temporada","avaliacao_episodio"})]
print(f"\n{'figura':26} {'extensao':>13}  fonte da tabela")
for fn,_,sel in REG:
    w,h=build(sel,fn+".tex")
    kk=min(170/(w*S*10),236/(h*S*10))
    print(f"  {fn:24} {w:5.0f}x{h:5.0f}   {PT(F_TAB)*kk:5.1f} pt")
