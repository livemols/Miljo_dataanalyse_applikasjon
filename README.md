
# Gruppe 113: Anvendt programmering

### Innholdsfortegnelse:
 - Intro
 - Data
 - Kildekritikk
 - 

## Intro
Oppgaven går ut på å utvikle et program som henter, analyserer og visulariserer værdata. Da kan man få innsikt i værmønstre og kan identifisere fremtidige værmønster. I del 1 skal man sortere, rense og forberede datasettet til videre utvikling. Mens i del 2 skal man analysere og visualisere datasettet. 


## Data
Datasettet vi har tatt utgangspunkt i er data fra blinern værstasjon (SN18700) fra 1.januar 2014 til og med 31.desember 2024. Værfenomenene vi har tatt utgangspunkt i er maks- og mintemperatur, middelvind, nedbør og snødybde. Det gir oss et godt overblikk over de vanlige naturfenomene i Oslo-området og gir oss et godt utgangspunkt for å identifisere fremtidige værmønster senere i oppgaven. 


## Kildekritikk
Datasettet vårt er basert på data fra en nettside som eies av Norsk klimaservicesenter (KSS). KSS er et samarbeid mellom forskjellige organisasjoner: Meterologisk institutt, Norges vassdrags- og energidirektorat, Kraftverket, NORCE og Bjerknessenteret. Organisasjonene er pålitelige og dataen som er samlet virker realistisk. For vårt spesifike datasett er Metrologisk institutt kilden til dataen.

Deres data er lett tilgjenelig gjennom en side hvor du får tilgang på værdata. Dette er gjennom å velge forskjellige kategorier som tidsoppløsning, værelementer og værstasjon. Dette bidrar til at nettsiden har god brukervenlighet og gjør det lett å kunne krysseksaminere dataene med en annen kilde. 

Linken til nettsiden er :https://seklima.met.no/observations/
Værdataen vi har hentet fra KSS er originalt fra Metreologisk institutt.

Vi valgte å samle data fra Blindern værsenter siden de hadde for det meste fullstendig data. 


Datasettet vårt som ble hentet fra KSS hadde få feil. Den største feilen var at noen av snødybdeværdiene ikke var målt i sommermånedene. Man kan lett konkludere med at hvis snødybden hadde blitt målt ville dybden være 0cm, men for å gjøre programmet uavhenngig av gode data måtte vi gjøre om på det. Ved å bruke interpolate fant vi mulige verdier for manglende data. 




