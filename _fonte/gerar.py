#!/usr/bin/env python3
"""Gera as páginas estáticas do site (PT e EN) a partir de dados.py.

Uso:  python3 _fonte/gerar.py      (a partir da pasta paginas-html-v2)
O resultado são arquivos .html comuns; editar o HTML direto também funciona,
mas a próxima geração sobrescreve. Prefira editar dados.py / este arquivo.
"""
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from dados import (ATUALIZADO, BASE_URL, COLAB, EMAIL_D, EMAIL_U, LINKS,  # noqa: E402
                   ORIENTACOES, PREMIOS, PUBS, TEMAS)

ROOT = Path(__file__).resolve().parent.parent
E = html.escape

PAGES = [  # chave, arquivo pt, arquivo en, rótulo pt, rótulo en
    ("inicio", "index.html", "index.html", "Início", "Home"),
    ("ensino", "ensino.html", "teaching.html", "Ensino", "Teaching"),
    ("orientacao", "orientacao.html", "advising.html", "Orientação", "Advising"),
    ("publicacoes", "publicacoes.html", "publications.html", "Produção", "Publications"),
    ("pesquisa", "pesquisa.html", "research.html", "Pesquisa", "Research"),
    ("extensao", "extensao.html", "outreach.html", "Extensão", "Outreach"),
]
FILE = {k: {"pt": pt, "en": en} for k, pt, en, _, _ in PAGES}
LABEL = {k: {"pt": lp, "en": le} for k, _, _, lp, le in PAGES}


def T(lang, pt, en):
    return pt if lang == "pt" else en


def href(lang, key):
    return FILE[key][lang]


# ---------------------------------------------------------------- componentes

def email(lang, subject=None, show=True):
    subj = f' data-subject="{E(subject)}"' if subject else ""
    copy = T(lang, "Copiar", "Copy")
    done = T(lang, "Copiado", "Copied")
    return (f'<span class="email-row"><a class="email" data-email data-show data-u="{EMAIL_U}" data-d="{EMAIL_D}"{subj}>'
            f'{EMAIL_U} [{T(lang, "arroba", "at")}] {EMAIL_D}</a>'
            f'<button type="button" class="copy" data-u="{EMAIL_U}" data-d="{EMAIL_D}" data-done="{done}">{copy}</button></span>')


def mail_btn(lang, text, subject, cls="btn"):
    return (f'<a class="{cls}" data-email data-u="{EMAIL_U}" data-d="{EMAIL_D}" data-subject="{E(subject)}" '
            f'href="#contato">{text}</a>')


def venue(p, lang):
    parts = [f'<i>{E(p["revista"])}</i>']
    if p.get("vol"):
        parts.append(f'v. {p["vol"]}' if lang == "pt" else f'vol. {p["vol"]}')
    if p.get("num"):
        parts.append(f'n. {p["num"]}' if lang == "pt" else f'no. {p["num"]}')
    if p.get("pag"):
        multi = "–" in p["pag"]
        parts.append((("p. " if lang == "pt" else "pp. ") if multi else ("art. " if lang == "pt" else "art. ")) + p["pag"])
    parts.append(str(p["ano"]))
    return ", ".join(parts) + "."


def pub_item(p, lang, show_year=True):
    authors = []
    for a in p["autores"].split("; "):
        sur = a.split(" ")[-1]
        if a == "M. Martin":
            authors.append(f"<b>{E(a)}</b>")
        elif sur in p.get("st", []):
            authors.append(f'<span class="st">{E(a)}</span>')
        else:
            authors.append(E(a))
    tema = TEMAS[p["tema"]][lang]
    year = f'<span class="year">{p["ano"]}</span>' if show_year else '<span class="year"></span>'
    return (f'<li class="pub" data-topic="{p["tema"]}">{year}<div class="body">'
            f'<h3>{E(p["titulo"])}</h3>'
            f'<p class="authors">{", ".join(authors)}</p>'
            f'<p class="venue">{venue(p, lang)}</p>'
            f'<p class="meta"><span class="tag">{E(tema)}</span>'
            f'<a class="doi" href="https://doi.org/{E(p["doi"])}" target="_blank" rel="noopener">doi:{E(p["doi"])}</a></p>'
            f'</div></li>')


def section(inner, cls="section", id_=None):
    i = f' id="{id_}"' if id_ else ""
    return f'<section class="{cls}"{i}><div class="wrap">{inner}</div></section>'


def head_block(eyebrow, title, intro=""):
    return (f'<div class="section-head"><p class="eyebrow">{eyebrow}</p><h2>{title}</h2>'
            + (f'<p class="muted">{intro}</p>' if intro else "") + "</div>")


def page_head(lang, eyebrow, title, lead):
    return (f'<header class="page-head"><div class="wrap" style="display:grid;gap:1rem">'
            f'<p class="eyebrow">{eyebrow}</p><h1>{title}</h1><p class="lead">{lead}</p></div></header>')


def logos_band(lang, pre):
    return f'''<section class="logos-band" aria-labelledby="logos-t"><div class="wrap">
<img src="{pre}figuras/logos-claro.png" alt="LOGOS: Laboratório de Otimização em Gestão de Operações Sustentáveis" width="900" height="160" loading="lazy">
<div class="text"><p class="eyebrow">{T(lang, "Laboratório", "Lab")}</p>
<h2 id="logos-t">LOGOS</h2>
<p>{T(lang,
 "O Laboratório de Otimização em Gestão de Operações Sustentáveis reúne os estudantes de iniciação científica e de mestrado que oriento na UFSCar Sorocaba. O grupo desenvolve modelos matemáticos e algoritmos para problemas reais de produção e logística, sempre com código, instâncias e resultados reprodutíveis.",
 "The Laboratory of Optimization in Sustainable Operations Management (LOGOS) brings together the undergraduate research and master's students I supervise at UFSCar Sorocaba. The group develops mathematical models and algorithms for real production and logistics problems, with reproducible code, instances and results.")}</p>
<p><a href="{href(lang, "orientacao")}">{T(lang, "Conheça os membros e como participar", "Meet the members and learn how to join")}</a></p>
</div></div></section>'''


# ---------------------------------------------------------------- páginas

def page_inicio(lang, pre):
    n_pubs = len(PUBS)
    n_conc = len(ORIENTACOES["concluidas"])
    n_and = len(ORIENTACOES["andamento"])
    ids = "".join(f'<a href="{u}" target="_blank" rel="noopener">{E(n)}</a>' for n, u in LINKS)
    hero = f'''<section class="hero"><div class="wrap">
<div class="hero-text">
<p class="eyebrow">{T(lang, "Pesquisa Operacional · Engenharia de Produção", "Operations Research · Industrial Engineering")}</p>
<h1>Mateus Pereira Martin<span>{T(lang, "Professor do Departamento de Engenharia de Produção da UFSCar, campus Sorocaba", "Professor of Industrial Engineering at the Federal University of São Carlos (UFSCar), Sorocaba campus")}</span></h1>
<p class="lead">{T(lang,
 "Desenvolvo modelos matemáticos e algoritmos para decisões de produção e logística: como cortar, empacotar, programar e transportar com menos desperdício e menos custo.",
 "I develop mathematical models and algorithms for production and logistics decisions: how to cut, pack, schedule and transport with less waste and lower cost.")}</p>
<div class="ids">{ids}</div>
</div>
<figure class="hero-art" style="margin:0">
<img class="photo" src="{pre}figuras/mateus.jpg" alt="{T(lang, "Foto de Mateus Pereira Martin", "Photo of Mateus Pereira Martin")}" width="720" height="960">
</figure>
</div></section>'''

    facts = f'''<div class="wrap"><dl class="facts">
<div><dt>{T(lang, "orientações concluídas", "completed supervisions")}</dt><dd>{n_conc}</dd></div>
<div><dt>{T(lang, "orientações em andamento", "ongoing supervisions")}</dt><dd>{n_and}</dd></div>
<div><dt>{T(lang, "artigos em periódicos", "journal articles")}</dt><dd>{n_pubs}</dd></div>
<div><dt>{T(lang, "projetos financiados (CNPq, FAPESP)", "funded projects (CNPq, FAPESP)")}</dt><dd>3</dd></div>
</dl></div>'''

    tl_items = [
        ("2024 –", T(lang, "Professor, Departamento de Engenharia de Produção (DEP-So), UFSCar Sorocaba", "Professor, Department of Industrial Engineering (DEP-So), UFSCar Sorocaba"),
         T(lang, "Docente credenciado no Programa de Pós-Graduação em Engenharia de Produção (PPGEPS)", "Faculty member of the Graduate Program in Industrial Engineering (PPGEPS)")),
        ("2021 – 2024", T(lang, "Professor, Universidade Federal Fluminense (UFF), Petrópolis", "Professor, Fluminense Federal University (UFF), Petrópolis"),
         T(lang, "Docente do mestrado profissional em Engenharia de Produção da UFF em Volta Redonda (2023 – 2026)", "Faculty member of UFF's professional master's program in Industrial Engineering, Volta Redonda (2023 – 2026)")),
        ("2020 – 2021", T(lang, "Pós-doutorado em Pesquisa Operacional", "Postdoctoral researcher in Operations Research"),
         "PPGPO, UNIFESP/ITA"),
        ("2016 – 2019", T(lang, "Doutorado em Engenharia de Produção", "PhD in Industrial Engineering"),
         T(lang, "PPGEP/UFSCar, com doutorado-sanduíche na Faculdade de Engenharia da Universidade do Porto (out/2018 – set/2019).",
           "PPGEP/UFSCar, with a visiting period at the Faculty of Engineering of the University of Porto (Oct 2018 – Sep 2019).")),
        ("2014 – 2016", T(lang, "Mestrado em Engenharia Elétrica", "MSc in Electrical Engineering"), "FEEC/UNICAMP"),
        ("2009 – 2013", T(lang, "Bacharelado em Engenharia de Produção", "BSc in Industrial Engineering"),
         T(lang, "FCA/UNICAMP, com intercâmbio na Universitat Politècnica de València (fev – jul/2012)", "FCA/UNICAMP, with an exchange semester at the Universitat Politècnica de València (Feb – Jul 2012)")),
    ]
    tl = "".join(f'<li><span class="when">{w}</span><div><strong>{t}</strong><span>{s}</span></div></li>' for w, t, s in tl_items)

    areas = [
        (T(lang, "Pesquisa Operacional e Otimização", "Operations Research and Optimization"),
         T(lang, "Desenvolvimento e aplicação de abordagens baseadas em Programação Linear Inteira Mista e Programação por Restrições para a resolução de problemas em sistemas produtivos e logísticos. O foco reside na modelagem matemática para otimização de recursos, com aplicações que abrangem desde problemas de manufatura, como corte e empacotamento, até a programação de operações industriais, incluindo gestão de pátios e logística de transportes.",
           "Development and application of approaches based on Mixed-Integer Linear Programming and Constraint Programming to solve problems in production and logistics systems. The focus is on mathematical modeling for resource optimization, with applications ranging from manufacturing problems, such as cutting and packing, to the scheduling of industrial operations, including yard management and transport logistics.")),
        (T(lang, "Gestão de Sistemas Produtivos e Logísticos", "Management of Production and Logistics Systems"),
         T(lang, "Estudo e aprimoramento de sistemas produtivos e logísticos, com ênfase no planejamento da produção, gestão da cadeia de suprimentos, logística e transformação digital. As atividades concentram-se na análise e no redesenho de processos, na coordenação de fluxos de materiais e informações e na construção de operações mais eficientes, resilientes e sustentáveis.",
           "Study and improvement of production and logistics systems, with emphasis on production planning, supply chain management, logistics and digital transformation. Activities focus on analyzing and redesigning processes, coordinating material and information flows, and building more efficient, resilient and sustainable operations.")),
        (T(lang, "Inteligência Artificial", "Artificial Intelligence"),
         T(lang, "Integração entre Pesquisa Operacional e Aprendizado de Máquina por meio do desenvolvimento de abordagens híbridas para apoio à tomada de decisão. Busca-se combinar a capacidade preditiva do Aprendizado de Máquina ao rigor prescritivo da Pesquisa Operacional em aplicações voltadas à gestão de operações em sistemas produtivos e logísticos.",
           "Integration of Operations Research and Machine Learning through hybrid approaches for decision support. The aim is to combine the predictive power of Machine Learning with the prescriptive rigor of Operations Research in applications to operations management in production and logistics systems.")),
    ]
    areas_html = "".join(f'<div class="item"><h3>{a}</h3><p>{b}</p></div>' for a, b in areas)

    recent = "".join(pub_item(p, lang) for p in PUBS[:3])

    return (hero + facts
            + section(head_block(T(lang, "Atuação", "Focus"), T(lang, "Áreas de atuação", "Areas of work")) + f'<div class="cols">{areas_html}</div>')
            + section(head_block(T(lang, "Trajetória", "Background"), T(lang, "Formação e carreira", "Education and career")) + f'<ol class="timeline" reversed>{tl}</ol>')
            + section(head_block(T(lang, "Distinções", "Awards"), T(lang, "Prêmios e distinções", "Awards and honors"))
                      + '<ol class="timeline">' + "".join(f'<li><span class="when">{p["ano"]}</span><div><span style="color:var(--ink)">{E(p[lang])}</span></div></li>' for p in PREMIOS) + '</ol>')
            + logos_band(lang, pre)
            + section(head_block(T(lang, "Publicações", "Publications"), T(lang, "Artigos mais recentes", "Latest articles"))
                      + f'<ul class="pubs">{recent}</ul><p style="margin-top:1.5rem"><a class="btn btn-ghost" href="{href(lang, "publicacoes")}">'
                      + T(lang, f"Ver os {n_pubs} artigos", f"See all {n_pubs} articles") + "</a></p>"))


def page_pesquisa(lang, pre):
    lines = [
        ("problema-corte.png", T(lang, "Corte e empacotamento", "Cutting and packing"),
         T(lang, "Problemas de corte (1D, 2D e 3D) e de empacotamento para reduzir o desperdício de matéria-prima e otimizar o arranjo de peças em processos industriais, como no corte de chapas de aço, vidro e madeira.",
           "Cutting (1D, 2D and 3D) and packing problems that reduce raw-material waste and optimize piece layouts in industrial processes such as cutting steel, glass and wood."),
         ["CSP", "2D-ODRPP", "3D-ODRPP", "2BPP-OS"]),
        ("problema-scheduling.png", T(lang, "Programação da produção e manutenção", "Production and maintenance scheduling"),
         T(lang, "Sequenciamento de operações com recursos limitados, da minimização de pilhas abertas à montagem estrutural e à manutenção de aeronaves.",
           "Sequencing operations under limited resources, from minimizing open stacks to aircraft structural assembly and maintenance."),
         ["MOSP", "ASASP", "RCPSP"]),
        ("problema-logistica.png", T(lang, "Logística", "Logistics"),
         T(lang, "Modelos para operações logísticas, como a realocação de blocos em pátios e depósitos e a recuperação de voos para unidades marítimas de petróleo e gás.",
           "Models for logistics operations such as block relocation in yards and warehouses and flight recovery for offshore oil and gas units."),
         ["BRP", "ARP"]),
    ]
    acr_note = T(lang, "Siglas dos problemas na literatura", "Problem acronyms used in the literature")
    lines_html = "".join(
        f'<div class="item"><div class="figure"><img src="{pre}figuras/{img}" alt="{E(t)}" loading="lazy"></div><h3>{t}</h3><p>{d}</p>'
        f'<div class="tags" aria-label="{acr_note}">' + "".join(f'<span class="tag tag-green">{a}</span>' for a in acr) + "</div></div>"
        for img, t, d, acr in lines)

    projects = [
        ("CNPq · Universal 10/2023", T(lang, "Métodos inteligentes de otimização para problemas de escalonamento e roteamento", "Intelligent optimization methods for scheduling and routing problems"),
         T(lang, "Escalonamento e roteamento de veículos com restrições reais (prioridades, janelas de tempo, incerteza), com métodos exatos e meta-heurísticas para logística e assistência médico-hospitalar. Coordenação: Thiago Alves de Queiroz.",
           "Scheduling and vehicle routing with real constraints (priorities, time windows, uncertainty), using exact methods and metaheuristics for logistics and healthcare. Coordinator: Thiago Alves de Queiroz.")),
        ("FAPESP · Temático 2022/05803-3", T(lang, "Problemas de corte, empacotamento, dimensionamento de lotes, programação da produção, roteamento e localização e suas integrações em contextos industriais e logísticos",
                                            "Cutting, packing, lot-sizing, scheduling, routing and location problems and their integration in industrial and logistics settings"),
         T(lang, "Modelos e algoritmos para problemas integrados de planejamento, em cooperação entre a academia e o setor produtivo.",
           "Models and algorithms for integrated planning problems, in cooperation between academia and industry.")),
        ("CNPq · Universal", T(lang, "Soluções integradas para problemas logísticos complexos via otimização", "Integrated solutions for complex logistics problems via optimization"),
         T(lang, "Modelos matemáticos e algoritmos para problemas integrados de localização, roteamento e programação de operações logísticas.",
           "Mathematical models and algorithms for integrated location, routing and logistics scheduling problems.")),
    ]
    proj_html = "".join(
        f'<li class="person"><div class="who"><span class="tag tag-orange">{a}</span><span class="muted" style="font-size:.9rem">{T(lang, "Pesquisador integrante", "Team member")}</span></div>'
        f'<div class="what"><h3>{t}</h3><p>{d}</p></div></li>' for a, t, d in projects)

    recent = "".join(pub_item(p, lang) for p in PUBS[:5])

    return (page_head(lang, T(lang, "Pesquisa", "Research"), T(lang, "Otimização para a produção e a logística", "Optimization for production and logistics"),
                      T(lang, "A Pesquisa Operacional usa matemática para encontrar a melhor decisão entre milhões de alternativas: a rota de uma frota, a ordem de produção de uma fábrica, o corte de uma chapa. Meu trabalho propõe formulações exatas e algoritmos eficazes para problemas clássicos da área e para as variantes que aparecem na indústria.",
                        "Operations Research uses mathematics to find the best decision among millions of alternatives: a fleet's routes, a plant's production sequence, how to cut a sheet. My work proposes exact formulations and effective algorithms for classic problems in the field and for the variants that arise in industry."))
            + section(head_block(T(lang, "Linhas", "Topics"), T(lang, "Linhas de pesquisa", "Research topics")) + f'<div class="cols">{lines_html}</div>')
            + section(head_block(T(lang, "Financiamento", "Funding"), T(lang, "Projetos em andamento", "Ongoing projects")) + f'<ul class="people">{proj_html}</ul>')
            + logos_band(lang, pre)
            + section(head_block(T(lang, "Produção", "Output"), T(lang, "Publicações recentes", "Recent publications"))
                      + f'<ul class="pubs">{recent}</ul><div class="actions" style="margin-top:1.5rem">'
                      + f'<a class="btn btn-ghost" href="{href(lang, "publicacoes")}">{T(lang, "Lista completa de publicações", "Full publication list")}</a>'
                      + f'<a class="btn btn-ghost" href="{href(lang, "extensao")}">{T(lang, "Parcerias com empresas", "Industry partnerships")}</a></div>'))


def page_publicacoes(lang, pre):
    counts = {k: sum(1 for p in PUBS if p["tema"] == k) for k in TEMAS}
    chips = [f'<button type="button" class="chip" data-topic="all" aria-pressed="true">{T(lang, "Todas", "All")}<span class="n">{len(PUBS)}</span></button>']
    chips += [f'<button type="button" class="chip" data-topic="{k}" aria-pressed="false">{E(v[lang])}<span class="n">{counts[k]}</span></button>'
              for k, v in TEMAS.items() if counts[k]]
    items = []
    last = None
    for p in PUBS:
        items.append(pub_item(p, lang, show_year=True))
        last = p["ano"]
    fmt = T(lang, "{n} artigos", "{n} articles")
    body = f'''<div class="filters" role="group" aria-label="{T(lang, "Filtrar por tema", "Filter by topic")}">{"".join(chips)}
<label class="skip" for="pub-search">{T(lang, "Buscar", "Search")}</label>
<input class="search" id="pub-search" type="search" placeholder="{T(lang, "Buscar por título, autor ou revista", "Search title, author or journal")}"></div>
<p class="count" id="pub-count" data-fmt="{fmt}">{fmt.replace("{n}", str(len(PUBS)))}</p>
<ol class="pubs" id="pub-list" reversed>{"".join(items)}</ol>
<p class="empty" id="pub-empty" hidden>{T(lang, "Nenhum artigo encontrado. Tente outro termo ou o filtro Todas.", "No articles found. Try another term or the All filter.")}</p>
<p class="legend">{T(lang, '<b>Negrito</b>: Mateus Martin. <span class="st">Sublinhado pontilhado</span>: orientando(a) como coautor(a).', '<b>Bold</b>: Mateus Martin. <span class="st">Dotted underline</span>: supervised student as co-author.')}
{T(lang, "Listas sempre atualizadas também no", "Always-current lists are also on")} <a href="{LINKS[2][1]}" target="_blank" rel="noopener">Google Scholar</a> {T(lang, "e no", "and")} <a href="{LINKS[0][1]}" target="_blank" rel="noopener">{T(lang, "Currículo Lattes", "Lattes CV")}</a>.</p>'''
    return (page_head(lang, T(lang, "Produção", "Publications"), T(lang, "Artigos em periódicos", "Journal articles"),
                      T(lang, f"Os {len(PUBS)} artigos de {min(p['ano'] for p in PUBS)} a {max(p['ano'] for p in PUBS)}, do mais recente ao mais antigo, pelo ano do fascículo. Filtre por tema ou busque por palavra.",
                        f"All {len(PUBS)} articles from {min(p['ano'] for p in PUBS)} to {max(p['ano'] for p in PUBS)}, newest first by issue year. Filter by topic or search by keyword."))
            + section(body))


def person(o, lang):
    nivel = {"ic": T(lang, "Iniciação científica", "Undergraduate research"), "mestrado": T(lang, "Mestrado", "Master's")}[o["nivel"]]
    tags = f'<span class="tag tag-green">{nivel}</span>'
    if o.get("coorientacao"):
        tags += f'<span class="tag">{T(lang, "Coorientação", "Co-supervision")}</span>'
    if o.get("fomento"):
        tags += f'<span class="tag tag-orange">{o["fomento"]}</span>'
    if o.get("ano"):
        tags += f'<span class="tag">{o["ano"]}</span>'
    curso = o["curso"] if lang == "pt" else (o["curso"].replace("Engenharia de Produção", "Industrial Engineering")
                                              .replace("Mestrado Profissional", "Professional master's"))
    extra = ""
    if o.get("pub"):
        p = next(x for x in PUBS if x["n"] == o["pub"])
        extra = (f'<p>{T(lang, "Coautor(a) do artigo", "Co-author of")} <a href="https://doi.org/{p["doi"]}" target="_blank" rel="noopener">'
                 f'“{E(p["titulo"])}”</a> (<i>{E(p["revista"])}</i>, {p["ano"]}).</p>')
    title = o.get(lang)
    if o.get("premio"):
        extra += (f'<p><span class="tag tag-orange">{T(lang, "Menção honrosa", "Honorable mention")}</span> '
                  + T(lang, "Prêmio ABEPRO &amp; Lean Way 2026, XLVI ENEGEP.", "ABEPRO &amp; Lean Way Award 2026, XLVI ENEGEP.") + "</p>")
    return (f'<li class="person"><div class="who"><strong>{E(o["nome"])}</strong><span class="muted" style="font-size:.88rem">{E(curso)}</span>'
            f'<div class="tags">{tags}</div></div><div class="what">'
            + (f'<h3 style="font-size:1.02rem;font-family:var(--font-body);font-weight:600;line-height:1.45">{E(title)}</h3>' if title else "")
            + f'{extra}</div></li>')


def page_orientacao(lang, pre):
    and_ = "".join(person(o, lang) for o in ORIENTACOES["andamento"])
    conc = "".join(person(o, lang) for o in ORIENTACOES["concluidas"])
    en_note = "" if lang == "pt" else '<p class="muted" style="font-size:.88rem;margin-bottom:1rem">Project titles translated from Portuguese.</p>'
    steps = [
        (T(lang, "Escolha um tema", "Pick a topic"),
         T(lang, "Veja as linhas de pesquisa e as publicações recentes. Não é preciso ter um tema fechado; uma área de interesse basta para começar a conversa.",
           "Look at the research topics and recent publications. You do not need a finished idea; an area of interest is enough to start.")),
        (T(lang, "Envie um e-mail", "Send an email"),
         T(lang, "Conte em poucas linhas seu curso, seu interesse e sua disponibilidade. Anexe o histórico escolar e o link do Currículo Lattes.",
           "Briefly describe your program, your interests and your availability. Attach your transcript and a CV.")),
        (T(lang, "Conversa e treinamento", "Meeting and onboarding"),
         T(lang, "Marcamos uma conversa. Em seguida vem um período de estudo com leituras e implementação em Python e solvers de otimização.",
           "We schedule a meeting, followed by a study period with readings and implementation in Python and optimization solvers.")),
        (T(lang, "Projeto e bolsa", "Proposal and funding"),
         T(lang, "Escrevemos juntos o projeto para pedir bolsa: FAPESP ou PIBIC/CNPq na iniciação científica; no mestrado, o ingresso é pelo processo seletivo do PPGEPS.",
           "We write the proposal together to apply for a scholarship: FAPESP or PIBIC/CNPq for undergraduate research; for the master's, admission is through the PPGEPS selection process.")),
    ]
    steps_html = "".join(f'<li><div><h3>{a}</h3><p>{b}</p></div></li>' for a, b in steps)
    profile = [
        T(lang, "Estudantes de Engenharia de Produção, Engenharias, Computação, Matemática ou áreas afins", "Students in industrial engineering, other engineering fields, computer science, mathematics or related areas"),
        T(lang, "Gosto por resolução de problemas, modelagem matemática e programação", "Enjoy problem solving, mathematical modeling and programming"),
        T(lang, "Disponibilidade semanal regular para o projeto", "Regular weekly time for the project"),
    ]
    return (page_head(lang, T(lang, "Orientação", "Advising"), T(lang, "Orientandos e oportunidades", "Students and opportunities"),
                      T(lang, "Oriento iniciação científica na graduação em Engenharia de Produção da UFSCar Sorocaba e mestrado no PPGEPS. Os projetos partem de problemas reais e costumam resultar em artigos com os estudantes como coautores.",
                        "I supervise undergraduate research in Industrial Engineering at UFSCar Sorocaba and master's students in PPGEPS. Projects start from real problems and often lead to articles co-authored by the students."))
            + section(head_block(T(lang, "Em andamento", "Ongoing"), T(lang, "Orientações em andamento", "Current students")) + en_note + f'<ul class="people">{and_}</ul>')
            + section(head_block(T(lang, "Concluídas", "Completed"), T(lang, "Orientações concluídas", "Former students")) + en_note + f'<ul class="people">{conc}</ul>')
            + section(head_block(T(lang, "Participe", "Join"), T(lang, "Como ser orientado(a)", "How to join the group"))
                      + f'''<div class="cols-2"><ol class="steps">{steps_html}</ol>
<div class="callout"><h3>{T(lang, "Perfil procurado", "Who we look for")}</h3><ul class="checklist">{"".join(f"<li>{x}</li>" for x in profile)}</ul>
<p>{T(lang, "Escreva para", "Write to")}:</p>{email(lang)}
{mail_btn(lang, T(lang, "Enviar e-mail sobre orientação", "Email about supervision"), T(lang, "Contato via site: interesse em orientação", "Website contact: supervision"))}
</div></div>''', id_="contato"))


def page_ensino(lang, pre):
    courses = [
        ("disciplina-mpaep.png", T(lang, "Modelos Probabilísticos Aplicados à Engenharia de Produção", "Probabilistic Models for Industrial Engineering"),
         T(lang, "Probabilidade e inferência estatística aplicadas a problemas da Engenharia de Produção: variáveis aleatórias, distribuições discretas e contínuas, Teorema Central do Limite e testes de aderência (Qui-Quadrado, Kolmogorov-Smirnov).",
           "Probability and statistical inference applied to industrial engineering problems: random variables, discrete and continuous distributions, the Central Limit Theorem and goodness-of-fit tests (chi-square, Kolmogorov-Smirnov)."),
         COLAB["mpaep"], T(lang, "Distribuições de probabilidade de ampla aplicação", "Widely used probability distributions")),
        ("disciplina-tpo.png", T(lang, "Pesquisa Operacional 3", "Operations Research 3"),
         T(lang, "Tópicos modernos de Pesquisa Operacional para produção e logística: programação linear inteira mista, otimização multiobjetivo, programação estocástica e heurísticas e meta-heurísticas, com implementação em Python e Gurobi/CPLEX.",
           "Modern operations research topics for production and logistics: mixed-integer linear programming, multi-objective optimization, stochastic programming, heuristics and metaheuristics, implemented in Python with Gurobi/CPLEX."),
         COLAB["tpo"], T(lang, "Visualizando a busca em meta-heurísticas populacionais", "Visualizing search in population-based metaheuristics")),
        ("disciplina-tia.png", T(lang, "Tópicos em Inteligência Artificial", "Topics in Artificial Intelligence"),
         T(lang, "Aprendizado de máquina supervisionado e não supervisionado: preparação de dados, classificação, regressão, agrupamento e regras de associação, com projetos em Google Colab e leitura crítica de artigos.",
           "Supervised and unsupervised machine learning: data preparation, classification, regression, clustering and association rules, with Google Colab projects and critical reading of papers."),
         COLAB["tia"], T(lang, "Redes neurais artificiais para previsão de séries temporais", "Artificial neural networks for time-series forecasting")),
    ]
    def cards(cs):
        return "".join(
        f'<div class="item"><div class="figure"><img src="{pre}figuras/{img}" alt="{E(t)}" loading="lazy"></div><h3>{t}</h3><p>{d}</p>'
        f'<p style="font-size:.8rem;color:var(--muted);margin-top:.4rem">{T(lang, "Material de apoio · Google Colab", "Support material · Google Colab")}</p>'
        f'<a class="link-out" href="{u}" target="_blank" rel="noopener">{n}</a></div>'
        for img, t, d, u, n in cs)
    grad, pos = courses[:2], courses[2:]
    return (page_head(lang, T(lang, "Ensino", "Teaching"), T(lang, "Da teoria à prática", "From theory to practice"),
                      T(lang, "Nas minhas disciplinas, os conceitos partem de problemas reais da Engenharia de Produção: planejar a produção, organizar estoques, decidir rotas, prever a demanda. Exemplos resolvidos e materiais de apoio, como notebooks prontos no Google Colab, ajudam a experimentar as ideias. É recomendado conhecimento inicial de programação.",
                        "In my courses, concepts start from real industrial engineering problems: planning production, managing inventory, choosing routes, forecasting demand. Worked examples and support materials, such as ready-to-use Google Colab notebooks, help students try out the ideas. Basic programming knowledge is recommended."))
            + section(head_block(T(lang, "Graduação", "Undergraduate"), T(lang, "Engenharia de Produção, UFSCar Sorocaba", "Industrial Engineering, UFSCar Sorocaba")) + f'<div class="cols-2 cards">{cards(grad)}</div>')
            + section(head_block(T(lang, "Pós-graduação", "Graduate"), T(lang, "Programa de Pós-Graduação em Engenharia de Produção (PPGEPS)", "Graduate Program in Industrial Engineering (PPGEPS)")) + f'<div class="cols-2 cards">{cards(pos)}</div>'))


def page_extensao(lang, pre):
    courses = [
        (T(lang, "Previsão de demanda e analytics", "Demand forecasting and analytics"),
         T(lang, "Análise quantitativa de séries temporais na indústria com Python: métodos de previsão, métricas de erro e uso das previsões no planejamento.",
           "Quantitative time-series analysis for industry with Python: forecasting methods, error metrics and using forecasts in planning.")),
        (T(lang, "IA generativa aplicada à produção", "Generative AI for operations"),
         T(lang, "Modelos de linguagem (LLMs) como assistentes no PCP: análise de dados de fábrica, diagnósticos de fluxo de valor e boas práticas de uso.",
           "Large language models as assistants in production planning: analyzing plant data, value-stream diagnostics and good practices.")),
        (T(lang, "Gestão de estoques e DDMRP", "Inventory management and DDMRP"),
         T(lang, "Dimensionamento de buffers, revisão de parâmetros de suprimento e Demand Driven MRP para proteger o fluxo de materiais da variabilidade.",
           "Buffer sizing, supply parameter review and Demand Driven MRP to protect material flow from variability.")),
        (T(lang, "Planejamento tático: S&OP", "Tactical planning: S&OP"),
         T(lang, "Estruturação do processo de Vendas e Operações para equilibrar a demanda projetada com a capacidade produtiva e melhorar o nível de serviço.",
           "Structuring the Sales and Operations Planning process to balance forecast demand with capacity and improve service levels.")),
    ]
    c_html = "".join(f'<div class="course"><span class="tag tag-orange">24 – 48 h</span><h3>{a}</h3><p>{b}</p></div>' for a, b in courses)
    fronts = [
        T(lang, "Planejamento, programação e controle da produção", "Production planning, scheduling and control"),
        T(lang, "Corte de matéria-prima e aproveitamento de chapas, bobinas e barras", "Raw-material cutting and yield of sheets, coils and bars"),
        T(lang, "Programação de operações logísticas, pátios e frotas", "Scheduling of logistics operations, yards and fleets"),
        T(lang, "Previsão de demanda e gestão de estoques", "Demand forecasting and inventory management"),
    ]
    return (page_head(lang, T(lang, "Extensão", "Outreach"), T(lang, "Universidade e setor produtivo", "University and industry"),
                      T(lang, "A extensão é uma via de mão dupla: a universidade leva conhecimento às organizações e aprende com seus problemas concretos, que voltam para a sala de aula e para a pesquisa.",
                        "Outreach goes both ways: the university brings knowledge to organizations and learns from their concrete problems, which feed back into teaching and research."))
            + section(head_block(T(lang, "Parcerias", "Partnerships"), T(lang, "Pesquisa aplicada para empresas", "Applied research for companies"))
                      + f'''<div class="cols-2"><div class="prose">
<p>{T(lang, "Problemas reais pedem mais que formulações teóricas: pedem sistemas de apoio à decisão que gerem resultado mensurável. Traduzo gargalos operacionais em modelos matemáticos e algoritmos sob medida, em projetos de P&amp;D e parcerias com a universidade.",
      "Real problems need more than theoretical formulations: they need decision-support systems with measurable results. I translate operational bottlenecks into tailored mathematical models and algorithms, through R&amp;D projects and university partnerships.")}</p>
<p>{T(lang, "Antes da carreira acadêmica, trabalhei na UniSoma, consultoria de modelagem matemática que aplica Pesquisa Operacional em empresas de vários setores. Projetos recentes partiram de demandas da siderurgia, da indústria aeronáutica e do transporte aéreo para o setor de petróleo e gás.",
      "Before my academic career I worked at UniSoma, a mathematical modeling consultancy that applies operations research for companies in many sectors. Recent projects started from needs in steelmaking, the aeronautics industry and air transport for the oil and gas sector.")}</p>
</div><div class="callout"><h3>{T(lang, "Frentes de atuação", "Areas")}</h3><ul class="checklist">{"".join(f"<li>{f}</li>" for f in fronts)}</ul>
<p>{T(lang, "Descreva a situação-problema da sua empresa:", "Describe your company's problem:")}</p>{email(lang)}
{mail_btn(lang, T(lang, "Enviar e-mail sobre parceria", "Email about a partnership"), T(lang, "Contato via site: parceria com empresa", "Website contact: industry partnership"))}</div></div>''', id_="contato")
            + section(head_block(T(lang, "Capacitação", "Training"), T(lang, "Cursos de extensão", "Short courses"),
                                 T(lang, "Propostas de cursos que podem ser oferecidos em formato híbrido ou na própria empresa (in company). Conteúdo e carga horária são ajustados à demanda.",
                                   "Course proposals that can run in a hybrid format or on site at the company. Content and length are adjusted to each request."))
                      + f'<div class="cols-2">{c_html}</div>'))


BUILDERS = {"inicio": page_inicio, "pesquisa": page_pesquisa, "publicacoes": page_publicacoes,
            "orientacao": page_orientacao, "ensino": page_ensino, "extensao": page_extensao}

DESC = {
    "inicio": ("Mateus Pereira Martin, professor de Engenharia de Produção na UFSCar Sorocaba. Pesquisa Operacional aplicada à produção e à logística.",
               "Mateus Pereira Martin, Industrial Engineering professor at UFSCar Sorocaba. Operations research for production and logistics."),
    "pesquisa": ("Linhas de pesquisa, projetos financiados e o laboratório LOGOS.", "Research topics, funded projects and the LOGOS lab."),
    "publicacoes": ("Lista completa de artigos em periódicos, com filtro por tema.", "Full list of journal articles, filterable by topic."),
    "orientacao": ("Orientações de iniciação científica e mestrado, e como participar do grupo.", "Undergraduate research and master's supervision, and how to join."),
    "ensino": ("Disciplinas e notebooks abertos no Google Colab.", "Courses and open Google Colab notebooks."),
    "extensao": ("Parcerias com empresas e cursos de extensão.", "Industry partnerships and short courses."),
}


def render(key, lang):
    pre = "" if lang == "pt" else "../"
    other = "en" if lang == "pt" else "pt"
    other_href = ("en/" if lang == "pt" else "../") + FILE[key][other]
    url_pt = BASE_URL + FILE[key]["pt"]
    url_en = BASE_URL + "en/" + FILE[key]["en"]
    title = ("Mateus Pereira Martin" if key == "inicio" else f'{LABEL[key][lang]} · Mateus Pereira Martin')
    desc = DESC[key][0 if lang == "pt" else 1]
    nav = "".join(
        f'<a href="{FILE[k][lang]}"' + (' aria-current="page"' if k == key else "") + f'>{LABEL[k][lang]}</a>'
        for k, *_ in PAGES)
    body = BUILDERS[key](lang, pre)
    return f'''<!DOCTYPE html>
<html lang="{T(lang, "pt-BR", "en")}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url_pt if lang == "pt" else url_en}">
<link rel="alternate" hreflang="pt-BR" href="{url_pt}">
<link rel="alternate" hreflang="en" href="{url_en}">
<meta property="og:type" content="website">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{BASE_URL}figuras/mateus.jpg">
<meta property="og:url" content="{url_pt if lang == "pt" else url_en}">
<meta property="og:locale" content="{T(lang, "pt_BR", "en_US")}">
<link rel="icon" href="{pre}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,600&display=swap">
<link rel="stylesheet" href="{pre}assets/site.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-FX92F528BC"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-FX92F528BC');</script>
</head>
<body>
<a class="skip" href="#conteudo">{T(lang, "Pular para o conteúdo", "Skip to content")}</a>
<header class="site-header"><div class="wrap">
<a class="brand" href="{FILE["inicio"][lang]}"><img src="{pre}figuras/logo-ufscar.png" alt="UFSCar" width="247" height="180"><span class="brand-text"><strong>Mateus P. Martin</strong><span>UFSCar · Sorocaba</span></span></a>
<button type="button" class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
<nav class="nav" id="nav" aria-label="{T(lang, "Principal", "Main")}">{nav}</nav>
<a class="lang" href="{other_href}" hreflang="{T(lang, "en", "pt-BR")}" lang="{T(lang, "en", "pt-BR")}">{T(lang, "EN", "PT")}</a>
</div></header>
<main id="conteudo">
{body}
</main>
<footer class="site-footer"><div class="wrap">
<div class="footer-top">
<div class="contact"><strong>Mateus Pereira Martin</strong>
<span class="muted" style="font-size:.9rem">{T(lang, "Departamento de Engenharia de Produção, UFSCar · Sorocaba, SP", "Department of Industrial Engineering, UFSCar · Sorocaba, SP, Brazil")}</span>
{email(lang)}</div>
<div class="inst">
<a href="https://www.ufscar.br/" target="_blank" rel="noopener"><img src="{pre}figuras/logo-ufscar.png" alt="UFSCar" width="247" height="180" loading="lazy"></a>
<a href="https://www.ccgt.ufscar.br/pt-br" target="_blank" rel="noopener"><img src="{pre}figuras/logo-ccgt.png" alt="CCGT/UFSCar" width="200" height="75" loading="lazy"></a>
<a href="https://www.ppgeps.ufscar.br/pt-br/" target="_blank" rel="noopener"><img src="{pre}figuras/logo-ppgeps.png" alt="PPGEPS/UFSCar" width="200" height="162" loading="lazy"></a>
<a href="{FILE["pesquisa"][lang]}"><img src="{pre}figuras/logos-claro.png" alt="LOGOS" width="900" height="160" loading="lazy"></a>
</div></div>
<p>{T(lang, "Site acadêmico e pessoal. As informações são de responsabilidade do autor e não representam posição oficial da Universidade Federal de São Carlos.",
       "Personal academic website. Its content is the author's responsibility and does not represent an official position of the Federal University of São Carlos.")}
{T(lang, "Atualizado em", "Last updated")} {ATUALIZADO[lang]}.</p>
</div></footer>
<script src="{pre}assets/site.js"></script>
</body>
</html>
'''


def sitemap():
    from datetime import date
    hoje = date.today().isoformat()
    urls = []
    for key, *_ in PAGES:
        pt = BASE_URL + FILE[key]["pt"]
        en = BASE_URL + "en/" + FILE[key]["en"]
        alt = (f'<xhtml:link rel="alternate" hreflang="pt-BR" href="{pt}"/>'
               f'<xhtml:link rel="alternate" hreflang="en" href="{en}"/>')
        for u in (pt, en):
            urls.append(f"  <url><loc>{u}</loc><lastmod>{hoje}</lastmod>{alt}</url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(urls) + "\n</urlset>\n")


def pagina_404():
    # Links absolutos: o GitHub Pages serve esta página em qualquer endereço inexistente.
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Página não encontrada · Mateus Pereira Martin</title>
<meta name="robots" content="noindex">
<link rel="icon" href="{BASE_URL}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,600&display=swap">
<link rel="stylesheet" href="{BASE_URL}assets/site.css">
</head>
<body>
<header class="site-header"><div class="wrap">
<a class="brand" href="{BASE_URL}"><img src="{BASE_URL}figuras/logo-ufscar.png" alt="UFSCar" width="247" height="180"><span class="brand-text"><strong>Mateus P. Martin</strong><span>UFSCar · Sorocaba</span></span></a>
</div></header>
<main><section class="section"><div class="wrap" style="display:grid;gap:1rem;max-width:40rem;margin-inline:0">
<p class="eyebrow">Erro 404</p>
<h1>Página não encontrada</h1>
<p class="lead">O endereço pode ter mudado. Comece pela página inicial ou use o menu.</p>
<p class="lead" lang="en">Page not found. The address may have changed; start from the home page.</p>
<div class="actions"><a class="btn" href="{BASE_URL}">Página inicial</a><a class="btn btn-ghost" href="{BASE_URL}en/" lang="en">Home (English)</a></div>
</div></section></main>
</body>
</html>
'''


def main():
    (ROOT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    (ROOT / "404.html").write_text(pagina_404(), encoding="utf-8")
    print("ok sitemap.xml, 404.html")
    for key, *_ in PAGES:
        for lang in ("pt", "en"):
            out = ROOT / (FILE[key][lang] if lang == "pt" else "en/" + FILE[key][lang])
            out.parent.mkdir(exist_ok=True)
            out.write_text(render(key, lang), encoding="utf-8")
            print("ok", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
