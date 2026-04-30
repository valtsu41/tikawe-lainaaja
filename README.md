# tikawe-lainaaja
Tikawe course project | Tikawe-kurssin projekti
## Sovelluksen toiminnot
Sovelluksen perusidea on, että käyttäjät voivat sekä tarjota asioita lainattavaksi, että lainata niitä muilta käyttäjiltä.
- [x] Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- [ ] Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan lainausilmoituksia.
- [x] Käyttäjä näkee sekä omat, että muiden ilmoitukset lainattavista asioista.
- [x] Käyttäjä pystyy hakemaan lainausilmoituksia.
- [ ] Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lainausilmoitukset.
- [ ] Käyttäjä pystyy valitsemaan lainausilmoituksille yhden tai useamman luokittelun.
- [ ] Käyttäjä pystyy lainaamaan toisten käyttäjien ilmoitusten kohteita.
## Sovelluksen käyttäminen
Sovelluksen tietokanta pitää ensin alustaa tietokannan hallintatyökalulla `db_admin.py`.
1. Avaa hallintatyökalu esim. komennolla `python db_admin.py`.
2. Syötä hallintatyökaluun komento `init`.
3. Sulje hallintatyökalu syöttämällä komento `exit`.
Tämän jälkeen varsinaisen sovelluksen saa käynnistettyä komennolla `flask run`.
