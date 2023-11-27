# Simple Unit (implémentation Python)

[![Anaconda-Server Badge](https://anaconda.org/cosmoloj/unit_simple/badges/version.svg)](https://anaconda.org/cosmoloj/unit_simple)
[![PyPI repository Badge](https://badge.fury.io/py/unit_simple.svg)](https://badge.fury.io/py/unit_simple)

## Mettre à jour l'environnement

```commandline
conda env update --file environment.yml
# ou bien simplement sans faire mention du fichier de conf Conda environment.yml implicite :
conda env update
# ou bien encore, pour supprimer les dépendances absentes du fichier d'environnement :
conda env update --prune --file environement.yml
# ou bien plus implement :
conda env update --prune
# ou bien pour forcer la suppression des dépendances :
conda env create --force
```

Pour mettre à jour l'environnement de dev (test, linter…):

```commandline
conda env create --force environment.dev.yml
```

## Utilisation

Utilisation des unités transformées :

```py
import unit_simple as su

m = su.FundamentalUnit()
km = m.scale_multiply(1000)
cm = m.scale_divide(100)
cmToKm = cm.get_converter_to(km)

cmToKm.convert(3) # 0.00003
cmToKm.inverse().convert(0.00003) # 3
```

Utilisation des unités dérivées :

```py
import unit_simple as su

m = su.FundamentalUnit()
km = m.scale_multiply(1000)

km2 = su.DerivedUnit(km.factor(2))
cm = m.scale_divide(100)
cm2 = su.DerivedUnit(cm.factor(2))
km2Tocm2 = km2.get_converter_to(cm2)

km2Tocm2.convert(3) # 30000000000
km2Tocm2.inverse().convert(30000000000) # 3
```

Utilisation des unités dérivées en combinant les dimensions :

```py
import unit_simple as su

m = su.FundamentalUnit()
kg = su.FundamentalUnit()
g = kg.scale_divide(1000)
ton = kg.scale_multiply(1000)
gPerM2 = su.DerivedUnit(g, m.factor(-2))
km = m.scale_multiply(1000)
tonPerKm2 = su.DerivedUnit(ton, km.factor(-2))
cm = m.scale_divide(100)
tonPerCm2 = su.DerivedUnit(ton, cm.factor(-2))
gPerM2ToTonPerKm2 = gPerM2.get_converter_to(tonPerKm2)
gPerM2ToTonPerCm2 = gPerM2.get_converter_to(tonPerCm2)

gPerM2ToTonPerKm2.convert(1) # 1
gPerM2ToTonPerKm2.inverse().convert(3) # 3
gPerM2ToTonPerCm2.convert(1) # 1e-4
gPerM2ToTonPerCm2.convert(3) # 3e-10
gPerM2ToTonPerCm2.offset() # 0.0
gPerM2ToTonPerCm2.scale() # 1e-10
gPerM2ToTonPerCm2.inverse().offset() # -0.0
gPerM2ToTonPerCm2.inverse().convert(3e-10) # 3
```

Utilisation des températures (conversions affines et linéaires) :

```py
import unit_simple as su

k = su.FundamentalUnit()
c = k.shift(273.15)
kToC = k.get_converter_to(c)

kToC.convert(0) # -273.15
kToC.inverse().convert(0) # 273.15

# en combinaison avec d'autres unités, les conversions d'unités de températures doivent devenir linéaires
m = su.FundamentalUnit()
cPerM = su.DerivedUnit(c, m.factor(-1))
kPerM = su.DerivedUnit(k, m.factor(-1))
kPerMToCPerM = kPerM.get_converter_to(cPerM)

kPerMToCPerM.convert(3) # 3
kPerMToCPerM.inverse().convert(3) # 3
```

Utilisation des conversions non décimales :

```py
import unit_simple as su

m = su.FundamentalUnit()
km = m.scale_multiply(1000.)

s = su.FundamentalUnit()
h = s.scale_multiply(3600.)

ms = su.DerivedUnit(m, s.factor(-1))
kmh = su.DerivedUnit(km, h.factor(-1))

msToKmh = ms.get_converter_to(kmh)

msToKmh.convert(100.) # 360
msToKmh.inverse().convert(18.) # 5
```