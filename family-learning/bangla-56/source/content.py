"""One content source drives the book and every game. French respelling is approximate."""
PAGES=[]
def item(bn,ph,fr,icon='star',glyph=None,note=''):
    return dict(bn=bn,ph=ph,fr=fr,icon=icon,glyph=glyph or bn,note=note)
def add(title,fr,items,kind='match',action='Montre. Écoute. Dis le mot.',note='',**kw):
    PAGES.append(dict(id=len(PAGES)+1,title=title,fr=fr,items=items,kind=kind,action=action,note=note,**kw))

add('বাংলা খেলার বই','Bangla à la maison',[
 item('চাঁদ','tchãd','lune','moon'),item('আম','am','mangue','mango')],
 action='Montre la lune.',note='56 pages • 56 jeux • 3–4 ans • Avec un adulte')
add('শুনি আর বলি','J’écoute. Je répète.',[
 item('মা','ma','maman','woman'),item('বাবা','ba-ba','papa','man')],kind='echo',action='Écoute. Puis fais écho.',
 note='Guide adulte : ô comme « porte » ; o comme « mot » ; ou comme « loup ».')
add('আমার নাম','Je m’appelle…',[
 item('আমার নাম…','a-mar nam…','Je m’appelle…','child'),item('তোমার নাম কী?','to-mar nam ki ?','Comment tu t’appelles ?','wave')],kind='echo',action='Dis ton nom. Salue.',note='Le prénom reste oral. Aucune donnée personnelle enregistrée.')

V=[
 item('অজগর','ô-djô-gôr','python','snake','অ'),item('আম','am','mangue','mango','আ'),
 item('ইঁদুর','ĩ-dour','souris','mouse','ই'),item('ঈগল','i-gôl','aigle','eagle','ঈ'),
 item('উট','out','chameau','camel','উ'),item('ঊন','oun','moins de','minus','ঊ','Mot abstrait : l’adulte explique avec des objets.'),
 item('ঋতু','ri-tou','saison','sun','ঋ'),item('এক','èk','un','one','এ'),
 item('ঐ','oï','là-bas','point','ঐ'),item('ও','o','et','plus','ও'),
 item('ঔষধ','ou-chôdh','médicament','medicine','ঔ','Seulement avec un adulte. Ne pas toucher.')]
for i in range(0,len(V),2):
    a=V[i:i+2]
    add(' '.join(x['glyph'] for x in a),'Voyelles • '+str(i//2+1),a,kind='letters',action='Retrouve la même lettre.',
        note='Écoute un mot. Observe une lettre. Pas de mémorisation exigée.')

C=[
 item('কলা','kô-la','banane','banana','ক'),item('খাতা','kha-ta','cahier','notebook','খ'),
 item('গরু','go-rou','vache','cow','গ'),item('ঘর','ghôr','maison','house','ঘ'),
 item('রঙ','rông','couleur','palette','ঙ','La lettre se trouve à la fin.'),item('চাকা','tcha-ka','roue','wheel','চ'),
 item('ছাতা','tchha-ta','parapluie','umbrella','ছ'),item('জল','djôl','eau','water','জ'),
 item('ঝুড়ি','djhou-ri','panier','basket','ঝ'),item('পাঞ্জা','pan-dja','paume / patte','hand','ঞ','La lettre se cache dans ঞ্জ.'),
 item('টমেটো','to-mé-to','tomate','tomato','ট'),item('ঠোঁট','thõt','lèvres','lips','ঠ'),
 item('ডিম','dim','œuf','egg','ড'),item('ঢোল','dhol','tambour','drum','ঢ'),
 item('হরিণ','ho-rine','cerf','deer','ণ','Trouve la lettre à la fin.'),item('তরমুজ','tôr-moudj','pastèque','melon','ত'),
 item('থালা','tha-la','assiette','plate','থ'),item('দুধ','doudh','lait','milk','দ'),
 item('ধান','dhan','riz sur pied','rice','ধ'),item('নৌকা','nou-ka','bateau','boat','ন'),
 item('পাখি','pa-khi','oiseau','bird','প'),item('ফুল','phoul','fleur','flower','ফ'),
 item('বল','bôl','ballon','ball','ব'),item('ভাত','bhat','riz cuit','bowl','ভ'),
 item('মাছ','matchh','poisson','fish','ম'),item('যান','djan','véhicule','car','য'),
 item('রাত','rat','nuit','night','র'),item('লেবু','lé-bou','citron','lemon','ল'),
 item('শাপলা','cha-pla','nénuphar','lotus','শ'),item('ষাঁড়','chãr','taureau','ox','ষ'),
 item('সাবান','cha-ban','savon','soap','স'),item('হাতি','ha-ti','éléphant','elephant','হ'),
 item('বড়','bô-ro','grand','elephant','ড়','La lettre se trouve à la fin.'),item('আষাঢ়','a-charh','mois des pluies','rain','ঢ়','Mot de découverte. L’adulte donne le modèle.'),
 item('পায়ে','pa-yé','aux pieds','foot','য়','La lettre se trouve au milieu.'),item('উৎসব','out-chôb','fête','party','ৎ','ৎ est une forme de ত sans voyelle.')]
assert len(C)==36
for i in range(0,len(C),2):
    a=C[i:i+2]
    add(' '.join(x['glyph'] for x in a),'Lettres • '+str(i//2+1),a,kind='letters',action='Montre. Écoute. Retrouve.',
        note=' '.join(x['note'] for x in a if x['note']) or 'Les sons se découvrent avec un adulte.')

add('ং  ঃ  ঁ','Trois signes à repérer',[
 item('বাংলা','bang-la','bangla','book','ং'),item('দুঃখ','douk-kho','tristesse','sad','ঃ'),item('চাঁদ','tchãd','lune','moon','ঁ')],
 kind='letters',action='Cherche le signe dans le mot.',note='Ces signes complètent les 36 consonnes du tableau traditionnel de 39 entrées.')
add('ক্ষ  জ্ঞ','Deux lettres se rencontrent',[
 item('ক্ষীর','khir','dessert au lait','bowl','ক্ষ'),item('জ্ঞান','ggan','savoir','book','জ্ঞ')],kind='letters',
 action='Observe les lettres ensemble.',note='ক্ষ = ক্ + ষ ; জ্ঞ = জ্ + ঞ. Ce sont des groupes, pas deux lettres de plus.')
add('কা  কি  কী  কু  কূ','Les voyelles s’accrochent • 1',[
 item('কা','ka','ক + া','book'),item('কি','ki','ক + ি','book'),item('কী','ki','ক + ী','book'),item('কু','kou','ক + ু','book'),item('কূ','kou','ক + ূ','book')],kind='letters',action='Choisis une forme. Dessine-la.',note='ই et ঈ se prononcent généralement pareil ; উ et ঊ aussi.')
add('কৃ  কে  কৈ  কো  কৌ','Les voyelles s’accrochent • 2',[
 item('কৃ','kri','ক + ৃ','book'),item('কে','ké','ক + ে','book'),item('কৈ','koï','ক + ৈ','book'),item('কো','ko','ক + ো','book'),item('কৌ','ko-ou','ক + ৌ','book')],kind='letters',action='Retrouve une forme identique.',note='ঔ : o puis ou, liés. Ce n’est pas le ou de উ.')

NUMS=[('শূন্য','choun-no','zéro'),('এক','èk','un'),('দুই','douï','deux'),('তিন','tine','trois'),('চার','tchar','quatre'),('পাঁচ','pãtch','cinq'),('ছয়','tchhôï','six'),('সাত','sat','sept'),('আট','at','huit'),('নয়','nôï','neuf'),('দশ','dôch','dix'),('এগারো','è-ga-ro','onze'),('বারো','ba-ro','douze'),('তেরো','té-ro','treize'),('চৌদ্দ','tchoud-do','quatorze'),('পনেরো','pô-né-ro','quinze'),('ষোলো','cho-lo','seize'),('সতেরো','chô-té-ro','dix-sept'),('আঠারো','a-tha-ro','dix-huit'),('উনিশ','ou-nich','dix-neuf'),('কুড়ি','kou-ri','vingt')]
def digits(n): return str(n).translate(str.maketrans('0123456789','০১২৩৪৫৬৭৮৯'))
for lo,hi in [(0,1),(2,3),(4,5),(6,7),(8,9),(10,10),(11,15),(16,20)]:
    a=[dict(item(*NUMS[n],icon='star',glyph=digits(n)),count=n) for n in range(lo,hi+1)]
    add('গুনি • '+digits(lo)+'–'+digits(hi),'Je compte • '+str(lo)+'–'+str(hi),a,kind='count',action='Touche chaque objet une fois.',
        note='11–20 : découverte facultative avec un adulte.' if lo>10 else 'Commence avec 1–3 objets. Arrête si l’enfant le souhaite.')

for bn,fr,kind,equation,ph,action,note in [
 ('যোগ','On ajoute','add','১ + ১ = ২','èk ar èk, douï','Ajoute une pomme. Compte tout.','1 + 1 = 2 ; 2 + 1 = 3.'),
 ('বিয়োগ','On enlève','subtract','৩ − ১ = ২','tine thé-ké èk baad, douï','Enlève une pomme. Compte le reste.','3 − 1 = 2 ; 2 − 1 = 1.'),
 ('গুণ','Des groupes identiques','groups','২ × ২ = ৪','douï goune douï, tchar','Deux paniers. Deux pommes chacun.','Initiation facultative. Pas de tables à apprendre.'),
 ('ভাগ','On partage','share','৪ ÷ ২ = ২','tchar bhag douï, douï','Partage quatre pommes entre deux.','Deux pommes par assiette. Pas de division écrite exigée.')]:
    add(bn,fr,[item(equation,ph,'Manipule puis regarde le symbole.','apple')],kind=kind,action=action,note=note)

TOPICS=[
 ('পোশাক','Je m’habille',[('জামা','dja-ma','vêtement','shirt'),('জুতো','djou-to','chaussures','shoe'),('টুপি','tou-pi','chapeau','hat')],'Mime : je mets mes chaussures.'),
 ('হাত ধুই','Je me lave',[('সাবান','cha-ban','savon','soap'),('জল','djôl','eau','water'),('ব্রাশ','brach','brosse à dents','toothbrush')],'Montre ce qui lave.'),
 ('খাবার সময়','À table',[('থালা','tha-la','assiette','plate'),('চামচ','tcha-môtch','cuillère','spoon'),('বাটি','ba-ti','bol','bowl')],'Cherche ces objets chez toi.'),
 ('ঘুমের সময়','Au lit',[('বিছানা','bi-tchha-na','lit','bed'),('বালিশ','ba-lich','oreiller','pillow'),('বই','boï','livre','book')],'Mime : je vais dormir.'),
 ('আমার ব্যাগ','Mon sac',[('ব্যাগ','bèg','sac','bag'),('খাতা','kha-ta','cahier','notebook'),('পেন্সিল','pèn-sil','crayon','pencil')],'Que met-on dans le sac ?'),
 ('ফল খাই','Les fruits',[('আম','am','mangue','mango'),('কলা','kô-la','banane','banana'),('আপেল','a-pèl','pomme','apple')],'Montre le fruit demandé.'),
 ('আমার শরীর','Mon corps',[('হাত','hat','main','hand'),('পা','pa','pied','foot'),('চোখ','tchokh','œil','eye')],'Montre sur toi, si tu veux.'),
 ('কেমন লাগছে?','Comment je me sens ?',[('খুশি','khou-chi','joie','happy'),('দুঃখ','douk-kho','tristesse','sad'),('রাগ','rag','colère','angry')],'Choisis un visage. Parle librement.')]
for bn,fr,terms,act in TOPICS:
    add(bn,fr,[item(*x) for x in terms],kind='feelings' if bn=='কেমন লাগছে?' else 'match',action=act,
        note='Tous les ressentis sont permis. Aucune bonne réponse.' if bn=='কেমন লাগছে?' else 'L’adulte lit la consigne. L’enfant montre une image.')

add('আয় আয় চাঁদ মামা','Comptine • la lune',[
 item('আয় আয় চাঁদ মামা','aï aï tchãd ma-ma','Viens, viens, oncle Lune.','moon'),
 item('টিপ দিয়ে যা','tip di-yé dja','Pose un point sur le front.','point')],kind='poem',action='Montre la lune. Touche ton front.',
 note='Tradition orale. Extrait d’ouverture ; variantes familiales possibles.',source='https://www.teachers.gov.bd/content/details/1722487')
add('তালগাছ','Poème • le palmier',[
 item('তালগাছ এক পায়ে দাঁড়িয়ে','tal-gatchh èk pa-yé dã-ri-yé','Le palmier tient sur un pied.','palm'),
 item('সব গাছ ছাড়িয়ে','chôb gatchh tchha-ri-yé','Il dépasse tous les arbres.','tree'),
 item('উঁকি মারে আকাশে।','ũ-ki ma-ré a-ka-ché','Il regarde vers le ciel.','sky')],kind='poem',action='Lève les bras comme un arbre.',
 note='Rabindranath Tagore • Shishu Bholanath • 1922 • Extrait : trois premiers vers.',source='https://bn.wikisource.org/wiki/শিশু_ভোলানাথ/তালগাছ')
add('আমাদের ছোটো নদী','Poème • la rivière',[
 item('আমাদের ছোটো নদী চলে বাঁকে বাঁকে','a-ma-dér tchho-to nô-di tchô-lé bã-ké bã-ké','Notre rivière suit des méandres.','river'),
 item('বৈশাখ মাসে তার হাঁটু জল থাকে।','boï-chakh ma-ché tar hã-tou djôl tha-ké','En Boïchakh, l’eau atteint les genoux.','water')],kind='poem',action='Dessine la rivière avec ton doigt.',
 note='Rabindranath Tagore • Sahaj Path • Extrait : deux premiers vers. Boïchakh : avril–mai.',source='https://www.teachers.gov.bd/content/details/1729477')
add('ঘুমপাড়ানি মাসি-পিসি','Comptine • le sommeil',[
 item('ঘুমপাড়ানি মাসি-পিসি','ghoum-pa-ra-ni ma-chi pi-chi','Tantes qui apportez le sommeil,','night'),
 item('মোদের বাড়ি এসো,','mo-dér ba-ri é-cho','venez dans notre maison.','house'),
 item('খাট নাই পালং নাই','khat naï pa-lông naï','Il n’y a pas de lit,','bed'),
 item('খোকার চোখে বসো।','kho-kar tcho-khé bô-cho','venez sur les yeux du petit.','eye')],kind='poem',action='Berce un doudou en récitant.',
 note='Tradition orale • Extrait : quatre premiers vers. Mas(i) et pis(i) : tantes.',source='https://www.prothomalo.com/onnoalo/children/ঘুমপাড়ানি-মাসিপিসি')
add('আবার খেলি','Je retrouve mes mots',[
 item('আম','am','mangue','mango'),item('চাঁদ','tchãd','lune','moon'),item('বই','boï','livre','book')],kind='memory',action='Retrouve les paires.',note='Choisis une page à refaire. Pas de score ni de classement.')
assert len(PAGES)==56, len(PAGES)

SOUNDS={'অ':'ô','আ':'a','ই':'i','ঈ':'i','উ':'ou','ঊ':'ou','ঋ':'ri','এ':'é','ঐ':'oï','ও':'o','ঔ':'o-ou',
 'ক':'kô','খ':'khô','গ':'gô','ঘ':'ghô','ঙ':'oung','চ':'tchô','ছ':'tchhô','জ':'djô','ঝ':'djhô','ঞ':'gno',
 'ট':'tô','ঠ':'thô','ড':'dô','ঢ':'dhô','ণ':'nô','ত':'tô','থ':'thô','দ':'dô','ধ':'dhô','ন':'nô',
 'প':'pô','ফ':'phô','ব':'bô','ভ':'bhô','ম':'mô','য':'djô','র':'rô','ল':'lô','শ':'chô','ষ':'chô','স':'chô / sô','হ':'hô',
 'ড়':'rô','ঢ়':'rhô','য়':'y','ৎ':'t','ং':'ng','ঃ':'selon le mot','ঁ':'voyelle nasale','ক্ষ':'kh / kkh','জ্ঞ':'gg'}
for page in PAGES:
    for x in page['items']: x['sound']=SOUNDS.get(x['glyph'],x['ph'])
