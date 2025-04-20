
# Gruppe 113: Anvendt programmering

### Innholdsfortegnelse:
 - Intro
 - Oppgave fordeling
 - Data
 - Kildekritikk

## Intro
Oppgaven går ut på å utvikle et program som henter, analyserer og visualiserer værdata. Da kan man få innsikt i værmønstre og kan identifisere fremtidige værmønster. I del 1 skal man sortere, rense og forberede datasettet til videre utvikling. Mens i del 2 skal man analysere og visualisere datasettet. 

## Oppgave oppsett
Hovedoppgaven er delt inn i del 1 og del 2. 
Del 1 består av filene:
- Notatbøkene:
    - data_cleaning.ipynb
    - data_understanding.ipynb
- src (data_preperatiron):
    - combine_files.py
    - data_cleaning.py
    - dirty_data_generator.py
    - month_average.py

Del 2 består av filene: 
- Notatbøkene:
    - data_analysis.ipynb
    - data_visual.ipynb
    - predictive_analysis.ipynb
    - Refleksjonsnotat.ipynb
- src (modelling):
    - data_analysis.py
    - missing_values.py

## Data
Datasettet vi har tatt utgangspunkt i er data fra Blindern værstasjon (SN18700) fra 1.januar 2014 til og med 31.desember 2024. Værfenomenene vi har tatt utgangspunkt i er maks-, min- og middeltemperatur, snø, nedbør, middelvind og høye vindkast. Det gir oss et godt overblikk over vanlige naturfenomener i Oslo-området og gir oss et godt utgangspunkt for å identifisere fremtidige værmønster senere i oppgaven. 

## Kildekritikk
Datasettet vårt er basert på data fra en nettside som eies av Norsk klimaservicesenter (KSS). KSS er et samarbeid mellom forskjellige organisasjoner: Meteorologisk institutt, Norges vassdrags- og energidirektorat, Kraftverket, NORCE og Bjerknessenteret. Organisasjonene er pålitelige og dataen som er samlet virker realistisk. For vårt spesifikke datasett er Metrologisk institutt kilden til dataen.

Deres data er lett tilgjengelig gjennom en side hvor du får tilgang på værdata. Dette er gjennom å velge forskjellige kategorier som tidsoppløsning, værelementer og værstasjon. Dette bidrar til at nettsiden har god brukervennlighet og gjør det lett å kunne krysseksaminere dataene med en annen kilde. 

Linken til nettsiden er :https://seklima.met.no/observations/
Værdataen vi har hentet fra KSS er originalt fra Metrologisk institutt.

Vi valgte å samle data fra Blindern værsenter siden de hadde for det meste fullstendig data. 

