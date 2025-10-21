Complex CI/CD Demo
===================

Ez a projekt egy összetettebb Python Flask alkalmazás, amely több API végpontot és egy dinamikus weboldalt valósít meg.  A célja, hogy bemutassa, hogyan lehet egy több lépcsős CI/CD folyamatot felépíteni GitHub Actions segítségével úgy, hogy semmilyen titkos adat (secret) ne legyen szükséges.  A rendszer része továbbá egy statikus dokumentációs oldal, amelyet a `mkdocs` épít és a GitHub Pages szolgáltatás publikál.

Fő funkciók
-----------

- **Webfelület**: a gyökér (`/`) útvonal egy HTML oldalt ad vissza, ahol megjelenik az alkalmazás verziója, a commit SHA és egy véletlen szám, amelyet az API-ból tölt be JavaScripttel.
- **API végpontok**:
  - `GET /api/random`: egy 0 és 100 közötti véletlen számot ad vissza.
  - `GET /api/time`: az aktuális UTC időt ISO‑8601 formátumban adja vissza.
  - `GET /api/calc/<a>/<b>`: összeadja az `a` és `b` paramétereket és JSON-ben küldi vissza.
  - `GET /api/info`: metaadatokat ad vissza (`version`, `commit`, `environment`).
  - `GET /api/health`: az alkalmazás egészségi állapotát jelzi.
- **Dinamikus commit megjelenítés**: a commit SHA és a verzió környezeti változókon keresztül kerül az oldalba, ezáltal minden újabb `push` láthatóan frissíti a weboldalt és a dokumentációt is.
- **Docker**: a multi‑stage Dockerfile hatékonyan építi fel az alkalmazást egy vékony runtime image‑be.
- **Dokumentáció**: a projekt tartalmaz egy `docs` mappát és `mkdocs.yml` konfigurációt.  A GitHub Actions a `main` branche‑re történő push alkalmával építi a statikus weboldalt a commit SHA beszúrásával, majd publikálja azt GitHub Pages‑en.

Mappastruktúra
--------------

    demo_cicd_complex/
    ├── app/                 # Flask alkalmazás
    │   ├── __init__.py
    │   ├── main.py
    │   └── templates/
    │       └── index.html
    ├── docs/                # mkdocs tartalom
    │   ├── index.md
    │   └── about.md
    ├── test/
    │   └── test_app.py      # unit tesztek
    ├── .github/workflows/   # GitHub Actions workflow definíciók
    │   ├── ci-pr.yml
    │   ├── ci-dev.yml
    │   └── ci-main.yml
    ├── Dockerfile           # többfázisú build
    ├── requirements.txt     # futásidejű függőségek
    └── mkdocs.yml           # mkdocs konfiguráció

Lokális futtatás
---------------

1. Telepítsd a Python függőségeket:

        python -m pip install -r requirements.txt

2. Indítsd el az alkalmazást:

        python -m app.main

3. Nyisd meg a böngészőben: [http://localhost:5000](http://localhost:5000).

Tesztelés
---------

Futtasd az egységteszteket a következő paranccsal:

        pytest -q

CI/CD áttekintés
----------------

Három különálló GitHub Actions workflow szolgálja a minőségbiztosítást és a build/deploy folyamatokat:

1. **PR CI (`ci-pr.yml`)**: Minden pull request nyitásakor vagy frissítésekor fut.  Egységteszteket és kódban futtatott statikus analízist (flake8) végez, így már az egyes PR-eknél kiszűri a hibákat.
2. **Dev Build & Audit (`ci-dev.yml`)**: A `dev` branch-re érkező pusht indítja.  Futnak a tesztek, a `pip-audit` függőség ellenőrzés, a `flake8` lint és a Docker image építése is.  Így a fejlesztői ágon már korán kiderülnek a problémák.
3. **Main Release & Pages (`ci-main.yml`)**: A `main` ágra történő push esetén fut.  Teszteket és statikus elemzéseket futtat (`flake8`, `bandit`), megépíti a Docker image‑et, majd `mkdocs` segítségével statikus oldalt generál a `docs` mappából, beleírja a friss commit SHA‑t, feltölti egy artefaktként és a végén a GitHub Pages szolgáltatásra publikálja.  Ez a GitHub Pages site mindig a `main` branch legutóbbi commitját jeleníti meg.

Ezek a folyamatok secretek nélkül működnek: a GitHub által biztosított token és runner környezet elegendő a buildhez és a Pages deployhoz.