# Retrospektiivien muistiinpanot

## Ensimmäinen sprintti

Toteutimme retrospektiivin heti ensimmäisen asiakastapaamisen jälkeen Start, Stop, Continue, More of, Less of Wheel tekniikalla. Kirjoitimme sprintin aikana esiin tulleita asioita ja ongelmia kehälle, keskustelimme niistä, sekä siitä miten voimme jatkossa toimia niiden
kannalta järkevämmin.

Yhtenä isoimpana huomiona tuli esiin pitää ryhmäläiset tarkalleen kartalla siitä mitä on projektiin tehnyt ja mitä aikoo tehdä tai on työn alla, sillä
rajallisen työajan ja kasvotusten näkemisen takia muiden on vaikea hahmottaa mitä todellisuudessa yhden työntekijän tietokoneella tapahtuu. Tähän liittyen ilmeni myös paremman aikataulutuksen tarve projektille, joka osaltaan helpottaa ensimmäistä ongelmaa.

Toisena isona huomiona tuli definition of donen täsmällinen noudattaminen ja sitä kautta myös pienempien kokonaisuuksien toteuttaminen kerralla.
Muun tiimin on vaikea jatkaa töitä jos 3 testiä on rikki ja pylint varoituksia on 5. Retrospektiivin aikana ilmeni myös tarve käyttää aikaa enemmän tekniseen suunnitteluun
tiimin kesken sprintin suunnittelun aikana, jotta ollaan paremmin kartalla siitä mitä lähdetään tekemään. Retrospektiiviin kului aikaa yhteensä noin 25 minuuttia.

## Toinen sprintti

Pidimme toisen sprintin retrospektiivin heti toisen asiakastapaamisen jälkeen. Käytimme Start, Stop, Continue, More of, Less of Wheel -tekniikkaa, kuten ensimmäisessä retrospektiivissä. Koska tekniikka oli meille tuttu, retrospektiivin aloittaminen oli helpompaa kuin viime kerralla. Keskustelimme sekä hyvin sujuneista asioista että mahdollisista kehityskohdista käyttäen apuna viisisektorista ympyrää, johon kirjasimme ajatuksia ylös. Esiin nousi kaksi kehitystoimenpidettä, joihin haluamme erityisesti panostaa kolmannessa sprintissä.

Ensimmäinen kehitystoimenpide on, että pushaamme GitHubiin vain toimivaa ja testit läpäisevää koodia. Tämän saavuttamiseksi sovimme, että ennen koodin pushaamista tarkistamme, että sovellus toimii ja ajamme paikallisesti Robot- ja yksikkötestit sekä PyLintin.

Toinen kehitystoimenpide on, että toteutamme riittävän pieniä osia sovelluksesta kerrallaan. Näin voidaan helpottaa eri osien toteuttamiseen kuluvan ajan arvioimista ja välttää pullonkaulat, joissa usean osan eteneminen on yhdestä ryhmäläisestä kiinni. Tämän saavuttamiseksi panostamme kolmannessa sprintissä riittävän pienten taskien suunnitteluun.

Muita retrospektiivissä esiin nousseita asioita olivat mm. aikaisempi tapaamisajankohta ryhmän kesken ennen asiakastapaamista, backlogin ahkerampi päivittäminen sekä parikoodaus. Käytimme retrospektiiviin aikaa noin 30 minuuttia.

## Kolmas sprintti

Jatkoimme kolmannessa retrospektiivissä Start, Stop, Continue, More of, Less of -pyörän käyttämistä. Tällä kertaa reflektoitavaa tuntui olevan vähemmän, kuin edellisillä kerroilla.

Koimme, että olimme onnistuneet hyvin edellisessä retrossa sovituissa kehitystoimenpiteissä. Olimme onnistuneet myös tällä kertaa jaotella user storyt huomattavasti pienempiin taskeihin, kuin ensimmäisien sprinttien aikana. CI-putki meni kolmannen sprintin aikana rikki huomattavasti harvemmin kuin kahden ensimmäisen sprintin aikana.

Sovimme tulevaan sprintiin tavoitteeksemme, että saisimme työn aikasemmin aikaseksi kuin kolmannessa sprintissä. Yritämme toteuttaa kaikki sprintin user storyt ja projektin ylläpidolliset asiat tiistai-iltaan mennessä vaikka lopullinen määräaika on torstaiaamu, kun osallistumme loppudemoon. Lisäksi poimimme viimeisen sprintin arvosteluperusteista tavoitteen, että commit-viestit olisivat yhtenäiset. Kirjoitamme vastaisuudessa commitit näin:

- englanniksi
- imperatiivi-muoto isolla alkukirjaimella
- mahdollisimman ytimekäs, yleensä alle 50 merkkiä
- esimerkiksi:

<pre>
Add "Save" button to front page
</pre>

