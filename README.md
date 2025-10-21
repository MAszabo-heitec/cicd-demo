# Demo: Python Flask CI/CD pipeline

Ez a mappa egy egyszerű Python/Flask alkalmazást és a hozzá tartozó GitHub Actions CI/CD pipeline‑t tartalmazza. A példa bemutatja, hogyan építhetünk, tesztelhetünk és telepíthetünk egy konténerizált alkalmazást teljesen automatizált módon. A projekt most már tartalmaz egy `/info` végpontot, amely visszaadja az alkalmazás verzióját és a környezetet az image‑be épített környezeti változókból.

## Fájlok

- `app/main.py` – minimális Flask alkalmazás, amely a gyökér útvonalon „Hello, CI/CD!” üzenetet ad vissza.
    - A `/info` végpont JSON‑t ad vissza a `version` és `environment` mezőkkel, amelyek az image‑be épített környezeti változókat (`APP_VERSION`, `ENVIRONMENT`) tükrözik.
- `requirements.txt` – a projekt Python‑függőségei.
- `test/test_app.py` – egyszerű unit teszt a Flask alkalmazás ellenőrzésére `pytest` segítségével.
- `Dockerfile` – multi‑stage Docker build: az első szakaszban telepítjük a függőségeket, a végső image pedig csak a futtatáshoz szükséges komponenseket tartalmazza.
    - Build argumentumok (`APP_VERSION`, `ENVIRONMENT`) használatával testreszabható a verzió és környezet. Ezeket `ENV` változóként definiáljuk, így az alkalmazás képes a /info végpontban megjeleníteni őket.
- `.github/workflows/ci.yml` – GitHub Actions workflow, amely épít, tesztel, sebezhetőségi scan‑t futtat, majd a main branch esetén pusholja az image‑t egy registry‑be (a példában Docker Hub‑ra).

## Használat

1. **Futtatás helyileg**:
   ```bash
   python3 -m venv venv
   . venv/bin/activate
   pip install -r requirements.txt
   python app/main.py
   # nyisd meg a http://localhost:5000 címet a böngészőben
   ```

2. **Teszt futtatása**:
   ```bash
   pip install -r requirements.txt
   pip install pytest
   pytest
   ```

3. **Docker build**:
   ```bash
   docker build -t yourrepo/hello-cicd:latest .
   docker run -p 5000:5000 yourrepo/hello-cicd:latest
   ```

4. **GitHub Actions**: tedd fel a repository‑t GitHub‑ra, állítsd be a Secrets (pl. `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`), majd pushold. A workflow automatikusan futni fog pull request esetén (build + teszt) és a `main` branchre történő push esetén (build + teszt + security scan + push + deploy).

Ez a demonstráció segít megérteni a CI/CD pipeline működését valós példán keresztül, beleértve a multi‑stage buildet, a tesztelést, a sebezhetőségi vizsgálatot és a konténer image publikálását.