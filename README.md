# Demo: CI/CD pipeline – három GitHub Actions workflow, titkok nélkül

Ebben a példában egy minimális Flask alkalmazást találunk a repository gyökerében, kiegészítve három különálló GitHub Actions workflow-val. A cél az, hogy a folyamat futtatásához ne legyen szükség semmilyen felhasználói titokra: minden lépés a GitHub alapértelmezett tokenjeit és környezetét használja. A kód struktúrája és a workflow-k úgy vannak kialakítva, hogy a legtöbb CI/CD funkciót szemléltessék.

## Mappa struktúra

- `app/` – a Flask alkalmazás csomagja, benne az `__init__.py` és `main.py` modulokkal.
- `test/` – pytest tesztek, amelyek ellenőrzik a `/` és `/info` végpontok működését.
- `requirements.txt` – a projekt Python-függőségei.
- `Dockerfile` – multi-stage build definíció paraméterezhető build argumentumokkal.
- `.github/workflows/` – három különálló workflow:
  - `ci-pr.yml` – PR case: build és tesztek.
  - `ci-dev.yml` – fejlesztői ágon (dev) build, tesztek és pip-audit.
  - `ci-main.yml` – főág (main) build, tesztek, bandit security scan és image artefakt.

## Workflow-k röviden

1. **ci-pr.yml** – fut, amikor pull request nyílik bármelyik branchről. Telepíti a Python környezetet, a függőségeket, majd futtatja a teszteket. Ha valamelyik teszt elbukik, a PR nem mergelhető.

2. **ci-dev.yml** – a `dev` branchre érkező push esetén aktiválódik. A workflow telepíti a függőségeket, futtatja a pytest-et, majd a `pip-audit` eszközzel ellenőrzi a `requirements.txt` sebezhetőségeit, és buildeli a Docker image-et `dev` taggel.

3. **ci-main.yml** – a `main` branchre történő pushra reagál. A workflow unit teszteket futtat, majd a `bandit` statikus kódanalízist végzi az `app/` könyvtáron. Ezután buildeli a Docker image-et, fájlba menti (`docker save`) és a GitHub Actions felületén artefaktként elmenti, letölthetővé téve a build eredményét.

## Használat

1. Hozd létre a GitHub repository-t a mappa tartalmával (a gyökérben található mappák és fájlok kerüljenek a repó gyökerébe).
2. Nyiss egy pull requestet – a `ci-pr` workflow lefut és teszteli a kódot.
3. Pusholj a `dev` branchre – a `ci-dev` workflow lefut, auditot és buildet végez.
4. Pusholj a `main` branchre – a `ci-main` workflow lefut, security scan-t és release buildet készít.

Semmilyen titok vagy egyéni token megadására nincs szükség; a workflow-k a GitHub által biztosított környezetet használják.