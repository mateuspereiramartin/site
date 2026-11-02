#!/usr/bin/env python3
"""Gera as páginas estáticas do site (PT e EN) a partir de dados.py.

Uso:  python3 _fonte/gerar.py      (a partir da pasta paginas-html-v2)
O resultado são arquivos .html comuns; editar o HTML direto também funciona,
mas a próxima geração sobrescreve. Prefira editar dados.py / este arquivo.
"""
import html
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # não gera _fonte/__pycache__
sys.path.insert(0, str(Path(__file__).parent))
from dados import (ATUALIZADO, BASE_URL, COLAB, ELI_EMAIL_D, ELI_EMAIL_U, EMAIL_D, EMAIL_U, LINKS,  # noqa: E402
                   ORIENTACOES, PREMIOS, PUBS, TEMAS)

ROOT = Path(__file__).resolve().parent.parent
E = html.escape

PAGES = [  # chave, arquivo pt, arquivo en, rótulo pt, rótulo en
    ("inicio", "index.html", "index.html", "Início", "Home"),
    ("ensino", "ensino.html", "teaching.html", "Ensino", "Teaching"),
    ("orientacao", "orientacao.html", "advising.html", "Orientação", "Advising"),
    ("publicacoes", "publicacoes.html", "publications.html", "Publicações", "Publications"),
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

def email(lang, subject=None, show=True, u=EMAIL_U, d=EMAIL_D):
    subj = f' data-subject="{E(subject)}"' if subject else ""
    copy = T(lang, "Copiar", "Copy")
    done = T(lang, "Copiado", "Copied")
    return (f'<span class="email-row"><a class="email" data-email data-show data-u="{u}" data-d="{d}"{subj}>'
            f'{u} [{T(lang, "arroba", "at")}] {d}</a>'
            f'<button type="button" class="copy" data-u="{u}" data-d="{d}" data-done="{done}">{copy}</button></span>')


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
    return (f'<header class="page-head"><div class="wrap" style="display:grid;gap:0.6rem">'
            f'<p class="eyebrow">{eyebrow}</p><h1>{title}</h1><p class="lead">{lead}</p></div></header>')


ELI_LINKS = [
    ("Lattes", "https://lattes.cnpq.br/6663631731115739"),
    ("ORCID", "https://orcid.org/0000-0001-7531-0300"),
    ("Scopus", "https://www.scopus.com/authid/detail.uri?authorId=26026490900"),
    ("ResearchGate", "https://www.researchgate.net/profile/Eli_Angela_Toso"),
]


def logos_band(lang, pre, lazy=True):
    return f'''<section class="logos-band" aria-labelledby="logos-t"><div class="wrap">
<img src="{pre}figuras/logos-horizontal.png" alt="LOGOS: Laboratório de Otimização em Gestão de Operações Sustentáveis" width="1600" height="579"{' loading="lazy"' if lazy else ""}>
<div class="text"><p class="eyebrow">{T(lang, "Laboratório", "Lab")}</p>
<h2 id="logos-t">LOGOS</h2>
<p>{T(lang,
 "Formado por mim e pela Profa. Dra. Eli Angela Vitor Toso, ambos docentes do DEP-So/UFSCar Sorocaba e do PPGEPS, o Laboratório de Otimização em Gestão de Operações Sustentáveis reúne nossos orientandos de graduação e pós-graduação e desenvolve modelos matemáticos e algoritmos para problemas práticos de produção e logística.",
 "Formed by Prof. Eli Angela Vitor Toso and me, both faculty members of the Department of Industrial Engineering (DEP-So) at UFSCar Sorocaba and of PPGEPS, the Laboratory of Optimization in Sustainable Operations Management (LOGOS) brings together our undergraduate and graduate students and develops mathematical models and algorithms for practical production and logistics problems.")}</p>
<div style="display:grid;gap:.4rem"><p style="font-size:.88rem">{T(lang, "Profa. Eli Toso", "Prof. Eli Toso")}: {" · ".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in ELI_LINKS)}</p>
{email(lang, u=ELI_EMAIL_U, d=ELI_EMAIL_D)}</div>
<p><a href="{href(lang, "orientacao")}#contato">{T(lang, "Saiba como participar do grupo", "Learn how to join the group")}</a></p>
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
<h1>Mateus Pereira Martin<span>{T(lang, "Professor do Departamento de Engenharia de Produção da UFSCar, campus Sorocaba", "Assistant Professor of Industrial Engineering at the Federal University of São Carlos (UFSCar), Sorocaba campus")}</span></h1>
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
<div><dt>{T(lang, "participações em projetos financiados (CNPq, FAPESP)", "funded projects as team member (CNPq, FAPESP)")}</dt><dd>3</dd></div>
</dl></div>'''

    tl_items = [
        ("2024 –", T(lang, "Professor, Departamento de Engenharia de Produção (DEP-So), UFSCar Sorocaba", "Assistant Professor, Department of Industrial Engineering (DEP-So), UFSCar Sorocaba"),
         T(lang, "Docente credenciado no Programa de Pós-Graduação em Engenharia de Produção (PPGEPS), com orientação na pós-graduação", "Faculty member of the Graduate Program in Industrial Engineering (PPGEPS), supervising graduate students")),
        ("2021 – 2024", T(lang, "Professor, Universidade Federal Fluminense (UFF), Petrópolis", "Assistant Professor, Fluminense Federal University (UFF), Petrópolis"),
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
        (T(lang, "Pesquisa Operacional Aplicada", "Applied Operations Research"),
         T(lang, "Desenvolvimento e aplicação de abordagens baseadas em programação linear inteira mista e programação por restrições para resolver problemas complexos em sistemas produtivos e logísticos. A modelagem matemática para otimização de recursos é o centro do trabalho, com aplicações que vão de problemas de corte e empacotamento à programação de operações industriais, à gestão de pátios (realocação de blocos) e à logística de transportes (alocação de berços e recuperação de malhas aéreas).",
           "Development and application of approaches based on mixed-integer linear programming and constraint programming to solve complex problems in production and logistics systems. Mathematical modeling for resource optimization is at the core of the work, with applications ranging from cutting and packing problems to the scheduling of industrial operations, yard management (block relocation) and transport logistics (berth allocation and airline schedule recovery).")),
        (T(lang, "Integração entre Pesquisa Operacional e Aprendizado de Máquina", "Integrating Operations Research and Machine Learning"),
         T(lang, "Nova linha, em estruturação: abordagens híbridas que integram técnicas de aprendizado de máquina (AM) a métodos de Pesquisa Operacional (PO), incluindo algoritmos heurísticos e meta-heurísticos. O objetivo é apoiar a tomada de decisão em cenários produtivos e logísticos, unindo a capacidade preditiva do AM ao rigor prescritivo da PO.",
           "A new direction, currently taking shape: hybrid approaches that integrate machine learning (ML) techniques with Operations Research (OR) methods, including heuristic and metaheuristic algorithms. The goal is to support decision-making in production and logistics settings, combining the predictive power of ML with the prescriptive rigor of OR.")),
    ]
    areas_html = "".join(f'<div class="item"><h3>{a}</h3><p>{b}</p></div>' for a, b in areas)

    return (hero + facts
            + section(head_block(T(lang, "Atuação", "Focus"), T(lang, "Linhas de pesquisa", "Research lines")) + f'<div class="cols-2">{areas_html}</div>')
            + section(head_block(T(lang, "Trajetória", "Background"), T(lang, "Formação e carreira", "Education and career")) + f'<ol class="timeline" reversed>{tl}</ol>')
            + section(head_block(T(lang, "Distinções", "Awards"), T(lang, "Prêmios e distinções", "Awards and honors"))
                      + '<ol class="timeline">' + "".join(f'<li><span class="when">{p["ano"]}</span><div><span style="color:var(--ink)">{E(p[lang])}</span></div></li>' for p in PREMIOS) + '</ol>')
            + logos_band(lang, pre))


def page_pesquisa(lang, pre):
    lines = [
        ("problema-corte.png", T(lang, "Corte e empacotamento", "Cutting and packing"),
         T(lang, "Como dividir chapas, bobinas e blocos de matéria-prima em peças menores com o mínimo de desperdício, ou como acomodar itens em placas, caixas e contêineres. São problemas do dia a dia de indústrias de aço, vidro, madeira, papel e móveis, e o meu principal tema desde o doutorado.",
           "How to cut sheets, rolls and blocks of raw material into smaller pieces with minimal waste, or how to fit items into plates, boxes and containers. These problems are part of daily operations in the steel, glass, wood, paper and furniture industries, and they have been my main topic since my PhD."),
         [T(lang, "Formulações de programação linear inteira mista para cortes guilhotinados em duas e três dimensões, com padrões restritos e número limitado de estágios",
            "Mixed-integer linear programming formulations for two- and three-dimensional guillotine cutting, with constrained patterns and a limited number of stages"),
          T(lang, "Variantes industriais: placas com defeitos, custo de setup, limite de pilhas abertas e dispersão de pedidos",
            "Industrial variants: plates with defects, setup costs, a limit on open stacks and order spread"),
          T(lang, "Programação por restrições, decomposição de Benders e algoritmos dedicados (abordagens top-down e bottom-up)",
            "Constraint programming, Benders decomposition and dedicated algorithms (top-down and bottom-up approaches)")],
         ["CSP", "2D-ODRPP", "3D-ODRPP", "2BPP-OS"]),
        ("problema-scheduling.png", T(lang, "Programação da produção e manutenção", "Production and maintenance scheduling"),
         T(lang, "Em que ordem e com quais recursos executar as operações de uma fábrica ou de uma equipe de manutenção, respeitando precedências, prazos e capacidades limitadas. Pequenas mudanças na sequência podem reduzir bastante o tempo total e o custo.",
           "In what order and with which resources to carry out the operations of a plant or a maintenance crew, respecting precedences, deadlines and limited capacities. Small changes in the sequence can greatly reduce total time and cost."),
         [T(lang, "Minimização de pilhas abertas e sua integração com o problema de corte",
            "Minimization of open stacks and its integration with cutting problems"),
          T(lang, "Montagem estrutural e manutenção de aeronaves, modeladas como programação de projetos com recursos limitados",
            "Aircraft structural assembly and maintenance, modeled as resource-constrained project scheduling"),
          T(lang, "Alocação de recursos de manutenção para aumentar a confiabilidade de redes de distribuição de energia",
            "Allocation of maintenance resources to improve the reliability of power distribution networks")],
         ["MOSP", "ASASP", "RCPSP"]),
        ("problema-logistica.png", T(lang, "Logística", "Logistics"),
         T(lang, "Planejamento da movimentação de cargas, veículos e aeronaves em sistemas com muitas restrições operacionais, em que cada decisão afeta as seguintes e imprevistos exigem replanejamento rápido.",
           "Planning the movement of cargo, vehicles and aircraft in systems with many operational constraints, where each decision affects the next and disruptions call for fast replanning."),
         [T(lang, "Realocação de blocos e contêineres em pátios e depósitos, com meta-heurísticas de chaves aleatórias (decoders no framework RKO)",
            "Block and container relocation in yards and warehouses, with random-key metaheuristics (decoders in the RKO framework)"),
          T(lang, "Recuperação da programação de voos para unidades marítimas de petróleo e gás, com programação por restrições e busca local iterada",
            "Flight schedule recovery for offshore oil and gas units, with constraint programming and iterated local search"),
          T(lang, "Participação em projetos sobre problemas integrados de localização, roteamento e programação de operações logísticas",
            "Participation in projects on integrated location, routing and scheduling problems in logistics")],
         ["BRP", "ARP"]),
    ]
    acr_note = T(lang, "Siglas dos problemas na literatura", "Problem acronyms used in the literature")
    lines_html = "".join(
        f'<div class="item"><div class="figure"><img src="{pre}figuras/{img}" alt="{E(t)}" loading="lazy"></div><h3>{t}</h3><p>{d}</p>'
        f'<ul class="checklist checklist-sm">' + "".join(f"<li>{x}</li>" for x in focus) + "</ul>"
        f'<div class="tags" aria-label="{acr_note}">' + "".join(f'<span class="tag tag-green">{a}</span>' for a in acr) + "</div></div>"
        for img, t, d, focus, acr in lines)

    ml_topics = [
        T(lang, "Modelagem de problemas de produção e logística como processos de decisão markovianos",
          "Modeling production and logistics problems as Markov decision processes"),
        T(lang, "Aprendizado por Reforço para decisões sequenciais, como despacho, sequenciamento, controle de estoques e roteamento dinâmico",
          "Reinforcement Learning for sequential decisions such as dispatching, sequencing, inventory control and dynamic routing"),
        T(lang, "Métodos híbridos, em que modelos de otimização e políticas aprendidas se complementam",
          "Hybrid methods in which optimization models and learned policies complement each other"),
        T(lang, "Aprendizado de máquina para acelerar algoritmos de otimização, por exemplo na escolha de heurísticas",
          "Machine learning to speed up optimization algorithms, for example in choosing heuristics"),
    ]
    ml_html = (f'<div class="cols-2"><div class="prose">'
        f'<p>{T(lang, "Muitas decisões em produção e logística são sequenciais e tomadas sob incerteza: a demanda muda, máquinas param, pedidos chegam ao longo do dia. Os modelos clássicos de otimização resolvem muito bem um cenário fixo, mas é mais difícil usá-los quando é preciso decidir de novo a cada evento.", "Many decisions in production and logistics are sequential and made under uncertainty: demand changes, machines break down, orders arrive throughout the day. Classic optimization models handle a fixed scenario very well, but they are harder to use when a new decision is needed at every event.")}</p>'
        f'<p>{T(lang, "Por isso estou abrindo esta nova frente de trabalho, com foco em aprendizado por reforço e processos de decisão markovianos. A ideia é combinar o que cada área faz melhor: o aprendizado de máquina para aprender políticas de decisão a partir de dados e simulação, e a Pesquisa Operacional para dar estrutura ao problema e garantir soluções viáveis e de qualidade mensurável.", "That is why I am opening this new line of work, focused on reinforcement learning and Markov decision processes. The idea is to combine what each field does best: machine learning to learn decision policies from data and simulation, and Operations Research to give the problem structure and ensure feasible solutions of measurable quality.")}</p>'
        f'<p>{T(lang, "O tema dialoga com a disciplina Tópicos em Inteligência Artificial, do PPGEPS.", "The topic connects with the graduate course Topics in Artificial Intelligence (PPGEPS).")}</p></div>'
        f'<div class="callout"><h3>{T(lang, "Temas de interesse", "Topics of interest")}</h3>'
        f'<ul class="checklist">' + "".join(f"<li>{x}</li>" for x in ml_topics) + "</ul>"
        f'<p>{T(lang, "Estudantes interessados são bem-vindos, mesmo sem experiência prévia em aprendizado por reforço.", "Interested students are welcome, even without prior experience in reinforcement learning.")}</p>'
        f'<a href="{href(lang, "orientacao")}#contato" style="justify-self:start;font-weight:600">{T(lang, "Como entrar para nosso grupo de pesquisa", "How to join the group")}</a></div></div>')

    projects = [
        ("CNPq · Universal 10/2023", T(lang, "Métodos inteligentes de otimização para problemas de escalonamento e roteamento", "Intelligent optimization methods for scheduling and routing problems"),
         T(lang, "Escalonamento e roteamento de veículos com restrições reais (prioridades, janelas de tempo, incerteza), com métodos exatos e meta-heurísticas para logística e assistência médico-hospitalar. Coordenação: Thiago Alves de Queiroz.",
           "Scheduling and vehicle routing with real constraints (priorities, time windows, uncertainty), using exact methods and metaheuristics for logistics and healthcare. Coordinator: Thiago Alves de Queiroz.")),
        ("FAPESP · Temático 2022/05803-3", T(lang, "Problemas de corte, empacotamento, dimensionamento de lotes, programação da produção, roteamento e localização e suas integrações em contextos industriais e logísticos",
                                            "Cutting, packing, lot-sizing, scheduling, routing and location problems and their integration in industrial and logistics settings"),
         T(lang, "Modelos e algoritmos para problemas integrados de planejamento, em cooperação entre a academia e o setor produtivo. Coordenação: Reinaldo Morabito Neto.",
           "Models and algorithms for integrated planning problems, in cooperation between academia and industry. Coordinator: Reinaldo Morabito Neto.")),
        ("CNPq · Universal", T(lang, "Soluções integradas para problemas logísticos complexos via otimização", "Integrated solutions for complex logistics problems via optimization"),
         T(lang, "Modelos matemáticos e algoritmos para problemas integrados de localização, roteamento e programação de operações logísticas. Coordenação: Reinaldo Morabito Neto.",
           "Mathematical models and algorithms for integrated location, routing and logistics scheduling problems. Coordinator: Reinaldo Morabito Neto.")),
    ]
    proj_html = "".join(
        f'<li class="person"><div class="who"><span class="tag tag-orange">{a}</span><span class="muted" style="font-size:.9rem">{T(lang, "Pesquisador integrante", "Team member")}</span></div>'
        f'<div class="what"><h3>{t}</h3><p>{d}</p></div></li>' for a, t, d in projects)

    return (page_head(lang, T(lang, "Pesquisa", "Research"), T(lang, "Otimização para a produção e a logística", "Optimization for production and logistics"),
                      T(lang, "A Pesquisa Operacional usa matemática para encontrar a melhor decisão entre milhões de alternativas: a rota de uma frota, a ordem de produção de uma fábrica, o corte de uma chapa. Meu trabalho propõe formulações exatas e algoritmos para problemas clássicos da área e para as variantes que aparecem na indústria.",
                        "Operations Research uses mathematics to find the best decision among millions of alternatives: a fleet's routes, a plant's production sequence, how to cut a sheet. My work proposes exact formulations and algorithms for classic problems in the field and for the variants that arise in industry."))
            + logos_band(lang, pre, lazy=False)
            + section(head_block(T(lang, "Linha de pesquisa", "Research line"), T(lang, "Pesquisa Operacional Aplicada", "Applied Operations Research"),
                                 T(lang, "Aplico Pesquisa Operacional a problemas de Gestão de Sistemas Produtivos. Em todas as frentes, o trabalho combina modelagem matemática, algoritmos exatos e heurísticos e testes com instâncias da literatura e de casos reais.",
                                   "I apply Operations Research to problems in Production Systems Management. Across all fronts, the work combines mathematical modeling, exact and heuristic algorithms, and tests on benchmark instances and real cases.")) + f'<div class="cols">{lines_html}</div>')
            + section(head_block(T(lang, "Nova linha de pesquisa", "New research line"), T(lang, "Integração entre Pesquisa Operacional e Aprendizado de Máquina", "Integrating Operations Research and Machine Learning")) + ml_html)
            + section(head_block(T(lang, "Financiamento", "Funding"), T(lang, "Projetos em andamento", "Ongoing projects")) + f'<ul class="people">{proj_html}</ul>'))


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
    return (page_head(lang, T(lang, "Publicações", "Publications"), T(lang, "Artigos em periódicos", "Journal articles"),
                      T(lang, f"Os {len(PUBS)} artigos publicados desde {min(p['ano'] for p in PUBS)}, do mais recente ao mais antigo. O ano indicado é o do fascículo, que pode ser posterior à publicação online. Filtre por tema ou busque por palavra.",
                        f"All {len(PUBS)} articles published since {min(p['ano'] for p in PUBS)}, newest first. The year shown is the issue year, which may be later than online publication. Filter by topic or search by keyword."))
            + section(body))


def person(o, lang):
    nivel = {"ic": T(lang, "Iniciação científica", "Undergraduate research"), "mestrado": T(lang, "Mestrado", "Master's"), "doutorado": T(lang, "Doutorado", "PhD")}[o["nivel"]]
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
        extra = (f'<p>{T(lang, "Coautora do artigo" if o.get("f") else "Coautor do artigo", "Co-author of")} <a href="https://doi.org/{p["doi"]}" target="_blank" rel="noopener">'
                 f'“{E(p["titulo"])}”</a> (<i>{E(p["revista"])}</i>, {p["ano"]}).</p>')
    title = o.get(lang)
    if o.get("premio"):
        extra += (f'<p><span class="tag tag-orange">{T(lang, "Menção honrosa", "Honorable mention")}</span> '
                  + T(lang, "no Prêmio ABEPRO &amp; Lean Way 2026, XLVI ENEGEP.", "ABEPRO &amp; Lean Way Award 2026, XLVI ENEGEP.") + "</p>")
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
         T(lang, f'Veja as <a href="{href(lang, "pesquisa")}">linhas de pesquisa</a> e as <a href="{href(lang, "publicacoes")}">publicações recentes</a>. Não é preciso ter um tema fechado; uma área de interesse basta para começar a conversa.',
           f'Look at the <a href="{href(lang, "pesquisa")}">research topics</a> and <a href="{href(lang, "publicacoes")}">recent publications</a>. You do not need a finished idea; an area of interest is enough to start.')),
        (T(lang, "Envie um e-mail", "Send an email"),
         T(lang, "Conte em poucas linhas seu curso, seu interesse e sua disponibilidade. Anexe o histórico escolar e o link do Currículo Lattes.",
           "Briefly describe your program, your interests and your availability. Attach your transcript and a CV.")),
        (T(lang, "Conversa e treinamento", "Meeting and onboarding"),
         T(lang, "Marcamos uma conversa. Em seguida vem um período de estudo com leituras e implementação em C/C++ ou Python e solvers de otimização, como Gurobi e HiGHS.",
           "We schedule a meeting, followed by a study period with readings and implementation in C/C++ or Python and optimization solvers such as Gurobi and HiGHS.")),
        (T(lang, "Projeto e bolsa", "Proposal and funding"),
         T(lang, "Havendo afinidade, elaboramos juntos um projeto e avaliamos a possibilidade de pedir bolsa (por exemplo, CNPq ou FAPESP). Na pós-graduação, o ingresso é pelo processo seletivo do PPGEPS.",
           "If there is a good fit, we write a project together and consider applying for a scholarship (e.g., CNPq or FAPESP). For graduate studies, admission is through the PPGEPS selection process.")),
    ]
    steps_html = "".join(f'<li><div><h3>{a}</h3><p>{b}</p></div></li>' for a, b in steps)
    profile = [
        T(lang, "Estudantes de Engenharia de Produção, Computação, Matemática ou áreas afins", "Students in industrial engineering, computer science, mathematics or related areas"),
        T(lang, "Gosto por resolução de problemas, modelagem matemática e programação, de preferência em C/C++ ou Python", "Enjoy problem solving, mathematical modeling and programming, preferably in C/C++ or Python"),
        T(lang, "Disponibilidade semanal regular para o projeto", "Regular weekly time for the project"),
    ]
    return (page_head(lang, T(lang, "Orientação", "Advising"), T(lang, "Orientandos e oportunidades", "Students and opportunities"),
                      T(lang, "Oriento projetos de iniciação científica e trabalhos de graduação no bacharelado em Engenharia de Produção da UFSCar Sorocaba, além de trabalhos de pós-graduação no PPGEPS. Os projetos partem de problemas reais e costumam resultar em artigos com os estudantes como coautores.",
                        "I supervise undergraduate research projects and final-year theses in the Industrial Engineering program at UFSCar Sorocaba, as well as graduate research in PPGEPS. Projects start from real problems and often lead to articles co-authored by the students."))
            + section(head_block(T(lang, "Em andamento", "Ongoing"), T(lang, "Orientações em andamento", "Current students")) + en_note + f'<ul class="people">{and_}</ul>')
            + section(head_block(T(lang, "Concluídas", "Completed"), T(lang, "Orientações concluídas", "Former students")) + en_note + f'<ul class="people">{conc}</ul>')
            + section(head_block(T(lang, "Participe", "Join"), T(lang, "Como entrar para nosso grupo de pesquisa", "How to join the group"))
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
         T(lang, "Tópicos modernos de Pesquisa Operacional para produção e logística: programação linear inteira mista, otimização multiobjetivo, programação estocástica e heurísticas e meta-heurísticas, com implementação em Python e nos solvers Gurobi e HiGHS.",
           "Modern operations research topics for production and logistics: mixed-integer linear programming, multi-objective optimization, stochastic programming, heuristics and metaheuristics, implemented in Python with the Gurobi and HiGHS solvers."),
         COLAB["tpo"], T(lang, "Visualizando a busca em meta-heurísticas populacionais", "Visualizing search in population-based metaheuristics")),
        ("disciplina-tia.png", T(lang, "Tópicos em Inteligência Artificial", "Topics in Artificial Intelligence"),
         T(lang, "Aprendizado de máquina aplicado à Engenharia de Produção: análise exploratória de dados, aprendizado não supervisionado (agrupamento e redução de dimensionalidade), supervisionado (classificação e regressão) e por reforço, com processos de decisão markovianos e sua interface com a Pesquisa Operacional.",
           "Machine learning applied to industrial engineering: exploratory data analysis, unsupervised learning (clustering and dimensionality reduction), supervised learning (classification and regression) and reinforcement learning, with Markov decision processes and their connection to operations research."),
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
                      T(lang, "Nas minhas disciplinas, os conceitos partem de problemas reais da Engenharia de Produção: planejar a produção, organizar estoques, decidir rotas, prever a demanda. Exemplos resolvidos e materiais de apoio, como notebooks prontos no Google Colab, ajudam a experimentar as ideias. Noções de programação ajudam a aproveitar melhor esses materiais.",
                        "In my courses, concepts start from real industrial engineering problems: planning production, managing inventory, choosing routes, forecasting demand. Worked examples and support materials, such as ready-to-use Google Colab notebooks, help students try out the ideas. Some programming experience helps to get the most out of these materials."))
            + section(head_block(T(lang, "Graduação", "Undergraduate"), T(lang, "Engenharia de Produção, UFSCar Sorocaba", "Industrial Engineering, UFSCar Sorocaba")) + f'<div class="cols-2 cards">{cards(grad)}</div>')
            + section(head_block(T(lang, "Pós-graduação", "Graduate"), T(lang, "Programa de Pós-Graduação em Engenharia de Produção (PPGEPS)", "Graduate Program in Industrial Engineering (PPGEPS)")) + f'<div class="cols-2 cards">{cards(pos)}</div>'))


def page_extensao(lang, pre):
    courses = [
        (T(lang, "Previsão de demanda com aprendizado de máquina", "Demand forecasting with machine learning"),
         T(lang, "Previsão de séries temporais com Python para a indústria, dos métodos estatísticos ao aprendizado de máquina (gradient boosting e redes neurais): métricas de erro e uso das previsões no planejamento.",
           "Time-series forecasting with Python for industry, from statistical methods to machine learning (gradient boosting and neural networks): error metrics and using forecasts in planning.")),
        (T(lang, "IA generativa aplicada ao PCP", "Generative AI for production planning and control"),
         T(lang, "Uso de modelos de linguagem (LLMs) como assistentes no planejamento e controle da produção (PCP): análise de dados de fábrica, elaboração de relatórios, diagnóstico do fluxo de valor, boas práticas e limitações.",
           "Using large language models (LLMs) as assistants in production planning and control: analyzing plant data, preparing reports, value-stream diagnostics, good practices and limitations.")),
        (T(lang, "Da previsão à decisão: IA e otimização no PCP", "From forecast to decision: AI and optimization in production planning"),
         T(lang, "Como previsões e dados de fábrica alimentam modelos de planejamento e programação da produção: noções de otimização com solvers (HiGHS e Gurobi) e de políticas de decisão aprendidas a partir de dados.",
           "How forecasts and plant data feed production planning and scheduling models: an introduction to optimization with solvers (HiGHS and Gurobi) and to decision policies learned from data.")),
        (T(lang, "Gestão de estoques orientada por dados", "Data-driven inventory management"),
         T(lang, "Classificação de itens por agrupamento, políticas de estoque, simulação e dimensionamento de estoques de segurança, com conceitos do DDMRP para proteger o fluxo de materiais da variabilidade.",
           "Item classification by clustering, inventory policies, simulation and safety-stock sizing, with DDMRP concepts to protect material flow from variability.")),
    ]
    c_html = "".join(f'<div class="course"><span class="tag tag-orange">24 – 48 h</span><h3>{a}</h3><p>{b}</p></div>' for a, b in courses)
    fronts = [
        T(lang, "Planejamento, programação e controle da produção", "Production planning, scheduling and control"),
        T(lang, "Corte de matéria-prima e aproveitamento de chapas, bobinas e barras", "Raw-material cutting and yield of sheets, coils and bars"),
        T(lang, "Programação de operações logísticas, pátios e frotas", "Scheduling of logistics operations, yards and fleets"),
        T(lang, "Previsão de demanda e gestão de estoques", "Demand forecasting and inventory management"),
    ]
    return (page_head(lang, T(lang, "Extensão", "Outreach"), T(lang, "Universidade e sociedade", "University and society"),
                      T(lang, "A extensão é uma via de mão dupla: a universidade compartilha métodos e conhecimento com empresas e instituições, e aprende com os desafios concretos que elas enfrentam. Essa troca melhora decisões na prática e mantém o ensino e a pesquisa conectados aos problemas reais da sociedade.",
                        "Outreach goes both ways: the university shares methods and knowledge with companies and institutions, and learns from the concrete challenges they face. This exchange improves decisions in practice and keeps teaching and research connected to society's real problems."))
            + section(head_block(T(lang, "Parcerias", "Partnerships"), T(lang, "Pesquisa aplicada em parceria", "Applied research in partnership"))
                      + f'''<div class="cols-2"><div class="prose">
<p>{T(lang, "Muitos desafios das organizações não se resolvem com fórmulas prontas: pedem sistemas de apoio à decisão feitos sob medida e com resultado mensurável. Em projetos de P&amp;D com empresas, buscamos transformar gargalos operacionais em modelos matemáticos e algoritmos, e as perguntas que surgem nesse processo podem virar temas de pesquisa e casos para a sala de aula.",
      "Many organizational challenges cannot be solved with off-the-shelf formulas: they call for tailored decision-support systems with measurable results. In R&amp;D projects with companies, we seek to turn operational bottlenecks into mathematical models and algorithms, and the questions that arise along the way can become research topics and classroom cases.")}</p>
<p>{T(lang, "Meus trabalhos mais recentes, feitos em colaboração com outros pesquisadores e com orientandos, tratam de problemas inspirados em casos reais da siderurgia, da indústria aeronáutica e do transporte aéreo a serviço do setor de petróleo e gás.",
      "My most recent work, carried out with other researchers and with my students, addresses problems inspired by real cases in steelmaking, the aeronautics industry and air transport serving the oil and gas sector.")}</p>
</div><div class="callout"><h3>{T(lang, "Frentes de atuação", "Areas")}</h3><ul class="checklist">{"".join(f"<li>{f}</li>" for f in fronts)}</ul>
<p>{T(lang, "Conte qual é o desafio da sua organização:", "Tell me about your organization's challenge:")}</p>{email(lang)}
{mail_btn(lang, T(lang, "Enviar e-mail sobre parceria", "Email about a partnership"), T(lang, "Contato via site: parceria com empresa", "Website contact: industry partnership"))}</div></div>''', id_="contato")
            + section(head_block(T(lang, "Capacitação", "Training"), T(lang, "Cursos de extensão", "Short courses"),
                                 T(lang, "Propostas de cursos que podem ser oferecidos em formato híbrido ou na própria empresa (in company). Conteúdo e carga horária são ajustados à demanda, e a oferta depende de aprovação do departamento e da universidade.",
                                   "Course proposals that can run in a hybrid format or on site at the company. Content and length are adjusted to each request, and offering a course requires approval from the department and the university."))
                      + f'<div class="cols-2">{c_html}</div>'))


BUILDERS = {"inicio": page_inicio, "pesquisa": page_pesquisa, "publicacoes": page_publicacoes,
            "orientacao": page_orientacao, "ensino": page_ensino, "extensao": page_extensao}

DESC = {
    "inicio": ("Mateus Pereira Martin, professor de Engenharia de Produção na UFSCar Sorocaba. Pesquisa Operacional aplicada à produção e à logística.",
               "Mateus Pereira Martin, Industrial Engineering professor at UFSCar Sorocaba. Operations research for production and logistics."),
    "pesquisa": ("Linhas de pesquisa, projetos financiados e o laboratório LOGOS.", "Research topics, funded projects and the LOGOS lab."),
    "publicacoes": ("Lista completa de artigos em periódicos, com filtro por tema.", "Full list of journal articles, filterable by topic."),
    "orientacao": ("Orientações de iniciação científica e de pós-graduação, e como participar do grupo.", "Undergraduate research and graduate supervision, and how to join."),
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
<div class="brand"><a href="{FILE["pesquisa"][lang]}#logos-t" title="{T(lang, "LOGOS: Laboratório de Otimização em Gestão de Operações Sustentáveis", "LOGOS lab")}"><img src="{pre}figuras/logos-simbolo-192.png" alt="LOGOS" width="192" height="192"></a><a class="brand-text" href="{FILE["inicio"][lang]}"><strong>Mateus P. Martin</strong><span>UFSCar · Sorocaba</span></a></div>
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
<a href="{FILE["pesquisa"][lang]}"><img src="{pre}figuras/logos-simbolo-claro.png" alt="LOGOS" title="LOGOS" width="1600" height="1600" loading="lazy"></a>
</div></div>
<p class="footer-note">{T(lang, "Site acadêmico e pessoal. As informações são de responsabilidade do autor e não representam posição oficial da Universidade Federal de São Carlos.",
       "Personal academic website. Its content is the author's responsibility and does not represent an official position of the Federal University of São Carlos.")}
<br>{T(lang, 'Este site usa o Google Analytics para gerar estatísticas de acesso (<a href="https://policies.google.com/technologies/partner-sites?hl=pt-BR" target="_blank" rel="noopener">como o Google usa esses dados</a>).',
       'This site uses Google Analytics for visit statistics (<a href="https://policies.google.com/technologies/partner-sites?hl=en" target="_blank" rel="noopener">how Google uses this data</a>).')}
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
<div class="brand"><a href="{BASE_URL}pesquisa.html#logos-t" title="LOGOS"><img src="{BASE_URL}figuras/logos-simbolo-192.png" alt="LOGOS" width="192" height="192"></a><a class="brand-text" href="{BASE_URL}"><strong>Mateus P. Martin</strong><span>UFSCar · Sorocaba</span></a></div>
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
