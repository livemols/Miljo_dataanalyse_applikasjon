# Data forberedelse
Filene i denne mappen lager klassene for datahåndtering og rensing, som blir brukt i flere notebooks. 

##### data_cleaning.py:
Siden datasettet ikke inneholder mange feil, er det ikke "nødvendig" å rense datasettet. Men for å gjøre programmet mer universelt bestemte vi oss for å rense dataen uansett med *[data_cleaning](./data_cleaning.py)*. Denne filen blir brukt i forbindelse med data_cleaning.ipynb i notebooks-mappen
 

 ##### make_data_files.py:
*[make_data_files](./make_data_files.py)* kombinerer to filer med data med samme start- og sluttdato (weather.csv og wind.csv). Dette er fordi det er maks fem værelementer for hver CSV-fil fra Norsk klimaservicesenter (https://seklima.met.no/observations/). Filen lager også et datasett som fikk flere genererte feil, for å vise at rensingen fungerte. De lagrende filene ligger under data-mappen, og filen blir brukt i forbindelse med data_cleaning.ipynb. 


