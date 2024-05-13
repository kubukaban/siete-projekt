# Bratislavská MHD

## Úvod
Mestská hromadná doprava predstavuje kľúčový prvok verejnej dopravy v mnohých moderných mestách po celom svete. V tomto projekte sa budeme zaoberať rôznymi aspektmi siete tvorenou vybranými zastávkami MHD v meste Bratislava a linkami, ktoré medzi týmito zastávkami premávajú. Cieľom je sa pozrieť na základné štatistické miery siete, výpočet centralit, vyhodnocovanie hustoty siete a podobne. Tieto informácie nám pomôžu odpovedať na niekoľko otázok, ktoré sme si položili. Na to využijeme programovací jazyk Python a knižnicu NetworkX, ktorá umožňujú efektívnu manipuláciu so sieťami a ich analýzu. 

Tu uvádzame niekoľko otázok, na ktoré sa budeme snažiť odpovedať v našom projekte:

1. Ktoré zastávky sú najdôležitejšie v sieti MHD a dôvody prečo sú dôležité? (podľa počtu liniek, ktoré cez ne prechádzajú; či spájajú mestské časti, alebo väčšina z nich je sústredená v jednej časti) 
2. Čo sú slabiny (mosty, artikulácie) v sieti MHD?
3. Aká je priemerná vzdialenosť 2 zastávok (počet zastávok medzi nimi)
4. Ako sa vieme dostať z jednej zastávky do druhej pomocou minimálneho počtu prestupov? 

## Použité dáta

Dáta o prepojenosti zastávok, aktuálne ku 14.4.2024, sme získali scrapovaním zo stránky https://imhd.sk/ba/. Stránka obsahuje linky Bratislavskej MHD spolu so zastávkami v oboch smeroch pre danú linku. Pre jednoduchosť sme použili len linky, ktoré mali číslo menšie ako 200. Linky s číslom nad 200 už zahŕňajú regionálne linky, ktoré obsluhujú obce mimo Bratislavy. Taksito sme nepoužili nočné linky a vlakové spojenia.

Scrapovali sme pomocou pythonovského programu a dáta sme uložili do súboru *linky.txt*. Každý riadok súbor sa začína číslom linky, za ktorým nasleduje postupnosť zastávok, cez ktoré daná linka ide. Keďže niektoré linky majú rozdielne zastávky v opačnom smere, je potrebné uložiť si postupnosť zastávok v oboch smeroch.








Vytvorenie siete Bratislavskej mhd.
Program crawl.py získal linky a zastávky z https://imhd.sk/ba/cestovne-poriadky a uložil ich do súboru linky.txt
linky.txt Je vo formáte číslo linky: zástavka1;zástavka2;zástavka3;....................;zastávkan
Program graph.ipynb načíta súbor linky.txt a vytvorý graf sieti mhd.  Tento graf je orientovaný, lebo existujú medzi zástavkami iba jednosmerné spojenia a je to multigraf, lebo madzi zastávkymi môže premávať viac liniek. Graf je uložený ako 2D slovník, kde graph[zastávka1][zastávka2] = x, zanemá že z prvej zastávky do druhej ide x liniek.
krelsenie grafu.py je program čo vygeneruje náhodný graf a nakrelí ho, vrcholy sú zafarbené podľa spojenosti( alebo centrality už si nie som istý). graf sa otvarí v prehliadači.

link na report https://docs.google.com/document/d/1pHp0rORXtKSpdfbTBlz6ld8ac9qV1hk0nLgn_M13WB4/edit?usp=sharing
link na colab s grafom https://colab.research.google.com/drive/1KxDKzoMGsNsfTO51mOG_hhd-zSiI1w_1?usp=sharing

