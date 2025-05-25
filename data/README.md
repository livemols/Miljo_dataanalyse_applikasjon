# Data
Datafilene her er for det meste samme datasett. 

De originale dataene er i weather.csv og wind.csv og blir kombinert ved hjelp av make_data_files.py. 
Dataen blir deretter "renset" og "skittnet til" i data_cleaning.ipynb. 

Filen vi bruker videre i oppgavene er blindern_data_cleaning.csv som er den originale dataen som i tillegg har gått gjennom rense programmet.

bins.jason er grenser på forskjellige kategorier innefor nedbør og vind. Hentet fra: Meteorologisk institutt. (2017, Mars 21). Begreper i værvarsling. Hentet fra Meteorologisk institutt: https://www.met.no/vaer-og-klima/begreper-i-vaervarsling

## Datasettet
Datasettet vi har tatt utgangspunkt i er data fra Blindern værstasjon (SN18700) fra 1.januar 2014 til og med 31.desember 2024. Værfenomenene vi har tatt utgangspunkt i er maks-, min- og middeltemperatur, snø, nedbør, middelvind og høye vindkast. Det gir oss et godt overblikk over vanlige naturfenomener i Oslo-området og gir oss et godt utgangspunkt for å identifisere fremtidige værmønster senere i oppgaven. 

## Kildekritikk
Datasettet vårt er basert på data fra en nettside som eies av Norsk klimaservicesenter (KSS). KSS er et samarbeid mellom forskjellige organisasjoner: Meteorologisk institutt, Norges vassdrags- og energidirektorat, Kraftverket, NORCE og Bjerknessenteret. Organisasjonene er pålitelige og dataen som er samlet virker realistisk. For vårt spesifikke datasett er Metrologisk institutt kilden til dataen.

Deres data er lett tilgjengelig gjennom en side hvor du får tilgang på værdata. Dette er gjennom å velge forskjellige kategorier som tidsoppløsning, værelementer og værstasjon. Dette bidrar til at nettsiden har god brukervennlighet og gjør det lett å kunne krysseksaminere dataene med en annen kilde. 

Linken til nettsiden er :https://seklima.met.no/observations/
Værdataen vi har hentet fra KSS er originalt fra Metrologisk institutt.

Vi valgte å samle data fra Blindern værsenter siden de hadde for det meste fullstendig data. 
