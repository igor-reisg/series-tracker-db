# -*- coding: utf-8 -*-
"""DER conceitual: layout em arcos, incide_* curtos, master + paginas de detalhe."""
import html, sys, math

C_ACERVO = "fillColor=#DCE9F5;strokeColor=#3D6E9E;"
C_USER   = "fillColor=#E4DEF2;strokeColor=#6A5A94;"
C_AVAL   = "fillColor=#FAE3CE;strokeColor=#B0703A;"
C_PONTE  = "fillColor=#E2EFD9;strokeColor=#5A8542;"
C_NEUTRO = "fillColor=#FFFFFF;strokeColor=#5A6570;"
C_ATTR   = "fillColor=#FFFFFF;strokeColor=#7A848C;"

F_ENT, F_SUB, F_REL, F_ATTR, F_CARD = 17, 15, 15, 14, 13
W_ELL, H_ELL = 148, 44
W_ENT, H_ENT = 156, 50
W_SUB, H_SUB = 196, 50
W_REL, H_REL = 160, 78
W_REL2, H_REL2 = 186, 96
W_TRI, H_TRI = 84, 66

shapes, edges = {}, []
base = {}

def S(name, kind, cx, cy, label=None, color=None, w=None, h=None, region="", extra=""):
    d = dict(ent=(W_ENT,H_ENT,"rounded=0;whiteSpace=wrap;html=1;",F_ENT),
             weak=(W_ENT,H_ENT,"rounded=0;whiteSpace=wrap;html=1;",F_ENT),
             sub=(W_SUB,H_SUB,"rounded=0;whiteSpace=wrap;html=1;",F_SUB),
             rel=(W_REL,H_REL,"shape=rhombus;perimeter=rhombusPerimeter;whiteSpace=wrap;html=1;",F_REL),
             rel2=(W_REL2,H_REL2,"shape=rhombus;perimeter=rhombusPerimeter;whiteSpace=wrap;html=1;",F_REL),
             attr=(W_ELL,H_ELL,"ellipse;whiteSpace=wrap;html=1;",F_ATTR),
             tri=(W_TRI,H_TRI,"triangle;direction=north;whiteSpace=wrap;html=1;",F_REL))[kind]
    w, h = w or d[0], h or d[1]
    style = d[2] + (color or C_NEUTRO) + f"fontSize={d[3]};align=center;verticalAlign=middle;" + extra
    base[name] = (cx, cy)
    shapes[name] = dict(name=name, kind=kind, cx=cx, cy=cy, w=w, h=h, region=region,
                        label=label if label is not None else name, style=style)

def E(a, b, label="", pts=None, ortho=True, extra=""):
    edges.append(dict(a=a, b=b, label=label, pts=pts or [], ortho=ortho, extra=extra))

def ARC(entity, names, R, t0, t1, region="", pad=18):
    """Atributos em arco. As linhas sao radiais, entao nunca cruzam as elipses irmas
    (garantia geometrica). O raio e calculado: o menor que separa todos os vizinhos."""
    ex, ey = base[entity]
    n = len(names)
    angs = [t0] if n == 1 else [t0 + (t1-t0)*i/(n-1) for i in range(n)]
    def ok(R):
        pts = [(ex+R*math.cos(math.radians(a)), ey-R*math.sin(math.radians(a))) for a in angs]
        for i in range(n-1):
            dx = abs(pts[i][0]-pts[i+1][0]); dy = abs(pts[i][1]-pts[i+1][1])
            if dx < W_ELL+pad and dy < H_ELL+pad: return False
        return True
    lo, hi = float(R), float(R)
    while not ok(hi) and hi < 4000: hi *= 1.15
    if ok(lo):
        hi = lo
    else:
        while hi-lo > 2:
            mid = (lo+hi)/2
            if ok(mid): hi = mid
            else: lo = mid
    R = hi*1.04
    for a, nm in zip(angs, names):
        r = math.radians(a)
        S(nm, "attr", ex + R*math.cos(r), ey - R*math.sin(r),
          label=nm.split("@")[0], color=C_ATTR, region=region)
        E(nm, entity, ortho=False)

# =====================================================================
# ACERVO: espinha horizontal, atributos em arco por cima
# =====================================================================
Y = 760
S("genero", "ent", 240, Y, color=C_ACERVO, region="acervo")
ARC("genero", ["id_genero@g","nome@g"], 210, 130, 50, region="acervo")
S("classifica", "rel", 600, Y, color=C_NEUTRO, region="acervo")
E("genero","classifica","(0,N)"); E("classifica","serie","(1,N)")

S("serie", "ent", 1180, Y, color=C_ACERVO, region="acervo")
ARC("serie", ["id_serie","titulo@s","titulo_original","sinopse@s","ano_estreia","situacao","pais_origem"],
    330, 160, 20, region="acervo")

S("possui_temporada", "rel2", 1780, Y, color=C_NEUTRO, region="acervo")
S("temporada", "weak", 2100, Y, color=C_ACERVO, region="acervo")
ARC("temporada", ["numero@t","titulo@t","data_estreia"], 230, 150, 30, region="acervo")
S("possui_episodio", "rel2", 2470, Y, color=C_NEUTRO, region="acervo")
S("episodio", "weak", 2860, Y, color=C_ACERVO, region="acervo")
ARC("episodio", ["numero@e","titulo@e","duracao_min","data_exibicao","sinopse@e"], 270, 160, 20, region="acervo")
for k,v in [("numero@t","<i>numero</i>"),("numero@e","<i>numero</i>")]: shapes[k]["label"] = v
E("serie","possui_temporada","(1,N)"); E("possui_temporada","temporada","(1,1)")
E("temporada","possui_episodio","(1,N)"); E("possui_episodio","episodio","(1,1)")

# pessoa pendura abaixo-esquerda da serie
S("participa", "rel", 660, 1120, color=C_NEUTRO, region="acervo")
S("pessoa", "ent", 300, 1400, color=C_ACERVO, region="acervo")
ARC("pessoa", ["id_pessoa","nome@p","data_nascimento","nacionalidade"], 250, 196, 344, region="acervo")
S("funcao", "attr", 900, 1050, color=C_ATTR, region="acervo");     E("funcao","participa",ortho=False)
S("personagem", "attr", 900, 1190, color=C_ATTR, region="acervo"); E("personagem","participa",ortho=False)
E("serie","participa","(0,N)", pts=[(1180,1120)])
E("participa","pessoa","(0,N)")

# =====================================================================
# ESPECIALIZACAO: cada subclasse fica DEBAIXO do seu alvo -> incide_* curto
# =====================================================================
S("incide_serie", "rel", 1180, 1500, color=C_NEUTRO, region="aval")
S("avaliacao_serie", "sub", 1180, 1780, color=C_AVAL, region="aval")
E("serie","incide_serie","(0,N)"); E("incide_serie","avaliacao_serie","(1,1)")

S("incide_temporada", "rel", 2100, 1500, color=C_NEUTRO, region="aval")
S("avaliacao_temporada", "sub", 2100, 1780, color=C_AVAL, region="aval")
E("temporada","incide_temporada","(0,N)"); E("incide_temporada","avaliacao_temporada","(1,1)")

S("incide_episodio", "rel", 2860, 1500, color=C_NEUTRO, region="aval")
S("avaliacao_episodio", "sub", 2860, 1780, color=C_AVAL, region="aval")
E("episodio","incide_episodio","(0,N)"); E("incide_episodio","avaliacao_episodio","(1,1)")

S("tri", "tri", 2100, 2000, label="d", color=C_AVAL, region="aval")
for s in ["avaliacao_serie","avaliacao_temporada","avaliacao_episodio"]: E(s, "tri")

S("avaliacao", "ent", 2100, 2360, color=C_AVAL, region="aval")
ARC("avaliacao", ["id_avaliacao","nota","texto@a","contem_spoiler","data_publicacao","tipo_alvo","total_curtidas"],
    360, 60, -60, region="aval")
shapes["total_curtidas"]["style"] = shapes["total_curtidas"]["style"].replace("ellipse;","ellipse;dashed=1;dashPattern=6 5;")
E("avaliacao","tri","", extra="shape=link;")     # linha dupla = especializacao total

S("escreve", "rel", 2100, 2720, color=C_NEUTRO, region="aval")
S("usuario", "ent", 2100, 3080, color=C_USER, region="usuario")
ARC("usuario", ["id_usuario","username","email","nome_exibicao","bio","data_cadastro"],
    330, 196, 344, region="usuario")
E("usuario","escreve","(0,N)"); E("escreve","avaliacao","(1,1)")
AGG = ["avaliacao","escreve","usuario"]

# =====================================================================
# ACOMPANHAMENTO: descidas laterais ate o usuario
# =====================================================================
S("declara_estado", "rel", 620, 2400, color=C_PONTE, region="usuario")
S("estado", "attr", 350, 2320, color=C_ATTR, region="usuario");           E("estado","declara_estado",ortho=False)
S("data_atualizacao", "attr", 350, 2480, color=C_ATTR, region="usuario"); E("data_atualizacao","declara_estado",ortho=False)
E("serie","declara_estado","(0,N)", pts=[(620,760)])
E("declara_estado","usuario","(0,N)", pts=[(620,3080)])

S("registra", "rel", 3560, 2400, color=C_PONTE, region="usuario")
S("data_assistido", "attr", 3560, 2200, color=C_ATTR, region="usuario"); E("data_assistido","registra",ortho=False)
E("episodio","registra","(0,N)", pts=[(3560,760)])
E("registra","usuario","(0,N)", pts=[(3560,3080)])

S("segue", "rel", 2100, 3600, color=C_NEUTRO, region="usuario")
S("data_inicio", "attr", 2360, 3600, color=C_ATTR, region="usuario"); E("data_inicio","segue",ortho=False)
E("usuario","segue","(0,N) seguidor", pts=[(1900,3600)])
E("segue","usuario","(0,N) seguido", pts=[(2300,3600)])

# =====================================================================
# SOCIAL
# =====================================================================
S("curte", "rel", 2820, 3080, color=C_NEUTRO, region="social")
S("data_curtida", "attr", 3080, 3080, color=C_ATTR, region="social"); E("data_curtida","curte",ortho=False)
E("usuario","curte","(0,N)")
E("curte","agregacao","(0,N)")

S("comentario", "ent", 1180, 3080, color=C_AVAL, region="social")
ARC("comentario", ["id_comentario","texto@c","data_publicacao@c"], 250, 196, 284, region="social")
S("recebe", "rel", 1480, 2560, color=C_NEUTRO, region="social")
E("avaliacao","recebe","(0,N)"); E("recebe","comentario","(1,1)")
S("comenta", "rel", 1640, 3080, color=C_NEUTRO, region="social")
E("usuario","comenta","(0,N)"); E("comenta","comentario","(1,1)")
S("responde", "rel", 1180, 2560, color=C_NEUTRO, region="social")
E("comentario","responde","(0,1) pai", pts=[(1060,2560)])
E("responde","comentario","(0,N) resposta", pts=[(1300,2560)])

for k,v in [("titulo@s","titulo"),("sinopse@s","sinopse"),("titulo@t","titulo"),("titulo@e","titulo"),
            ("sinopse@e","sinopse"),("nome@g","nome"),("nome@p","nome"),("id_genero@g","id_genero"),
            ("texto@a","texto"),("texto@c","texto"),("data_publicacao@c","data_publicacao")]:
    shapes[k]["label"] = v

# caixa da agregacao
_x=[shapes[m]["cx"]-shapes[m]["w"]/2 for m in AGG]+[shapes[m]["cx"]+shapes[m]["w"]/2 for m in AGG]
_y=[shapes[m]["cy"]-shapes[m]["h"]/2 for m in AGG]+[shapes[m]["cy"]+shapes[m]["h"]/2 for m in AGG]
M=34
shapes["agregacao"]=dict(name="agregacao",kind="agg",cx=(min(_x)+max(_x))/2,cy=(min(_y)+max(_y))/2,
    w=max(_x)-min(_x)+2*M, h=max(_y)-min(_y)+2*M, label="", region="aval",
    style="rounded=0;whiteSpace=wrap;html=1;dashed=1;dashPattern=10 7;fillColor=none;"
          "strokeColor=#6A5A94;strokeWidth=2;")

# =====================================================================
# VERIFICACAO
# =====================================================================
def box(s): return (s["cx"]-s["w"]/2, s["cy"]-s["h"]/2, s["cx"]+s["w"]/2, s["cy"]+s["h"]/2)
def ovl(a,b,pad=14):
    A,B=box(a),box(b)
    return not (A[2]+pad<=B[0] or B[2]+pad<=A[0] or A[3]+pad<=B[1] or B[3]+pad<=A[1])
def seg_box(p,q,bx,pad=4):
    x0,y0,x1,y1=bx[0]-pad,bx[1]-pad,bx[2]+pad,bx[3]+pad
    dx,dy=q[0]-p[0],q[1]-p[1]; t0,t1=0.0,1.0
    for pp,qq in ((-dx,p[0]-x0),(dx,x1-p[0]),(-dy,p[1]-y0),(dy,y1-p[1])):
        if pp==0:
            if qq<0: return False
        else:
            r=qq/pp
            if pp<0:
                if r>t1: return False
                t0=max(t0,r)
            else:
                if r<t0: return False
                t1=min(t1,r)
    return True
def clip(p,q,ba,bb):
    dx,dy=q[0]-p[0],q[1]-p[1]; L=math.hypot(dx,dy) or 1; ux,uy=dx/L,dy/L
    t0,t1=0.0,L
    for bx,which in ((ba,0),(bb,1)):
        t=0.0
        while t<=L:
            x,y=p[0]+ux*t,p[1]+uy*t
            if bx[0]<=x<=bx[2] and bx[1]<=y<=bx[3]:
                if which==0: t0=max(t0,t+1)
                else: t1=min(t1,t-1)
            t+=1.0
    return (p,p) if t1<=t0 else ((p[0]+ux*t0,p[1]+uy*t0),(p[0]+ux*t1,p[1]+uy*t1))

problems=[]
ns=[n for n,s in shapes.items() if s["kind"]!="agg"]
for i in range(len(ns)):
    for j in range(i+1,len(ns)):
        if ovl(shapes[ns[i]],shapes[ns[j]]): problems.append(f"SOBREPOSICAO: {ns[i]} x {ns[j]}")
for e in edges:
    if e["ortho"] or "agregacao" in (e["a"],e["b"]): continue
    a,b=shapes[e["a"]],shapes[e["b"]]
    p,q=clip((a["cx"],a["cy"]),(b["cx"],b["cy"]),box(a),box(b))
    if p==q: continue
    for n,s in shapes.items():
        if n in (e["a"],e["b"]) or s["kind"]=="agg": continue
        if seg_box(p,q,box(s),2): problems.append(f"LINHA: {e['a']}->{e['b']} passa em {n}")

xs=[box(s)[0] for s in shapes.values()]+[box(s)[2] for s in shapes.values()]
ys=[box(s)[1] for s in shapes.values()]+[box(s)[3] for s in shapes.values()]
W,H=max(xs)-min(xs),max(ys)-min(ys)
print(f"formas={len(shapes)} arestas={len(edges)}  canvas {W:.0f} x {H:.0f} (razao {W/H:.2f})")
esc_=min(170/W,247/H); print(f"master pagina inteira: atributo {F_ATTR*esc_/0.3528:.1f} pt")
if problems:
    print(f"\n{len(problems)} PROBLEMAS:")
    for p in sorted(set(problems)): print("   ",p)
    sys.exit(1)
print("OK: sem sobreposicoes e sem linhas radiais atravessando formas.")

# =====================================================================
# EMISSAO: master + visao estrutural + paginas de detalhe
# =====================================================================
def esc(t): return html.escape(t, quote=True)
adj = {}
for e in edges:
    adj.setdefault(e["a"], set()).add(e["b"]); adj.setdefault(e["b"], set()).add(e["a"])

PAGES = [
    ("DER completo",              None,        False, 420),
    ("Visao estrutural",          None,        True,  150),
    ("Detalhe 1 - Acervo",        "acervo",    False, 200),
    ("Detalhe 2 - Especializacao","aval",      False, 200),
    ("Detalhe 3 - Acompanhamento","usuario",   False, 200),
    ("Detalhe 4 - Social",        "social",    False, 200),
]

def compact(sel, maxgap):
    """Comprime os vaos vazios de cada eixo, preservando a ordem e a vizinhanca.
    E o que faz uma pagina de detalhe nao carregar o espaco vazio do master."""
    def axis(lo_hi):
        iv = sorted(lo_hi)
        merged = []
        for a, b in iv:
            if merged and a <= merged[-1][1] + 1: merged[-1][1] = max(merged[-1][1], b)
            else: merged.append([a, b])
        shift, cuts = 0.0, []
        for i in range(1, len(merged)):
            gap = merged[i][0] - merged[i-1][1]
            if gap > maxgap:
                shift += gap - maxgap
                cuts.append((merged[i][0], shift))
        return cuts
    bxs = {n: box(shapes[n]) for n in sel}
    cx = axis([(b[0], b[2]) for b in bxs.values()])
    cy = axis([(b[1], b[3]) for b in bxs.values()])
    def sh(v, cuts):
        s_ = 0.0
        for pos, acc in cuts:
            if v >= pos: s_ = acc
        return s_
    return {n: (-sh(bxs[n][0], cx), -sh(bxs[n][1], cy)) for n in sel}
LEG = ('<b>Legenda</b><br>'
       '<span style="background:#DCE9F5;">&nbsp;&nbsp;&nbsp;</span> acervo&nbsp; '
       '<span style="background:#E4DEF2;">&nbsp;&nbsp;&nbsp;</span> usuario&nbsp; '
       '<span style="background:#FAE3CE;">&nbsp;&nbsp;&nbsp;</span> avaliacao e social&nbsp; '
       '<span style="background:#E2EFD9;">&nbsp;&nbsp;&nbsp;</span> acompanhamento<br>'
       'retangulo duplo = entidade fraca &nbsp;|&nbsp; losango duplo = relacionamento identificador<br>'
       'elipse tracejada = atributo derivado &nbsp;|&nbsp; <i>numero</i> = chave parcial<br>'
       'triangulo com <b>d</b> = especializacao disjunta &nbsp;|&nbsp; linha dupla = especializacao total<br>'
       'retangulo tracejado = agregacao')

def select(region, structural):
    if region is None:
        core = {n for n, s in shapes.items() if s["kind"] != "agg"}
        if structural: core = {n for n in core if shapes[n]["kind"] != "attr"}
        return core
    core = {n for n, s in shapes.items() if s["region"] == region and s["kind"] != "agg"}
    ctx = set()
    for n in list(core):
        for m in adj.get(n, ()):
            if m in shapes and m not in core and shapes[m]["kind"] != "attr":
                ctx.add(m)
    for m in list(ctx):                      # contexto puxa o losango que o liga
        for k in adj.get(m, ()):
            if k in core and shapes[k]["kind"] in ("rel", "rel2"): pass
    return core | ctx

out = ['<mxfile host="app.diagrams.net">']
report = []
for pi, (pname, region, structural, MAXGAP) in enumerate(PAGES):
    sel = select(region, structural)
    if all(m in sel for m in AGG): sel = sel | {"agregacao"}
    off = compact(sel, MAXGAP)
    bxs = [(box(shapes[n])[0]+off[n][0], box(shapes[n])[1]+off[n][1],
            box(shapes[n])[2]+off[n][0], box(shapes[n])[3]+off[n][1]) for n in sel]
    minx, miny = min(b[0] for b in bxs), min(b[1] for b in bxs)
    maxx, maxy = max(b[2] for b in bxs), max(b[3] for b in bxs)
    ox, oy = 60 - minx, 60 - miny
    pw, ph = maxx-minx+120, maxy-miny+180
    report.append((pname, len(sel), pw, ph, F_ATTR*min(170/pw, 247/ph)/0.3528))

    out.append(f'  <diagram name="{esc(pname)}" id="p{pi}">')
    out.append(f'    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" '
               f'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{pw:.0f}" '
               f'pageHeight="{ph:.0f}" math="0" shadow="0"><root>'
               f'<mxCell id="0" /><mxCell id="1" parent="0" />')
    ids = {}
    def emit(cid, style, label, x, y, w, h):
        out.append(f'<mxCell id="{cid}" value="{esc(label)}" style="{style}" vertex="1" parent="1">'
                   f'<mxGeometry x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" as="geometry" /></mxCell>')
    if "agregacao" in sel:
        a = shapes["agregacao"]; ids["agregacao"] = f"p{pi}agg"
        adx, ady = off["agregacao"]
        emit(ids["agregacao"], a["style"], "", a["cx"]-a["w"]/2+ox+adx, a["cy"]-a["h"]/2+oy+ady, a["w"], a["h"])
    k = 0
    for n in sel:
        s = shapes[n]
        if s["kind"] == "agg": continue
        k += 1; cid = f"p{pi}n{k}"; ids[n] = cid
        dx, dy = off[n]
        x, y = s["cx"]-s["w"]/2+ox+dx, s["cy"]-s["h"]/2+oy+dy
        emit(cid, s["style"], s["label"], x, y, s["w"], s["h"])
        if s["kind"] in ("weak", "rel2"):
            inner = s["style"].split("fillColor=")[0] + "fillColor=none;strokeColor=" + \
                    s["style"].split("strokeColor=")[1].split(";")[0] + \
                    ";fontSize=1;movable=0;deletable=0;connectable=0;"
            d = 10
            emit(cid+"i", inner, "", x+d, y+d, s["w"]-2*d, s["h"]-2*d)
    for ei, e in enumerate(edges):
        if e["a"] not in ids or e["b"] not in ids: continue
        st = ("edgeStyle=orthogonalEdgeStyle;rounded=0;jettySize=auto;" if e["ortho"] else "edgeStyle=none;rounded=0;")
        st += "html=1;endArrow=none;endFill=0;strokeColor=#5A6570;" + e["extra"]
        out.append(f'<mxCell id="p{pi}e{ei}" value="" style="{st}" edge="1" parent="1" '
                   f'source="{ids[e["a"]]}" target="{ids[e["b"]]}"><mxGeometry relative="1" as="geometry">')
        if e["pts"] and MAXGAP >= 400:
            out.append('<Array as="points">' +
                       "".join(f'<mxPoint x="{px+ox:.0f}" y="{py+oy:.0f}" />' for px, py in e["pts"]) +
                       '</Array>')
        out.append('</mxGeometry></mxCell>')
        if e["label"]:
            pos = 0.76 if shapes[e["a"]]["kind"] in ("rel","rel2") else -0.76
            out.append(f'<mxCell id="p{pi}e{ei}l" value="{esc(e["label"])}" '
                       f'style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];'
                       f'fontSize={F_CARD};fontStyle=2;labelBackgroundColor=#FFFFFF;" vertex="1" '
                       f'connectable="0" parent="p{pi}e{ei}"><mxGeometry x="{pos}" relative="1" as="geometry">'
                       f'<mxPoint as="offset" /></mxGeometry></mxCell>')
    emit(f"p{pi}leg", "rounded=0;whiteSpace=wrap;html=1;fillColor=#FBFCFA;strokeColor=#B6BEB8;"
         "align=left;verticalAlign=top;fontSize=13;spacing=8;", LEG,
         60, maxy-miny+80, min(pw-120, 1500), 120)
    out.append('</root></mxGraphModel>  </diagram>')
out.append('</mxfile>')
open("der-conceitual.drawio", "w", encoding="utf-8").write("\n".join(out))

print("\npagina                          formas   canvas        texto no PDF")
for nm, n, w, h, pt in report:
    modo = "pagina inteira" if pt < 5.5 else "width=\\textwidth"
    print(f"  {nm:30} {n:4}   {w:5.0f}x{h:5.0f}   {pt:4.1f} pt")
print("\nescrito: der-conceitual.drawio")
