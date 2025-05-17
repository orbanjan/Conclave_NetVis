# Conclave Network Analysis

Ez a projekt a bíborosok közötti kapcsolatok hálózati elemzését végzi el. A projekt négy fő Python fájlból áll:

## 1. conclave_generate.py
Ez a fájl felelős a hálózat generálásáért:
- Betölti a bíborosok adatait a `data/cardinals.csv` fájlból
- Automatikusan meghatározza a kontinenseket az országok alapján
- Létrehoz egy súlyozott hálózatot, ahol:
  - A csomópontok a bíborosok
  - Az élek a bíborosok közötti kapcsolatokat jelölik
  - A súlyok a kapcsolatok erősségét mutatják (pl. ugyanaz a pápa, ugyanaz a konsisztórium, stb.)
- Exportálja a hálózatot `edges.csv` és `nodes.csv` formátumban

## 2. cluster_analysis.py
Ez a fájl végzi a közösségi elemzést:
- Betölti a generált hálózatot
- Kiszámítja az alapvető hálózati jellemzőket (átmérő, átlagos fokszám, stb.)
- Közösségi detektálást végez a Louvain módszerrel
- Elemzi a közösségek jellemzőit (méret, átlagéletkor, CB arány, stb.)
- Létrehoz négy vizualizációs fájlt:
  - `community_sizes.png`: Közösségek mérete
  - `community_characteristics.png`: Közösségek jellemzői
  - `community_correlations.png`: Korrelációs mátrix
  - `network_visualization.png`: Hálózat vizualizáció

## 3. network_analysis.py
Ez a fájl a hálózat részletes elemzését végzi:
- Hálózati metrikák számítása
- Közösségi detektálás
- Vizualizációk generálása
- Statisztikák készítése

## 4. conclave_analysis.py
Ez a fájl a bíborosok adatainak elemzését végzi:
- Demográfiai elemzés
- Országok és kontinensek eloszlása
- Életkor és rang szerinti elemzés
- Statisztikák és vizualizációk készítése

## Telepítés

A projekt futtatásához szükséges csomagok:
```bash
pip install pandas networkx python-louvain matplotlib seaborn numpy scikit-learn pycountry pycountry-convert
```

## Használat

1. Először futtasd a `conclave_generate.py` fájlt a hálózat generálásához:
```bash
python conclave_generate.py
```

2. Ezután futtasd a `cluster_analysis.py` fájlt a közösségi elemzéshez:
```bash
python cluster_analysis.py
```

3. Opcionálisan futtathatod a `network_analysis.py` és `conclave_analysis.py` fájlokat további elemzésekhez.

## Kimenetek

A program több vizualizációs fájlt és CSV-t generál:
- `edges.csv`: A hálózat élei
- `nodes.csv`: A hálózat csomópontjai
- Különböző PNG fájlok a vizualizációkhoz
- Statisztikai összefoglalók a konzol kimenetében

