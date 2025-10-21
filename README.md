# Demo: CI/CD pipeline három különálló GitHub Actions workflow-val

Ez a mappa egy egyszerű Python/Flask alkalmazást tartalmaz, amely többféle CI/CD workflow-t demonstrál. A cél, hogy a GitHub Actions használata során semmilyen felhasználói secretre ne legyen szükség: minden lépés a GitHub által nyújtott alapértelmezett környezetben fut. Három különböző workflow található a `.github/workflows` mappában, amelyek eltérő eseményekre reagálnak.

## Főbb jellemzők

- **Egyszerű Flask alkalmazás** két végponttal: a gyökér (`/`) „Hello, CI/CD!” üzenetet küld vissza, a `/info` pedig JSON formátumban adja meg az `APP_VERSION` és `ENVIRONMENT` környezeti változókat.
- **Multi-stage Docker build**: a Dockerfile két szakaszban építi az image-et. Az `ARG` direktívákkal megadható a verzió és a környezet, de ezek alapértelmezett értékeket tartalmaznak, így a build paraméterek megadása nem kötelező.
- **Nincs szükség secretekre**: az összes workflow úgy van felépítve, hogy ne használjon kézi bevitelű tokeneket vagy jelszavakat. Az egyetlen automatikusan elérhető token a `GITHUB_TOKEN`, ami a GitHub API hívásokhoz használható, de a demonstrációban erre sincs szükség.

## Workflow-k

1. **Pull Request (CI) – `.github/workflows/ci-pr.yml`**

   - **Trigger**: bármilyen pull request (`pull_request`) a repository bármely branchéről.
   - **Lépések**: kód checkout, Python telepítés, függőségek telepítése, unit tesztek futtatása pytest-tel. Célja a fejlesztők visszajelzése a merge előtt.

2. **Fejlesztői build & audit – `.github/workflows/ci-dev.yml`**

   - **Trigger**: push a `dev` branchre.
   - **Lépések**: kód checkout, Python telepítése, függőségek és kiegészítő eszközök (pytest, pip-audit) telepítése, unit tesztek futtatása, a `pip-audit` eszköz lefuttatása a `requirements.txt` fájl ellen, végül egy Docker image építése. A build paraméterek alapértelmezett értékeket használnak.

3. **Főágbeli release build – `.github/workflows/ci-main.yml`**

   - **Trigger**: push a `main` branchre.
   - **Lépések**: checkout, Python telepítése, függőségek telepítése, unit tesztek futtatása, egy docker image építése, a `bandit` statikus kódanalizáló futtatása a `app/` mappán, az image fájlba mentése (`docker save`), majd annak feltöltése artefaktumként. A feltöltött artefakt a GitHub Actions felületéről letölthető.

Ezek a workflow-k példát adnak arra, hogyan különíthetjük el a különböző pipeline-fázisokat branch vagy esemény alapján, mindezt úgy, hogy a futtatáshoz nincs szükség extra secretekre.

## Fájlok

- `app/main.py` – Flask alkalmazás a `/` és a `/info` végpontokkal.
- `requirements.txt` – a Python-függőségek listája.
- `test/test_app.py` – unit tesztek pytest-tel a végpontokhoz.
- `Dockerfile` – multi-stage build, amely build argumentumokat (`APP_VERSION`, `ENVIRONMENT`) fogad, de ezeknek alapértelmezett értékei vannak.
- `.github/workflows/ci-pr.yml` – PR-re reagáló CI workflow.
- `.github/workflows/ci-dev.yml` – `dev` branchre reagáló build & audit workflow.
- `.github/workflows/ci-main.yml` – `main` branchre reagáló release build workflow.

## Használat

1. **Repó inicializálása**: Hozd létre a GitHub repositoryt a mappa tartalmával. Nincs szükség semmilyen titokra vagy tokenre.
2. **Pull request létrehozása**: Nyiss pull requestet bármely branchről; a `ci-pr` workflow automatikusan fut és kiértékeli a teszteket.
3. **Fejlesztői push**: Pusholj a `dev` branchre; a `ci-dev` workflow lefuttatja a teszteket, a `pip-audit` ellenőrzést és épít egy Docker image-et.
4. **Fő push**: Pusholj a `main` branchre; a `ci-main` workflow lefuttatja a teszteket, futtat egy statikus elemzést `bandit`-tal, és az elkészült image-et artefaktként elmenti. Ez a fájl a GitHub Actions felületén letölthető.

Ez a demonstráció bemutatja, hogyan építhető fel több lépcsős CI/CD pipeline secretek használata nélkül, és hogyan lehet különböző ágakra eltérő workflow-kat definiálni.