# Verden på Norsk

Steg:


## Datasett
1. Sjekk om alle er i metadata
2. Sjekk om alle er i DHLAB
3. Få URN fra mdb
4. Test wikidata extraction
5. Wikidata alternativer?

## Kartapp
???

## Korpusapp


## Kommentar fra Oddrun
Ja, dette var en veldig knapp post, ingen andre clues her. Sikkert noen som har tenkt at den oversatte tittelen er den samme som originaltittelen, så da trenger vi ikke å registrere den 

Og nei, alle har ikke opplysninger om originalspråk. 

 

For å fange opp alle potensielle norske oversettelser, tror jeg man må bruke flere kriterier.  

Indikasjoner på at vi har en norsk oversettelse: 

Språket i ressursen vi ser på er norsk: 041$a og/eller Leader[35-37] inneholder 'nno', 'nob' eller 'nor' 
OG minst ett av følgende:
041$h (originalspråk) er noe annet enn norsk
246$i 'Originaltittel:'  finnes
700$i 'Oversettelse av:' finnes
700$a<>$4 'trl' finnes
700$a<>$e 'overs.' finnes
765 finnes (brukes ikke så mye)

Grunnen til alle disse kriteriene er at det har  vært ulike katalogiseringspraksiser opp gjennom tiden.  Nå er det 700/710/711 som skal brukes til å uttrykke verket (med originaltittel), men det er ganske nytt. 

Når settet med kandidater er funnet, få man analysere videre ut fra dette (da kan evt. notefeltene 534 of 546 inneholde info (i tekst)), og bestemme videre strategi for å finne originalutgavene.

Er det MODS du vanligvis bruker for metadata? I dette tilfellet tror jeg det er best å bruke Marc21, da man må se på spesifikke delfelt. 

Jeg har forsåvidt muligheten for å ekstrahere en initiell kandidatliste basert på ovenstående, hvis du er interessert. Tipper at det holder å bruke norbok (postene med 913$aNorbok) som grunnlagssett for dette.

## Kommentar 2
Å finne oversettelsene til norsk tror jeg skal la seg gjøre, med originaltittel. Men for å finne origialutgaven/ landet må man antakelig bruke ulike strategier avh. Av hvilket land. Men store baser som f eks lc, BL og DnB er muligens bra å starte med. Og worldcat (oclc), som du var inne på. Samt autoritetsregisteret/viaf/inni hvis man trenger info om opphavspetsoner og hvor de kommer fra...