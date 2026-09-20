Sovelluksessa voi tallentaa päivän aikana syötyjä annoksia niiden sisältämiä makroja ja reseptejä.

Sovelluksen ominaisuuksia ovat:

-Sovellukseen pystyy myös kirjautua sisään ja ulos.

-Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan annoksia.

-Käyttäjä pystyy lisäämään reseptejä annoksiin.

-Kirjautuessa näkee tallennetut annokset, dataa makrojen määrästä ja suosituksia lähitulevaisuuteen.

-Käyttäjä voi hakea dataa valitsemansa aikajakson perusteella.

-Annosnäkymästä voi lisätä annoksiin raaka-aineita ja makroja.

-Tekoäly web käyttöliittymä mm. reseptien suosituksiin tallennetun datan pohjalta.

## Välipalautus 2

- Käyttäjä voi kirjautua, rekisteröityä ja hallita omaa profiiliaan.
- Etusivulla on haku, jolla voi löytää annoksia nimen, hinnan ja tyypin perusteella.
- Käyttäjä voi lisätä, muokata ja poistaa omia annoksia sekä tarkastella niiden tietoja.
- Aterioiden hinta ja makrot näkyvät helposti käyttöliittymässä.
- Sovellus käyttää SQLite-tietokantaa ja ylläpitää käyttäjäkohtaisia annoksia.
- Profiilisivulla on mahdollista vaihtaa salasana ja poistaa tili.
- Olin ottanut huomioon ensimmäisen välipalautuksen palautteen ja yritän tehdä sovelluksesta kurssin mukaisen.
- Aihe on vielä elävä ja projekti saattaa muuttua reseptipankiksi tulevaisuudessa.
- Repo saattaa vielä sisältää kurssin harjoitusmateriaalin testaamisesta jääneitä lomakkeita ja toimintoja. Nämä siivotaan pois seuraavaan välipalautukseen mennessä.

## Kuinka sovellusta testataan toisella koneella

1. Kopioi projekti toiselle koneelle GitHubista tai zip-tiedostona.
2. Voit myös kloonata repon komennolla:
   ```bash
   git clone https://github.com/tomppaaa/tikawe-test.git
   ```
3. Avaa terminaali projektin juurihakemistoon.
4. Varmista, että Python 3 on asennettu.
5. Asenna tarvittavat riippuvuudet:
   ```bash
   python3 -m pip install flask
   ```
6. Varmista seuraavat asiat:
   - "init.sql" sijaitsee samassa kansiossa kuin "db.py".
   - "database.db"-tiedostoa ei tarvitse luoda itse. Sovellus suorittaa "init.sql"-tiedoston automaattisesti käynnistyessään ja luo kaikki tietokannan taulut.
7. Käynnistä sovellus:
   ```bash
   python3 app.py
   ```
8. Avaa selaimessa osoite http://127.0.0.1:5000.
9. Testaa sovellusta:
   - Luo tili ja kirjaudu sisään.
   - Testaa annosten lisäämistä, muokkaamista, poistamista, hakua ja profiilin hallintaa.
10. Jos haluat aloittaa puhtaalla tietokannalla, pysäytä sovellus, poista "database.db" ja käynnistä sovellus uudelleen:
    ```bash
    rm database.db
    python3 app.py
    ```

