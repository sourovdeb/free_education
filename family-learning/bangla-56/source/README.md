# Bangla à la maison

56 pages. 56 activités HTML.

Pour jouer avec un adulte.
Âge visé : 3–4 ans.

## Ouvrir

Décompressez le ZIP.
Ouvrez `index.html`.
Internet n’est pas nécessaire.
Gardez tous les fichiers ensemble.

`book.pdf` contient le livre.
`pages/page-01.html` ouvre son jeu.
Les numéros correspondent au PDF.
Chaque page possède son entrée HTML.
Les jeux partagent leur moteur.

## Parcours

| Pages | Contenu |
|---|---|
| 1–3 | Images, écho, présentation |
| 4–9 | Les 11 voyelles |
| 10–27 | 36 consonnes et formes |
| 28 | ং, ঃ, ঁ : trois signes |
| 29 | ক্ষ et জ্ঞ : groupes |
| 30–31 | Les dix signes vocaliques |
| 32–37 | Nombres de 0 à 10 |
| 38–39 | Découverte de 11 à 20 |
| 40–43 | Ajouter, enlever, grouper, partager |
| 44–51 | Objets, corps et émotions |
| 52–55 | Quatre extraits de comptines/poèmes |
| 56 | Paires d’images |

Le classement traditionnel varie.
Ici : 11 voyelles, 36 consonnes/formes.
Trois signes complètent les 39 entrées.
ক্ষ et জ্ঞ sont des groupes.
Les formes sanskrites historiques sont exclues.
Le tableau couvre le bangla usuel.

## Avec votre enfant

Choisissez une page selon l’envie.
Montrez une image. Nommez-la.
Attendez la réponse, même gestuelle.
Répétez sans demander de performance.
Arrêtez quand l’enfant le souhaite.

Les jeux supposent un adulte lecteur.
L’enfant n’a pas besoin de lire.
Les lettres rares sont une découverte.
Les opérations restent une manipulation.
11–20 reste une extension facultative.
Ne demandez pas de tables.
Utilisez des jouets sans petites pièces.

Les poèmes sont des extraits.
Ils ne sont pas présentés complets.
Les gestes accompagnent chaque vers.
Les traductions expliquent le sens.
Elles ne cherchent pas la rime.

## Prononciation pour francophones

Cette transcription reste approximative.
Elle n’est pas une norme linguistique.
La voix familiale reste le modèle.
Une relecture bengalophone reste souhaitable.

| Repère | Comment lire |
|---|---|
| a | « patte », jamais « ain » |
| i | « ici » |
| ou | « loup », pas « lune » |
| é | « été » |
| è | « père » |
| ô | o ouvert de « porte » |
| o | o fermé de « mot » |
| oï | o puis i, liés |
| o-ou | o puis ou, liés |
| ch | « chat » |
| tch | « tchao » |
| dj | « djembé » |
| g | « gare », toujours dur |
| kh, gh, th, dh, ph, bh | Consonne puis souffle, sans voyelle supplémentaire |
| h | Un souffle, non muet |
| r | Battement de langue, approximatif |
| ã, ĩ, ũ | Voyelle nasalisée, pas « an/in/un » français |
| ng | Un son, comme « parking » |

Tous les n et m écrits s’entendent.
`tine` conserve le n final.
`am` n’est pas nasal.
`sat` conserve le t final.
`at` ne finit pas par th.
Le h n’est jamais l’anglais « th ».
ফ peut se réaliser ph ou f.
Les variantes familiales sont légitimes.

Les deux séries ট/ত, ঠ/থ, ড/দ, ঢ/ধ ne sont pas distinguées entièrement par ces repères français : l’adulte montre la différence d’articulation.
Pour les noms des lettres ঙ et ঞ, les repères oung/gno sont seulement des aides approximatives ; donnez votre modèle oral.
Le même graphème change parfois de son selon le mot. Écoutez le mot entier.

## Audio

Le bouton vocal cherche une voix bangla.
Sans voix installée, il l’annonce.
Il ne choisit pas une voix française.
Une voix installée peut nécessiter Internet.
Les jeux restent utilisables sans voix.

Vous pouvez choisir votre enregistrement.
Le fichier reste sur votre appareil.
Il disparaît en changeant de page.
Aucun microphone n’est activé.
Aucun fichier n’est envoyé.

## Publier sur votre site

1. Ouvrez le gestionnaire de fichiers.
2. Créez `public_html/bangla-56/`.
3. Téléversez le contenu du dossier.
4. Gardez les sous-dossiers et noms.
5. Ouvrez `https://sourovdeb.com/bangla-56/index.html`.

Cette adresse est un exemple d’installation.
Ce paquet ne modifie pas WordPress.
Évitez de coller JavaScript dans l’éditeur.
Dans WordPress, ajoutez un lien.
Ou utilisez un bloc HTML :

```html
<iframe src="/bangla-56/index.html"
  title="Jeux bangla et français"
  width="100%" height="1000"
  style="border:0" loading="lazy"></iframe>
```

Chaque activité est partageable :
`/bangla-56/pages/page-40.html` pour l’addition.
`/bangla-56/index.html#52` pour la lune.

GitHub conserve les fichiers.
GitHub Pages demande une activation distincte.
Un lien de dépôt n’est pas un site.

## Modifier

`content.json` contient les données lisibles.
Le navigateur lit `content.js`.
Modifiez ce fichier pour une retouche.
`source/content.py` est la source principale.
Le générateur recopie le site.
Il reconstruit PDF et ZIP.

Pour reconstruire : placez les sources dans un dossier, avec `release/assets/` déjà fourni. Copiez aussi `LICENCE-MIT.txt` à côté de `build.py`. Installez `pymupdf`, `reportlab`, `svglib` et `markdown`. Lancez `python3 build.py`. Les sources ne nécessitent ni compte ni clé.

## Vérification

56 pages PDF rendues et inspectées.
56 activités testées dans Chromium.
Ouverture locale sans serveur testée.
Écran mobile : largeur 390 pixels.
Aucun débordement horizontal détecté.
Entrée directe, page 43 : testée.
Absence de voix bangla : testée.
La prononciation demande une relecture familiale.
Les tests ne remplacent pas cette relecture.

## Sources consultées

- [Unicode : bloc bengali](https://unicode.org/charts/PDF/U0980.pdf) : caractères, formes, signes.
- [Alphabet et signes vocaliques](https://bengalityping.com/bengali-alphabet) : inventaire pédagogique comparé.
- [Comptine de la lune](https://www.teachers.gov.bd/content/details/1722487) : début traditionnel. La première version de ce projet est remplacée ; pas de vers inventé ajouté.
- [Tagore, Talgach](https://bn.wikisource.org/wiki/শিশু_ভোলানাথ/তালগাছ) : les trois premiers vers. Shishu Bholanath, 1922. Source Wikisource.
- [Amader chhoto nodi](https://www.teachers.gov.bd/content/details/1729477) : repérage pédagogique. Texte d’ouverture recoupé avec [cet exemplaire cité](https://www.facebook.com/sankar.chakraborty.1800/posts/2988766531319908/). Tagore, Sahaj Path ; deux premiers vers.
- [Ghumparani masi-pisi](https://www.prothomalo.com/onnoalo/children/ঘুমপাড়ানি-মাসিপিসি) : comptine identifiée comme traditionnelle. Quatre premiers vers.

Consultation : 23 septembre 2026.
Les variantes orales sont signalées.
Les repères français sont éditoriaux.
Aucun enregistrement source n’est reproduit.

## Droits et crédits

Code original : licence MIT.
Texte pédagogique et traduction : CC BY 4.0.
Crédit : projet Free Education, Sourov Deb.
Les textes traditionnels restent traditionnels.
Les extraits de Tagore sont attribués.
La licence nouvelle ne les revendique pas.

Illustrations Twemoji, copyright Twitter et autres contributeurs, CC BY 4.0 : https://github.com/jdecked/twemoji. Illustrations inchangées, dimensions adaptées. Oreiller et rivière : dessins originaux CC BY 4.0.
Police Noto Sans Bengali : SIL OFL 1.1. Les textes de licence sont fournis dans `assets/`.
Licence CC BY : https://creativecommons.org/licenses/by/4.0/

## Limites

Ce support ne remplace pas l’échange.
Ce n’est pas un test développemental.
Les jeux n’évaluent pas la prononciation.
Le dessin n’est pas corrigé automatiquement.
Les émotions n’ont aucune bonne réponse.
Le livre ne reprend pas les photos.
Il ne reproduit pas leur mise en page.
