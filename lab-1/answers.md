## Lab 1

### 2.1 Forberedelser

-  _Convertion time_ er oppgitt som 12 klokkesykluser. Vi ser også fra figur 1-1 at det tar 3 sykluser fra CS går lav til MSB blir sent på datalinjen. Derfra (inkl. MSB) går det 12 sykluser til all dataen er overført. Det tar altså 15 sykluser å gjøre en sample.
-  Om vi antar at _Vref_ er satt til _Vdd_ så er oppløsningen gitt ved: $$\frac{V_ref}{4096} = 0.80 mV.$$
-  Under maximum ratings kan vi se at vi maksimalt kan gå 0.6V under Vss og 0.6V over Vdd.

-  Vi har ikke kontroll over tidsintervallene som kode vi skriver på CPUen på Pien kjører med, fordi CPUen kjører mange tråder og andre programmer samtidig. DMA håndterer innhenting av data fra ADCene for oss. I starten av et program kan vi initialisere DMAen til å sample data fra ADCene med en bestemt samplingsfrekvens. Målepunktene vil så bli lagret i en buffer. Når denne er full kjøres en interupt slik at programmet vårt kan lese av dataen. Imens vi analyserer det første datasettet fylles en annen buffer opp.
