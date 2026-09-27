import json
import pathlib
import re
import html
import hashlib
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent

cards = [
  {
    "id": "dupont-pfoa",
    "title": "DuPont: science followed contamination",
    "question": "How did company knowledge travel?",
    "body": """**Documented fact.** DuPont used PFOA near Parkersburg. Production began during 1951. The chemical aided fluoropolymer production. Internal studies recorded liver effects. Later documents tracked worker exposures. Community water also became contaminated. Those findings were not public. Litigation released many records. A 2004 settlement followed. It funded blood testing. Nearly 70,000 people participated. Independent scientists formed a panel. Their work linked exposures. Several diseases received probable links. These included kidney cancer. Testicular cancer also qualified. Ulcerative colitis also qualified. Thyroid disease also qualified. Pregnancy hypertension also qualified. High cholesterol also qualified. The project produced epidemiology. It also informed regulation. **Scholarly interpretation.** Corporate control delayed scrutiny. Litigation changed research incentives. Money then funded independent work. That mechanism matters historically. Harmful products create evidence gaps. Courts can reopen them. **Counterevidence and limits.** Early toxicology lacked certainty. Animal effects prove limited things. Community studies remain observational. A probable link differs. It does not prove causation. Exposure estimates also varied. DuPont disputed many conclusions. The record supports delayed disclosure. It cannot quantify motives. Nor does every illness qualify.""",
    "summary": "PFOA records stayed internal. Litigation funded outside science.",
    "sources": [
      ["The Devil They Knew", "https://pmc.ncbi.nlm.nih.gov/articles/PMC10237242/"],
      ["The C8 Health Project", "https://pmc.ncbi.nlm.nih.gov/articles/PMC2799461/"],
      ["Evidence of Air Dispersion", "https://pmc.ncbi.nlm.nih.gov/articles/PMC8015386/"]
    ],
    "beats": ["Factory releases enter water.", "Reports record liver effects.", "Findings remain company-held.", "Litigation funds outside science.", "Health links gain definition."],
    "setting": "River town and factory",
    "objects": [
      {"kind":"factory","label":"DuPont plant","track":[[70,205],[70,205],[70,205],[70,205],[70,205],[70,205]],"from":0},
      {"kind":"drop","label":"PFOA","track":[[145,205],[235,245],[335,245],[430,245],[520,245],[565,245]],"from":0},
      {"kind":"house","label":"water district","track":[[535,195],[535,195],[535,195],[535,195],[535,195],[535,195]],"from":0},
      {"kind":"file","label":"internal study","track":[[165,95],[250,95],[335,95],[335,150],[335,150],[335,150]],"from":1},
      {"kind":"drawer","label":"closed file","track":[[420,95],[420,95],[420,95],[420,95],[500,95],[500,95]],"from":1},
      {"kind":"gavel","label":"settlement","track":[[580,105],[580,105],[580,105],[500,105],[400,105],[400,105]],"from":3},
      {"kind":"lab","label":"C8 panel","track":[[575,175],[575,175],[575,175],[520,175],[415,175],[325,175]],"from":3}
    ]
  },
  {
    "id": "sackler-purdue",
    "title": "Sackler gifts met Purdue markets",
    "question": "When did education support sales?",
    "body": """**Documented fact.** The Sacklers owned Purdue Pharma. Purdue launched OxyContin during 1996. The company funded pain education. It supported university programs. Tufts received related gifts. Purdue also paid speakers. Government records show more. Purdue later admitted conspiracies. One involved misleading DEA reporting. Another involved doctor payments. Those payments encouraged prescriptions. Purdue funded electronic prompts. They recommended Purdue opioids. The Justice Department announced settlements. Purdue’s plea covered 2007–2017. Sackler shareholders settled allegations separately. Pain treatment had real needs. Many patients lacked relief. Better education could help. Controlled-release opioids also had uses. **Scholarly interpretation.** Funding created credibility channels. Education and marketing overlapped. University prestige softened scrutiny. Speaker programs widened reach. **Counterevidence and limits.** A grant proves no corruption. Researchers retain individual agency. Legitimate pain care existed. OxyContin caused no crisis alone. Prescribing culture also mattered. Regulators also made decisions. Insurers shaped treatment options. Illicit fentanyl later dominated deaths. The record establishes payments. It establishes corporate admissions. It supports institutional influence. It cannot assign each prescription. Nor can gifts prove intent. Specific documents carry weight.""",
    "summary": "Pain education met marketing. Admissions show paid prescription channels.",
    "sources": [
      ["Congressional Hearing 116-130", "https://www.govinfo.gov/app/details/CHRG-116hhrg43010"],
      ["Justice Department Resolution", "https://www.oversight.gov/justice-department-announces-global-resolution-criminal-and-civil-investigations-opioid"],
      ["How Tufts Gifts Advanced Goals", "https://www.statnews.com/2019/04/09/sackler-purdue-pharma-gifts-to-tufts-advanced-company-interests/"]
    ],
    "beats": ["Pain needs invite funding.", "Money enters medical education.", "Speakers carry prescribing messages.", "Prescriptions expand patient exposure.", "Admissions clarify the channel."],
    "setting": "Medical school and clinic",
    "objects": [
      {"kind":"pillfactory","label":"Purdue","track":[[65,220],[65,220],[65,220],[65,220],[65,220],[65,220]],"from":0},
      {"kind":"coin","label":"grant","track":[[120,165],[220,145],[305,125],[305,125],[305,125],[305,125]],"from":1},
      {"kind":"university","label":"pain program","track":[[325,210],[325,210],[325,210],[325,210],[325,210],[325,210]],"from":0},
      {"kind":"doctor","label":"speaker","track":[[350,225],[350,225],[430,200],[500,195],[500,195],[500,195]],"from":2},
      {"kind":"script","label":"prescription","track":[[420,115],[420,115],[470,130],[530,155],[565,190],[565,190]],"from":2},
      {"kind":"patient","label":"patient","track":[[565,235],[565,235],[565,235],[565,235],[565,235],[565,235]],"from":0},
      {"kind":"warning","label":"court record","track":[[565,85],[565,85],[565,85],[565,85],[470,85],[365,85]],"from":4}
    ]
  },
  {
    "id": "wellcome",
    "title": "Wellcome: medicine funded medicine",
    "question": "What can one bequest build?",
    "body": """**Documented fact.** Henry Wellcome sold medicines. His 1936 will created Wellcome. The trust inherited his company. It owned every share. Dividends funded medical research. Early grants followed founder interests. Pharmacy received attention. Pharmacology received attention. Tropical medicine received attention. Veterinary medicine also benefited. The company became profitable. Research spending then expanded. Partial share sales began. A 1986 listing diversified assets. Remaining shares sold later. Investment returns replaced dividends. The trust funded major infrastructure. Sanger helped sequence genomes. Overseas programs built partnerships. Ebola research gained fast support. Peer reviewers now assess grants. **Scholarly interpretation.** Commercial wealth built public knowledge. Ownership also shaped early scope. Diversification reduced one dependency. Independent governance added distance. This model shows dual effects. Concentrated wealth enables scale. Concentrated choice sets agendas. **Counterevidence and limits.** Founder influence changed over time. Today’s trust differs greatly. Its company no longer funds grants. External reviewers constrain decisions. Public agencies also choose priorities. Genome success has many funders. Attribution therefore remains shared. The archive documents structures. It does not prove capture. Scale alone proves no harm. Accountability still warrants scrutiny.""",
    "summary": "A drug fortune built research. Governance reduced founder control.",
    "sources": [
      ["Wellcome Trust Corporate Archive", "https://wellcomecollection.org/works/x5w2tw8d"],
      ["Wellcome: How We Are Funded", "https://wellcome.org/about-us/investments"],
      ["Wellcome History", "https://wellcome.org/about-us"],
      ["Wellcome Governance", "https://wellcome.org/about-us/our-people/governance"]
    ],
    "beats": ["Drug sales create dividends.", "Dividends fill the trust.", "Grants reach research labs.", "Share sales diversify funding.", "Reviewers filter future grants."],
    "setting": "Pharmacy, trust, genome lab",
    "objects": [
      {"kind":"pharmacy","label":"Wellcome company","track":[[65,215],[65,215],[65,215],[65,215],[65,215],[65,215]],"from":0},
      {"kind":"coin","label":"dividends","track":[[120,170],[220,150],[300,145],[300,145],[300,145],[300,145]],"from":0},
      {"kind":"trust","label":"1936 trust","track":[[315,220],[315,220],[315,220],[315,220],[315,220],[315,220]],"from":0},
      {"kind":"grant","label":"research grant","track":[[340,155],[340,155],[435,145],[515,135],[515,135],[515,135]],"from":2},
      {"kind":"dna","label":"genome work","track":[[550,220],[550,220],[550,220],[550,220],[550,220],[550,220]],"from":2},
      {"kind":"portfolio","label":"diversified assets","track":[[170,90],[170,90],[170,90],[260,90],[360,90],[360,90]],"from":3},
      {"kind":"review","label":"peer review","track":[[565,90],[565,90],[565,90],[565,90],[475,90],[400,90]],"from":4}
    ]
  },
  {
    "id": "gates-who",
    "title": "Gates grants steer WHO resources",
    "question": "Who chooses earmarked priorities?",
    "body": """**Documented fact.** The Gates Foundation funds WHO. Grants usually carry purposes. A 2025 study counted them. It covered 2000 through 2024. Researchers found 640 grants. Their value reached $5.5 billion. Infectious diseases received four-fifths. Polio received almost three-fifths. Vaccine work received over half. Health systems received 0.7 percent. Noncommunicable diseases received under one percent. WHO relies heavily on voluntary money. Most such money is earmarked. Gates funding supported vaccination. It supported disease modeling. It supported new medical tools. These programs can prevent deaths. They also mobilize other donors. **Scholarly interpretation.** Earmarks shift institutional attention. Donors gain agenda power. Measurable technologies become attractive. System capacity can lose funding. **Counterevidence and limits.** Funding alignment proves no coercion. WHO accepts each grant. Member states created dependence. Their assessed payments stayed low. Polio eradication requires concentration. Vaccines bring broad benefits. The study tracked allocations. It did not measure outcomes. It also found no secret control. Gates reports public priorities. The documented mechanism is earmarking. The unresolved question concerns balance. Public financing could change it.""",
    "summary": "Earmarked grants fund vaccines. Other WHO priorities receive less.",
    "sources": [
      ["Who’s Leading WHO?", "https://gh.bmj.com/content/10/10/e015343"],
      ["BMJ Study Summary", "https://bmjgroup.com/world-health-organizations-priorities-shaped-by-its-reliance-on-grants-from-donor-organisations-such-as-the-gates-foundation/"],
      ["Gates Foundation Work", "https://www.gatesfoundation.org/our-work"],
      ["Global Health Philanthropy Conflicts", "https://pmc.ncbi.nlm.nih.gov/articles/PMC3075225/"]
    ],
    "beats": ["States leave funding gaps.", "Earmarked grants enter WHO.", "Most funding targets infections.", "Vaccines reach many clinics.", "Other priorities remain thin."],
    "setting": "WHO allocation table",
    "objects": [
      {"kind":"states","label":"member states","track":[[65,215],[65,215],[65,215],[65,215],[65,215],[65,215]],"from":0},
      {"kind":"gap","label":"budget gap","track":[[160,210],[230,210],[230,210],[230,210],[230,210],[230,210]],"from":0},
      {"kind":"foundation","label":"Gates grants","track":[[70,100],[160,105],[250,120],[250,120],[250,120],[250,120]],"from":1},
      {"kind":"who","label":"WHO","track":[[310,205],[310,205],[310,205],[310,205],[310,205],[310,205]],"from":0},
      {"kind":"vials","label":"vaccines","track":[[355,145],[355,145],[430,130],[520,115],[560,140],[560,140]],"from":2},
      {"kind":"clinic","label":"clinics","track":[[560,220],[560,220],[560,220],[560,220],[560,220],[560,220]],"from":0},
      {"kind":"hospital","label":"health systems","track":[[430,260],[430,260],[430,260],[455,260],[480,260],[495,260]],"from":4}
    ]
  },
  {
    "id": "coca-cola-gebn",
    "title": "Coca-Cola funded energy-balance science",
    "question": "How did funding shape emphasis?",
    "body": """**Documented fact.** Coca-Cola funded nutrition researchers. It also backed GEBN. That network launched during 2014. Its message stressed energy balance. Physical activity received strong emphasis. Diet received less emphasis. Researchers later examined emails. Freedom-of-information requests produced them. The corpus exceeded 18,000 pages. Analysts found messaging coordination. They found constituency building. Some communications minimized funding visibility. Coca-Cola also published funding lists. Another study mapped those disclosures. Funded work clustered around activity. Energy balance also featured. Exercise research has real value. Obesity has multiple causes. Activity improves many health outcomes. **Scholarly interpretation.** Funding selected helpful questions. Those questions favored company interests. Influence worked through emphasis. It required no false experiment. Network building amplified messages. **Counterevidence and limits.** Funding never disproves findings. Energy balance remains valid biology. Researchers were not identical. Email analysis involves interpretation. It cannot measure every effect. The work covered selected universities. GEBN later dissolved publicly. Coca-Cola promised more transparency. Disclosure improved some visibility. Yet transparency lists remained incomplete. The strongest claim concerns influence. It does not prove fabrication.""",
    "summary": "Research funding shifted emphasis. Exercise overshadowed beverage intake.",
    "sources": [
      ["Coca-Cola Emails Analysis", "https://pubmed.ncbi.nlm.nih.gov/32744984/"],
      ["Research Funding Network Analysis", "https://pmc.ncbi.nlm.nih.gov/articles/PMC5962884/"],
      ["Science Organisations and Coca-Cola", "https://pmc.ncbi.nlm.nih.gov/articles/PMC6109246/"],
      ["GEBN Disbanded", "https://www.bmj.com/content/351/bmj.h6590"]
    ],
    "beats": ["Company funds research networks.", "Emails coordinate public emphasis.", "Exercise messaging moves forward.", "Sugary drinks move backward.", "Disclosure brings outside scrutiny."],
    "setting": "Research network and newsroom",
    "objects": [
      {"kind":"bottle","label":"Coca-Cola","track":[[65,220],[65,220],[65,220],[65,220],[65,245],[65,245]],"from":0},
      {"kind":"coin","label":"funding","track":[[110,160],[210,145],[300,140],[300,140],[300,140],[300,140]],"from":0},
      {"kind":"network","label":"GEBN","track":[[320,210],[320,210],[320,210],[320,210],[320,210],[320,210]],"from":0},
      {"kind":"email","label":"emails","track":[[260,90],[325,90],[410,105],[470,120],[470,120],[470,120]],"from":1},
      {"kind":"runner","label":"exercise","track":[[400,235],[400,235],[460,220],[535,195],[575,180],[575,180]],"from":2},
      {"kind":"sugar","label":"drink intake","track":[[510,175],[510,175],[510,175],[460,205],[410,245],[410,245]],"from":3},
      {"kind":"magnifier","label":"disclosure","track":[[575,85],[575,85],[575,85],[575,85],[490,85],[390,85]],"from":4}
    ]
  },
  {
    "id": "primitive-kin",
    "title": "Primitive Echo: kin advantage",
    "question": "Why do families receive preference?",
    "body": """**Documented evidence.** Humans often help relatives. Small-scale societies show this. Food transfers frequently favor kin. Evolutionary theory offers one mechanism. Helping relatives can preserve genes. Hamilton formalized that logic. Yet human kinship exceeds biology. Families also exchange repeatedly. Reputation can stabilize support. Marriage links networks. Cultural rules define relatives. Institutions later formalize inheritance. Firms can preserve family control. Foundations can preserve family priorities. **Scholarly interpretation.** Old kin bias scales upward. Wealth makes that scaling durable. Trust strengthens close networks. It can reduce transaction costs. It can also restrict access. Outsiders receive less information. Succession can bypass competence. Philanthropy redirects some wealth. It can fund public goods. **Counterevidence and limits.** Kin selection explains no dynasty alone. One Ache study found reciprocity stronger. Food transfers followed exchange patterns. Cultural institutions also dominate choices. Laws reshape inheritance. Markets reward non-kin cooperation. Many founders surrender control. Some relatives reject succession. Biology creates tendencies, not commands. Nepotism requires institutional analysis. Family support is not corruption. Harm depends on power. Transparency changes that risk. Independent review can counterbalance it.""",
    "summary": "Kin support has roots. Culture and rules scale it.",
    "sources": [
      ["Reciprocal Altruism, Rather Than Kin Selection", "https://gurven.anth.ucsb.edu/sites/secure.lsit.ucsb.edu.anth.d7_gurven/files/sitefiles/papers/allenaraveetal2008.pdf"],
      ["Cultural Group Selection and Cooperation", "https://pmc.ncbi.nlm.nih.gov/articles/PMC10427285/"],
      ["Nepotistic Cooperation in Primates", "https://pmc.ncbi.nlm.nih.gov/articles/PMC2781876/"],
      ["Kin Selection Theory History", "https://arxiv.org/abs/1305.4354"]
    ],
    "beats": ["Relatives share repeated support.", "Genes offer one pathway.", "Reciprocity offers another pathway.", "Inheritance scales family advantage.", "Rules can limit capture."],
    "setting": "Camp, family tree, boardroom",
    "objects": [
      {"kind":"family","label":"family","track":[[85,215],[85,215],[85,215],[85,215],[85,215],[85,215]],"from":0},
      {"kind":"food","label":"shared food","track":[[120,170],[205,160],[285,155],[285,155],[285,155],[285,155]],"from":0},
      {"kind":"kin","label":"close kin","track":[[305,220],[305,220],[305,220],[305,220],[305,220],[305,220]],"from":0},
      {"kind":"token","label":"reciprocity","track":[[355,140],[355,140],[430,145],[500,155],[500,155],[500,155]],"from":2},
      {"kind":"stranger","label":"non-kin partner","track":[[545,220],[545,220],[545,220],[545,220],[545,220],[545,220]],"from":2},
      {"kind":"tree","label":"inheritance","track":[[250,85],[250,85],[250,85],[330,85],[400,85],[400,85]],"from":3},
      {"kind":"audit","label":"independent rules","track":[[575,90],[575,90],[575,90],[575,90],[500,90],[430,90]],"from":4}
    ]
  }
]

def words(text):
    clean = re.sub(r"https?://\S+|[*#]", "", text)
    return len(re.findall(r"\b[\w’.-]+\b", clean))

for card in cards:
    count = words(card["body"])
    if not 140 <= count <= 200:
        raise ValueError((card["title"], count))
    card["word_count"] = count

lesson = {
  "title": "Fortunes, Funding, and Focus",
  "subtitle": "History Investigation — 28 September 2026, 01:00 Réunion",
  "palette": {"ink":"#272735","paper":"#f3e6c8","teal":"#2a7775","coral":"#cf5c4f","gold":"#e0a83e","blue":"#4b78a3","green":"#6e8b67"},
  "chapter_seconds": 30,
  "fps": 25,
  "cards": cards
}

(ROOT / "lesson.json").write_text(json.dumps(lesson, ensure_ascii=False, indent=2), encoding="utf-8")

source_md = lambda c: "\n".join(f"- [{html.escape(t)}]({u})" for t,u in c["sources"])
parts = ["# Fortunes, Funding, and Focus", "", "History Investigation — 28 September 2026, 01:00 Réunion", "", "Five cases examine private funding. One behavior card follows. Facts, interpretation, and uncertainty stay separate.", ""]
for i,c in enumerate(cards,1):
    parts += [f"## {i}. {c['title']}", "", c["body"], "", f"*Word count: {c['word_count']}*", "", "### Sources", "", source_md(c), ""]
parts += ["## Illustration", "", "![Funding influence evidence ladder](evidence.svg)", "", "## Production note", "", "The HTML file remains unpublished. The video and viewer share lesson data. The viewer works offline."]
(ROOT / "edition.md").write_text("\n".join(parts), encoding="utf-8")

sections=[]
for i,c in enumerate(cards,1):
    paras = "".join(f"<p>{html.escape(p).replace('**','')}</p>" for p in c["body"].split("\n\n"))
    links = "".join(f'<li><a href="{u}">{html.escape(t)}</a></li>' for t,u in c["sources"])
    sections.append(f'<section id="{c["id"]}"><p class="kicker">CARD {i:02d} · {c["word_count"]} WORDS</p><h2>{html.escape(c["title"])}</h2>{paras}<h3>Sources</h3><ul>{links}</ul></section>')
wp = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{lesson['title']}</title><style>body{{margin:auto;max-width:900px;padding:32px;font:18px/1.6 Georgia,serif;color:#272735;background:#f3e6c8}}h1,h2,h3,.kicker{{font-family:Arial,sans-serif}}h1{{font-size:clamp(42px,8vw,86px);line-height:.95}}section{{border-top:3px solid #272735;padding:32px 0}}a{{color:#165b72}}.kicker{{font-size:12px;letter-spacing:.15em}}img{{max-width:100%}}.notice{{padding:14px;border:2px solid #cf5c4f}}</style></head><body><p class="kicker">HISTORY INVESTIGATION</p><h1>{lesson['title']}</h1><p class="notice"><strong>Unpublished draft.</strong> Prepared for WordPress. No website upload occurred.</p>{''.join(sections)}<section><h2>Evidence map</h2><img src="evidence.svg" alt="Evidence ladder comparing five funding mechanisms and one behavioral mechanism"></section></body></html>'''
(ROOT / "wordpress-draft.html").write_text(wp, encoding="utf-8")

labels = ["PFOA", "OxyContin", "Wellcome", "WHO grants", "GEBN", "Kin bias"]
colors = ["#cf5c4f","#e0a83e","#2a7775","#4b78a3","#cf5c4f","#6e8b67"]
rows=[]
for i,(lab,col) in enumerate(zip(labels,colors)):
    y=116+i*78
    rows.append(f'<g><rect x="48" y="{y}" width="170" height="48" rx="3" fill="{col}"/><text x="64" y="{y+31}" class="label">{lab}</text><path d="M230 {y+24} H390"/><circle cx="410" cy="{y+24}" r="16" fill="{col}"/><path d="M430 {y+24} H590"/><rect x="605" y="{y}" width="220" height="48" rx="3" fill="#f3e6c8"/><text x="620" y="{y+30}" class="small">{['records → settlement','gifts → speakers','dividends → grants','earmarks → allocation','emails → emphasis','kin → institutions'][i]}</text></g>')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="640" viewBox="0 0 900 640" role="img" aria-labelledby="title desc"><title id="title">Funding influence evidence ladder</title><desc id="desc">Six rows show how money or kin ties pass through institutions, create incentives, and meet evidence checks.</desc><rect width="900" height="640" fill="#f3e6c8"/><style>text{{font-family:Arial,sans-serif;fill:#272735}}.head{{font-weight:700;font-size:34px}}.label{{font-weight:700;font-size:20px;fill:white}}.small{{font-size:17px}}path{{stroke:#272735;stroke-width:5;fill:none}}rect{{stroke:#272735;stroke-width:2}}</style><text x="48" y="60" class="head">Money changes research pathways</text><text x="48" y="90" class="small">Follow mechanism. Then inspect evidence.</text>{''.join(rows)}<text x="48" y="605" class="small">Source links appear inside the edition.</text></svg>'''
(ROOT / "evidence.svg").write_text(svg, encoding="utf-8")

viewer = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Lesson viewer</title><style>body{margin:0;background:#272735;color:#f3e6c8;font:16px Arial,sans-serif}.wrap{max-width:1100px;margin:auto;padding:18px}canvas{width:100%;background:#f3e6c8;border:3px solid #f3e6c8}.controls{display:flex;gap:10px;align-items:center;flex-wrap:wrap}button,input{font:inherit}button{padding:9px 13px;border:0;background:#e0a83e;color:#272735}input{flex:1}.objects{display:flex;gap:7px;flex-wrap:wrap;margin:12px 0}.objects button{background:#2a7775;color:white}.panel{border-left:5px solid #cf5c4f;padding:8px 14px;background:#353545}.sources a{color:#f2cb68}.reduced canvas{display:none}@media(prefers-reduced-motion:reduce){canvas{display:none}}</style></head><body><main class="wrap"><h1>Fortunes, Funding, and Focus</h1><canvas id="c" width="960" height="540" aria-label="Animated cut-paper causal scene"></canvas><div class="controls"><button id="play">Pause</button><button id="back">Step back</button><button id="next">Step forward</button><button id="replay">Replay</button><input id="scrub" type="range" min="0" max="180" step="0.04" value="0"><button id="motion">Reduced motion</button></div><div class="objects" id="objects"></div><article class="panel"><h2 id="title"></h2><p id="beat"></p><p id="fact"></p><div class="sources" id="sources"></div></article></main><script>const DATA=__DATA__;const C=document.querySelector('#c'),x=C.getContext('2d'),scrub=document.querySelector('#scrub');let t=0,playing=true,last=performance.now(),reduced=false;const P=DATA.palette;function ease(v){return v*v*(3-2*v)}function interp(track,p){let k=Math.min(4,Math.floor(p*5)),q=ease(p*5-k),a=track[k],b=track[k+1];return[a[0]+(b[0]-a[0])*q,a[1]+(b[1]-a[1])*q]}function paper(px,py,w,h,col){x.fillStyle='#9f927b';x.fillRect(px+7,py+8,w,h);x.fillStyle=col;x.strokeStyle=P.ink;x.lineWidth=3;x.fillRect(px,py,w,h);x.strokeRect(px,py,w,h)}function draw(o,p){let[a,b]=interp(o.track,p),k=o.kind;x.save();x.translate(a*1.5,b*1.5);x.fillStyle=P.gold;x.strokeStyle=P.ink;x.lineWidth=3;if(['coin','drop','food','token'].includes(k)){x.beginPath();x.arc(0,0,k==='drop'?12:20,0,7);x.fill();x.stroke()}else if(['doctor','patient','runner','family','kin','stranger'].includes(k)){x.beginPath();x.arc(0,-28,16,0,7);x.fill();x.stroke();paper(-18,-8,36,50,k==='runner'?P.coral:P.blue)}else if(k==='dna'){x.strokeStyle=P.coral;for(let i=-35;i<35;i+=8){x.beginPath();x.moveTo(-18,i);x.lineTo(18,i+8);x.stroke()}}else{paper(-34,-27,68,54,['factory','pillfactory','pharmacy','foundation','who','network','trust'].includes(k)?P.teal:P.paper)}x.fillStyle=P.ink;x.font='bold 14px Arial';x.textAlign='center';x.fillText(o.label,0,54);x.restore()}function render(){let ci=Math.min(5,Math.floor(t/30)),local=t-ci*30,p=local/30,c=DATA.cards[ci];x.fillStyle=P.paper;x.fillRect(0,0,C.width,C.height);x.fillStyle=ci%2? '#ded8cf':'#dce5d8';x.fillRect(0,76,C.width,390);x.fillStyle=P.ink;x.fillRect(0,0,C.width,72);x.fillRect(0,468,C.width,72);x.fillStyle=P.paper;x.font='bold 26px Arial';x.textAlign='left';x.fillText((ci+1).toString().padStart(2,'0')+'  '+c.title.toUpperCase(),26,45);for(const o of c.objects)if(local>=o.from*6)draw(o,p);let beat=Math.min(4,Math.floor(local/6));x.fillStyle=P.paper;x.font='bold 28px Arial';x.fillText(c.beats[beat],26,512);document.querySelector('#title').textContent=c.title;document.querySelector('#beat').textContent=c.beats[beat];document.querySelector('#fact').textContent=c.summary;document.querySelector('#sources').innerHTML=c.sources.map(s=>`<a href="${s[1]}">${s[0]}</a>`).join(' · ');document.querySelector('#objects').innerHTML=c.objects.map((o,i)=>`<button data-i="${i}">${o.label}</button>`).join('');document.querySelectorAll('#objects button').forEach(b=>b.onclick=()=>{let o=c.objects[+b.dataset.i];document.querySelector('#fact').textContent=o.label+' participates here. Open sources for evidence.'});scrub.value=t}function loop(now){if(playing&&!reduced)t=(t+(now-last)/1000)%180;last=now;render();requestAnimationFrame(loop)}document.querySelector('#play').onclick=()=>{playing=!playing;document.querySelector('#play').textContent=playing?'Pause':'Play'};document.querySelector('#back').onclick=()=>{playing=false;t=Math.max(0,t-1);render()};document.querySelector('#next').onclick=()=>{playing=false;t=Math.min(179.96,t+1);render()};document.querySelector('#replay').onclick=()=>{t=Math.floor(t/30)*30;playing=true};document.querySelector('#motion').onclick=()=>{reduced=!reduced;document.body.classList.toggle('reduced',reduced);playing=!reduced};scrub.oninput=e=>{playing=false;t=+e.target.value;render()};requestAnimationFrame(loop)</script></body></html>'''.replace('__DATA__', json.dumps(lesson, ensure_ascii=False))
(ROOT / "lesson-viewer.html").write_text(viewer, encoding="utf-8")

readme = """# Fortunes, Funding, and Focus\n\nThis edition examines family wealth, institutions, and corporate influence on research.\n\n- `edition.md`: sourced cards\n- `wordpress-draft.html`: unpublished draft\n- `evidence.svg`: original evidence map\n- `lesson.json`: shared scene data\n- `lesson-viewer.html`: offline interactive viewer\n- `render_video.py`: editable renderer\n- `history-investigation.mp4`: silent visual lesson\n\nWebsite publishing did not occur.\n"""
(ROOT / "README.md").write_text(readme, encoding="utf-8")

print(json.dumps({"word_counts":[c["word_count"] for c in cards],"cards":len(cards)}, indent=2))
