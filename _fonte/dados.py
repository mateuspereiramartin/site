# Dados do site (fonte única). Edite aqui e rode:  python3 _fonte/gerar.py
# Pastas iniciadas por "_" não são publicadas pelo GitHub Pages.

BASE_URL = "https://mateuspereiramartin.github.io/site/"
EMAIL_U, EMAIL_D = "mpmartin", "ufscar.br"
ATUALIZADO = {"pt": "outubro de 2026", "en": "October 2026"}

LINKS = [
    ("Lattes", "http://lattes.cnpq.br/9814295914139504"),
    ("ORCID", "https://orcid.org/0000-0002-6722-7571"),
    ("Google Scholar", "https://scholar.google.com.br/citations?user=QnhlnG8AAAAJ&hl"),
    ("Scopus", "https://www.scopus.com/authid/detail.uri?authorId=57204688163"),
    ("Web of Science", "https://www.webofscience.com/wos/author/record/ADG-9938-2022"),
    ("LinkedIn", "https://www.linkedin.com/in/mateus-pereira-martin/"),
]

# ano = ano do fascículo (volume/issue); se ainda não há fascículo, ano da publicação online.
# Temas: corte | prod | log | outros
# "st" = coautores que eram meus orientandos (sobrenome como aparece em "autores")
PUBS = [
    dict(n=22, ano=2026, vol="20", num="", pag="e20004", tema="corte", autores="V. F. Henriques; M. Martin", st=["Henriques"],
         titulo="Problemas de corte bi- e tridimensional guilhotinados k-estágios e restritos: uma extensão do algoritmo de Wang",
         revista="Pesquisa Operacional para o Desenvolvimento", doi="10.59254/PODes.2026.004"),
    dict(n=21, ano=2026, vol="34", num="3", pag="523–547", tema="prod", autores="M. O. Pileggi; M. Martin; R. Morabito",
         titulo="Applying project scheduling approaches to optimize aircraft maintenance activities",
         revista="TOP", doi="10.1007/s11750-026-00722-9"),
    dict(n=20, ano=2027, vol="34", num="2", pag="822–846", tema="prod", autores="B. J. V. da Silva; M. Martin; R. Morabito; V. Pureza",
         titulo="Optimization of structural assembly scheduling in the aeronautics industry",
         revista="International Transactions in Operational Research", doi="10.1111/itor.70214"),
    dict(n=19, ano=2026, vol="21", num="56", pag="", tema="outros", autores="J. G. S. P. Sales; L. A. D. Rangel; M. Martin", st=["Sales"],
         titulo="Aplicação de métodos multicritério da escola francesa na avaliação e seleção de caldeiras a vapor em fábricas de papel",
         revista="Cadernos UniFOA", doi="10.47385/cadunifoa.v21.n56.5851"),
    dict(n=18, ano=2026, vol="64", num="4", pag="1358–1385", tema="corte", autores="G. G. Guimarães; K. C. Poldi; M. Martin",
         titulo="On formulations for the one-dimensional cutting stock with a limited number of open stacks problem",
         revista="International Journal of Production Research", doi="10.1080/00207543.2025.2568739"),
    dict(n=17, ano=2026, vol="58", num="7", pag="2128–2144", tema="corte", autores="M. Martin; F. Amorim; M. Ferreira; T. A. de Queiroz; R. Morabito", st=["Amorim", "Ferreira"],
         titulo="Models for the two-dimensional open-dimension rectangular packing problem",
         revista="Engineering Optimization", doi="10.1080/0305215X.2025.2551024"),
    dict(n=16, ano=2025, vol="76", num="12", pag="2494–2506", tema="log", autores="M. Martin; A. Alvarez; J. De La Vega; R. Morabito",
         titulo="A constraint programming model and a hybrid iterated local search algorithm for solving an aircraft recovery problem in the oil and gas industry",
         revista="Journal of the Operational Research Society", doi="10.1080/01605682.2025.2478257"),
    dict(n=15, ano=2025, vol="49", num="3", pag="43", tema="corte", autores="G. G. Guimarães; K. C. Poldi; M. Martin",
         titulo="Mathematical models for the one-dimensional cutting stock problem with setups and open stacks",
         revista="Journal of Combinatorial Optimization", doi="10.1007/s10878-025-01276-5"),
    dict(n=14, ano=2024, vol="48", num="1", pag="8", tema="corte", autores="M. Martin; H. H. Yanasse; M. O. Santos; R. Morabito",
         titulo="Models for two-dimensional bin packing problems with customer order spread",
         revista="Journal of Combinatorial Optimization", doi="10.1007/s10878-024-01201-2"),
    dict(n=13, ano=2024, vol="167", num="", pag="106651", tema="corte", autores="M. Martin; T. A. de Queiroz; R. Morabito",
         titulo="Solving the three-dimensional open-dimension rectangular packing problem: a constraint programming model",
         revista="Computers & Operations Research", doi="10.1016/j.cor.2024.106651"),
    dict(n=12, ano=2024, vol="31", num="5", pag="3010–3035", tema="corte", autores="H. Becker; M. Martin; O. Araujo; L. S. Buriol; R. Morabito",
         titulo="Comparative analysis of mathematical formulations for the two-dimensional guillotine cutting problem",
         revista="International Transactions in Operational Research", doi="10.1111/itor.13358"),
    dict(n=11, ano=2024, vol="340", num="1", pag="345–365", tema="prod", autores="M. Martin; F. L. Usberti; C. Lyra",
         titulo="Improving reliability with optimal allocation of maintenance resources: an application to power distribution networks",
         revista="Annals of Operations Research", doi="10.1007/s10479-022-05039-x"),
    dict(n=10, ano=2023, vol="61", num="9", pag="2895–2916", tema="corte", autores="M. Martin; H. H. Yanasse; M. O. Santos; R. Morabito",
         titulo="Models for two- and three-stage two-dimensional cutting stock problems with a limited number of open stacks",
         revista="International Journal of Production Research", doi="10.1080/00207543.2022.2070882"),
    dict(n=9, ano=2022, vol="44", num="1", pag="557–582", tema="corte", autores="M. Martin; H. H. Yanasse; L. L. Salles-Neto",
         titulo="Pattern-based ILP models for the one-dimensional cutting stock problem with setup cost",
         revista="Journal of Combinatorial Optimization", doi="10.1007/s10878-022-00848-z"),
    dict(n=8, ano=2022, vol="29", num="5", pag="2944–2967", tema="prod", autores="M. Martin; H. H. Yanasse; M. J. Pinto",
         titulo="Mathematical models for the minimization of open stacks problem",
         revista="International Transactions in Operational Research", doi="10.1111/itor.13053"),
    dict(n=7, ano=2021, vol="72", num="12", pag="2755–2769", tema="corte", autores="M. Martin; R. Morabito; P. Munari",
         titulo="A top-down cutting approach for modeling the constrained two- and three-dimensional guillotine cutting problems",
         revista="Journal of the Operational Research Society", doi="10.1080/01605682.2020.1813640"),
    dict(n=6, ano=2022, vol="60", num="6", pag="1854–1873", tema="corte", autores="M. Martin; R. Morabito; P. Munari",
         titulo="Two-stage and one-group two-dimensional guillotine cutting problems with defects: a CP-based algorithm and ILP formulations",
         revista="International Journal of Production Research", doi="10.1080/00207543.2021.1876270"),
    dict(n=5, ano=2021, vol="168", num="", pag="114257", tema="corte", autores="M. Martin; J. F. Oliveira; E. Silva; R. Morabito; P. Munari",
         titulo="Three-dimensional guillotine cutting problems with constrained patterns: MILP formulations and a bottom-up algorithm",
         revista="Expert Systems with Applications", doi="10.1016/j.eswa.2020.114257"),
    dict(n=4, ano=2020, vol="115", num="", pag="104851", tema="corte", autores="M. Martin; R. Morabito; P. Munari",
         titulo="A bottom-up packing approach for modeling the constrained two-dimensional guillotine placement problem",
         revista="Computers & Operations Research", doi="10.1016/j.cor.2019.104851"),
    dict(n=3, ano=2020, vol="27", num="2", pag="767–793", tema="corte", autores="M. Martin; E. G. Birgin; R. D. Lobato; R. Morabito; P. Munari",
         titulo="Models for the two-dimensional rectangular single large placement problem with guillotine cuts and constrained pattern",
         revista="International Transactions in Operational Research", doi="10.1111/itor.12703"),
    dict(n=2, ano=2020, vol="58", num="9", pag="2712–2729", tema="corte", autores="M. Martin; P. H. D. B. Hokama; R. Morabito; P. Munari",
         titulo="The constrained two-dimensional guillotine cutting problem with defects: an ILP formulation, a Benders decomposition and a CP-based algorithm",
         revista="International Journal of Production Research", doi="10.1080/00207543.2019.1630773"),
    dict(n=1, ano=2018, vol="28", num="", pag="e20170105", tema="corte", autores="M. Martin; A. Moretti; M. Gomes-Ruggiero; L. Salles-Neto",
         titulo="Modification of Haessler's sequential heuristic procedure for the one-dimensional cutting stock problem with setup cost",
         revista="Production", doi="10.1590/0103-6513.20170105"),
]

TEMAS = {
    "corte": {"pt": "Corte e empacotamento", "en": "Cutting and packing"},
    "prod": {"pt": "Programação da produção e manutenção", "en": "Production and maintenance scheduling"},
    "log": {"pt": "Logística", "en": "Logistics"},
    "outros": {"pt": "Outros", "en": "Other"},
}

# Orientações. nivel: ic | mestrado. fomento: só quando confirmado.
ORIENTACOES = {
    "andamento": [
        dict(nome="Gabriel da Silva Moris", nivel="ic", fomento="FAPESP", curso="Engenharia de Produção, UFSCar",
             pt="Reprogramação de voos no transporte aéreo para unidades marítimas via programação por restrições",
             en="Flight rescheduling in air transport to offshore units via constraint programming"),
        dict(nome="Henrique Fornazari de Paiva", nivel="ic", fomento="FAPESP", curso="Engenharia de Produção, UFSCar",
             pt="Problema de corte de estoque tridimensional guilhotinado k-estágios via modelagem matemática",
             en="Three-dimensional k-staged guillotine cutting stock problem via mathematical modeling"),
        dict(nome="Gustavo Lisboa Benvenuti Magnoler", nivel="ic", fomento="FAPESP", curso="Engenharia de Produção, UFSCar",
             pt="Programação de atividades de manutenção aeronáutica com restrições de recursos",
             en="Resource-constrained scheduling of aircraft maintenance activities"),
        dict(nome="Deyvison de Carvalho Souza", nivel="mestrado", fomento=None, curso="Mestrado Profissional, PPGEP/UFF",
             pt="Programação linear inteira mista aplicada ao planejamento e controle da produção em uma central de logística reversa industrial",
             en="Mixed-integer linear programming for production planning and control in an industrial reverse logistics center"),
    ],
    "concluidas": [
        dict(nome="Fábio Alvaro de Amorim", nivel="mestrado", fomento=None, curso="Mestrado Profissional, PPGEP/UFF", ano=2026,
             pt="Planejamento de manutenção em redes de distribuição de energia elétrica via programação estocástica",
             en="Maintenance planning in power distribution networks via stochastic programming", pub=17),
        dict(nome="Matheus Augusto Almeida Ferreira", nivel="mestrado", fomento=None, curso="Mestrado Profissional, PPGEP/UFF", ano=2026,
             pt="O problema de realocação de blocos em um depósito de bobinas de aço",
             en="The block relocation problem in a steel coil warehouse", pub=17),
        dict(nome="Vitor Ferrari Henriques", nivel="ic", fomento="FAPESP", curso="Engenharia de Produção, UFSCar",
             pt="Um algoritmo combinatório para o problema de corte guilhotinado k-estágios e restrito",
             en="A combinatorial algorithm for the constrained k-staged guillotine cutting problem", pub=22),
        dict(nome="João Vítor Gutierres Figueroa", nivel="ic", fomento="FAPESP", curso="Engenharia de Produção, UFSCar", premio=2026,
             pt="Modelagem matemática para o problema de corte de estoque tridimensional guilhotinado",
             en="Mathematical modeling for the three-dimensional guillotine cutting stock problem"),
        dict(nome="Guilherme Reis Nahass", nivel="ic", fomento="FAPESP", curso="Engenharia de Produção, UFSCar",
             pt="Metaheurísticas de chaves aleatórias para o problema de realocação de blocos",
             en="Random-key metaheuristics for the block relocation problem"),
        dict(nome="João Gabriel de Souza Pinto Sales", nivel="mestrado", coorientacao=True, fomento=None,
             curso="Mestrado Profissional, PPGEP/UFF", pt=None, en=None, pub=19),
    ],
}

COLAB = {
    "mpaep": "https://drive.google.com/file/d/1h-5Y5MYMwv81FWM93g3x6eEG03k9MObl/view?usp=sharing",
    "tpo": "https://drive.google.com/file/d/1fMIifYJaDQ4jOW6JrUlp1kKAKRyo1Fkm/view?usp=sharing",
    "tia": "https://drive.google.com/file/d/1A-oyep1Do1-Lzng84SmGSnDDSdbzsqLS/view?usp=sharing",
}

PUBS.sort(key=lambda p: (p["ano"], p["n"]), reverse=True)

# Prêmios e distinções (mais recente primeiro)
PREMIOS = [
    dict(ano=2026,
         pt="Menção honrosa no Prêmio ABEPRO & Lean Way 2026 (Artigo em Sessões Temáticas), XLVI ENEGEP, pelo trabalho “Uma formulação matemática para o problema de corte de estoque tridimensional guilhotinado”, com o orientando de iniciação científica João Vítor Gutierres Figueroa",
         en="Honorable mention, ABEPRO & Lean Way Award 2026 (Thematic Sessions paper), XLVI ENEGEP, for “Uma formulação matemática para o problema de corte de estoque tridimensional guilhotinado”, with undergraduate research student João Vítor Gutierres Figueroa"),
    dict(ano=2020,
         pt="Menção honrosa no Prêmio de Teses do SBPO, Sociedade Brasileira de Pesquisa Operacional (SOBRAPO), pela tese “Problemas de corte guilhotinado e restritos: formulações matemáticas e métodos de solução”",
         en="Honorable mention, SBPO Thesis Award, Brazilian Operations Research Society (SOBRAPO), for the PhD thesis on constrained guillotine cutting problems"),
    dict(ano=2012,
         pt="Melhor Tema Livre no XX Congresso Interno de Iniciação Científica da UNICAMP",
         en="Best Free Topic award, 20th UNICAMP Undergraduate Research Congress"),
]
