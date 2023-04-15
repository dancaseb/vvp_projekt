# Projekt do předmětu Vědecké výpočty v Pythonu
Jako projekt jsem si vybral simulaci pohybů planet ve 2D. Tento projekt byl 
vyhotoven v rámci letního semestru 2022/2023 a je napsán v Pythonu.
Zadání projektu nalezneme na konci tohoto readme.

## Implementace
Ve složce planet_project nalezneme zdrojový kód k simulaci. 
V této složce se nachází několik důležitých souborů:
- simulation.py - soubor určený pro spuštení animace, který bude uživatel nejčastěji používat
- universe.py - soubor, ve kterém jsou definované třídy, metody a výpočty sloužící k simulaci pohybu planet
- animation.py - soubor starající se o vykreslování animace
- constans.py - soubor s konstantami

## Použití 

Ve složce data můžeme najít soubory json, ve kterých jsou informace potřebné k vytvoření planet a následné simulaci.
Můžete se podívat na soubor planets.json, který napodobuje naši Sluneční soustavu. 
Každá planeta (mezi planety řadíme i Slunce, protože má stejné atributy jako planety) musí mit definovanou počáteční 
pozici (position), rychlost (velocity), hmotnost (mass) a jméno (name). Tyto hodnoty definujeme v json souborech.

Kód spouštíme z root directory projektu (tedy vvp_planety). Nejdříve si musíme importovat
třídu Simulation. Vytvoříme instanci třídy Simulation, na kterou poté zavoláme metodu run().
Třída Simulation má 1 parametr dt, což je délka časového kroku. Defaultně je nastaven na hodnotu 60\*60\*24 (1 den).
Třídě simulation musíme rovněž zadat parametr path, určující, kde se nachází json soubor s daty našich planet. 
Třída simulation rovněž umožňuje zadat parametr planets_number. V tomto případě se 
vygenerujou planety s náhodnými pozicemi, rychlostmi a hmotnostmi (Nejsou úplně náhodně, snažil jsem
se o menší optimalizaci, aby planety aspoň trochu rotovali kolem sebe.).
Nesmíme zadat současně parametry path a planets_number. Musíme zadat 1 z těchto parametrů. Parametr
dt je povinný vždy.

Při spouštění v jupyter notebooku doporučuji si zapnout jiný matplotlib backend pomocí příkazu
**%matplotlib tk**

Po spuštění metody run se zapne simulaci. Označením levým tlačítkem myší můžeme animaci přiblížit, pravým 
tlačítkem oddálit. Při kliknutí na animaci levým tlačítkem myši animaci pozastavíme a opět můžeme
spustit levým tlačítkem myši.

Po zavření animace se poslední animující objekt uloží do souboru **planets_simulation.mp4**. Uložení trvá asi 
1 minutu a výsledná animace má délku 100 sekund.
Pro uložení animace je potřeba mít nainstalovaný FFMPeg a upravit animation.ffmpeg_path parametr v samém souboru 
(řešení pro windows -_-).

V souboru example.ipynb můžete najít příklady použítí této knihovny.

## Zadání
Tento projekt se zabývá simulací pohybu planet (těles) ve 2D prostoru
(všechny objekty budou mít pro jednoduchost stejnou $z$ souřadnici).
Uvažujeme gravitační interakce mezi každou dvojicí těles v podobě
Newtonova gravitačního zákona $$F_{g}=G\frac{m_{1}m_{2}}{r^{2}},$$ kde
$G=6.674\cdot10^{-11}\left[m^{3}kg^{-1}s^{-2}\right]$ je gravitační
konstanta, $m_{1},m_{2}$ jsou váhy těles a $r$ je vzdálenost mezi nimi.
$F_{g}$ je velikost síly působící mezi dvojicí těles, směr síly je vždy
k druhému tělesu.

Cílem je implementovat numerickou aproximaci řešení pohybových rovnic
planet a vytvoření vizualizace tohoto pohybu. Pro simulaci bude použita
časová diskretizace, přičemž v každém časovém kroku je uvažováno
konstantní zrychlení $a=\frac{F_{g}}{m}$ způsobené gravitační silou
mezi každou dvojicí planet. $a$ je opět pouze velikost zrychlení, směr
je stejný jako směr síly.

Výstupem projektu bude vizualizace pohybu pomocí knihovny Matplotlib,
která zobrazuje pohyb planet v čase a zobrazuje jejich trajektorie.

## Funkcionality
-   načítání počátečních podmínek (polohy,
    rychlosti a hmotnosti) planet z json souboru
-   Vytvořit funkci pro výpočet zrychlení způsobené gravitační silou
    mezi všemi dvojicemi planet
-   Vykreslit aktuální polohy těles v čase
-   Ukládat polohy všech těles v čase pro pozdější vykreslení
    trajektorie
-   Pomocí série obrázků vytvořit animaci pohybu planet, která zobrazuje
    trajektorie a polohy planet v čase
-   Implementovat funkci pro uložení výsledné animace do video souboru
-   Vytvořit funkci pro generování náhodných scénářů simulace, která
    bude náhodně generovat počáteční podmínky planet (polohy, rychlosti
    a hmotnosti)
-   vyzkušet různé délky časového kroku (u planet např. hodina, den, týden, ...) a pozorovat kdy dojde k degradaci simulace 

