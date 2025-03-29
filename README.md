# Miljo_dataanalyse_applikasjon

**Gruppe 113 Anvendt programmering**

Intro til oppgaven: 
By: 

Statistikk:

Kilder:
# Prosjektet

### Innholdsfortegnelse:
- Intro
- Kildekritikk
- Data
- Gjennomsnitt 

### Intro:
For å få et godt overblikk over klimautviklingen i Norge har vi sett på værdata for ti år fra værstasjonen blindern (SN18700).

Dataene våre er fra 1.januar 2014 til 31.desember 2024. 


### Kildekritikk:
Datasettet vårt er basert på data fra en nettside som eies av Norsk klimaservicesenter (KSS). KSS er et samarbeid mellom forskjellige organisasjoner: Meterologisk institutt, Norges vassdrags- og energidirektorat, Kraftverket, NORCE og Bjerknessenteret. Organisasjonene er pålitelige og dataen som er samlet virker realistisk. 

Deres data er lett tilgjenelig gjennom en side hvor du får tilgang på værdata. Dette er gjennom å velge forskjellige kategorier som tidsoppløsning, værelementer og værstasjon. Dette bidrar til at nettsiden har god brukervenlighet og gjør det lett å kunne krysseksaminere dataene med en annen kilde. 

Linken til nettsiden er :https://seklima.met.no/observations/
Værdataen vi har hentet fra KSS er originalt fra Metreologisk institutt.

Vi valgte å samle data fra Blindern værsenter siden de hadde for det meste fullstendig data. 

### Data:
Datasettet vårt som ble hentet fra KSS hadde få feil. Den største feilen var at noen av snødybdeværdiene ikke var målt i sommermånedene. Man kan lett konkludere med at hvis snødybden hadde blitt målt ville dybden være 0cm, men for å gjøre programmet uavhenngig av gode data måtte vi gjøre om på det. Ved å bruke interpolate fant vi mulige verdier for manglende data. 




