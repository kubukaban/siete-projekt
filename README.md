Vytvorenie siete Bratislavskej mhd.
Program crawl.py získal linky a zastávky z https://imhd.sk/ba/cestovne-poriadky a uložil ich do súboru linky.txt
linky.txt Je vo formáte číslo linky: zástavka1;zástavka2;zástavka3;....................;zastávkan
Program graph.ipynb načíta súbor linky.txt a vytvorý graf sieti mhd.  Tento graf je orientovaný, lebo existujú medzi zástavkami iba jednosmerné spojenia a je to multigraf, lebo madzi zastávkymi môže premávať viac liniek. Graf je uložený ako 2D slovník, kde graph[zastávka1][zastávka2] = x, zanemá že z prvej zastávky do druhej ide x liniek.
