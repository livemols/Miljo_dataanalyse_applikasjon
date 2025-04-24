
Filene i denne mappen tar for seg datahåndtering.

combine_files.py kombinerer to filer med data med samme start- og sluttdato (weather.csv og wind.csv). Dette er fordi det er maks fem værelementer for hver CSV-fil fra Norsk klimaservicesenter (https://seklima.met.no/observations/). 

Siden datasettet ikke inneholder mange feil, er det ikke "nødvendig" å rense datasettet. Men for å gjøre programmet mer universelt bestemte vi oss for å rense dataen uansett med data_cleaning. Vi lagde også et datasett som fikk flere genererte feil (dirty_data_generator.py), for å vise at rensingen fungerte. 

month_average.py regner ut det månedlige gjennomsnittet for hver av kolonnene. Altså gjennomsnittet av måneden over de ti årene datasettet er for. 
