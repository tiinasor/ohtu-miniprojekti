## Ohtu miniprojekti

[![CI](https://github.com/tiinasor/ohtu-miniprojekti/actions/workflows/ci.yaml/badge.svg)](https://github.com/tiinasor/ohtu-miniprojekti/actions/workflows/ci.yaml)

[![codecov](https://codecov.io/github/tiinasor/ohtu-miniprojekti/graph/badge.svg?token=HZXVDE5V7V)](https://codecov.io/github/tiinasor/ohtu-miniprojekti)

[Product ja sprint backlog](https://docs.google.com/spreadsheets/d/1mSdKyYM1908SzdmZ8wrdTdeK1SKqvMYnkV53-zhKxrM/edit?gid=1#gid=1)

[Final Report](https://github.com/tiinasor/ohtu-miniprojekti/blob/main/report.md)

## Definition of done

Vaatimus on analysoitu, suunniteltu, ohjelmoitu, testattu, testaus automatisoitu ja integroitu muuhun ohjelmistoon.

## Asennus
Tässä vaiheessa oletetaan, että jokin Python-versio (3.12+) ja sen kanssa yhteensopiva Poetry-versio ovat asennettuina.

Aloitetaan luomalla `.env`-tiedosto ympäristömuuttujia varten:
```
DATABASE_URL=postgresql://xxxxx
TEST_ENV=true
SECRET_KEY=satunnainen_merkkijono
```

Tämän jälkeen asennetaan projektin riippuvuudet:
```
$ poetry install
```

## Käynnistys
Käynnistyksen helpottamiseksi siirrytään ensin virtuaaliympäristöön:
```
$ eval $(poetry env activate)
```

Ennen ensimmäistä käynnistystä on myös tärkeää, että tietokanta alustetaan:
```
$ python src/db_helper.py
```

Nyt projekti voidaan käynnistää:
```
$ python src/index.py
```

Yksikkötestit voidaan suorittaa komennolla:
```
$ pytest src/tests
```

Robot-testit voidaan suorittaa komennolla:
```
$ robot src/story_tests
```
