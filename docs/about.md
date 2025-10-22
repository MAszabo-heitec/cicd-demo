# About This Project

The **Complex CI/CD Demo** illustrates best practices for continuous integration and delivery in a simple yet realistic setup.  By using multiple GitHub Actions workflows, it separates concerns between pull request verification, development branch builds with security audits, and production releases with automatic documentation deployment.

## CI/CD Workflows

### Pull Request CI (`ci-pr.yml`)

This workflow is triggered on every open or updated pull request.  It performs the following steps:

1. **Check out the repository** to ensure it has access to the code under test.
2. **Set up Python 3.11** using the official `actions/setup-python` action.
3. **Install runtime and development dependencies**, including the linter (`flake8`).
4. **Run the linter** to catch code style issues and potential errors.
5. **Execute unit tests** with `pytest` to verify functionality.

By running these checks early, the workflow catches errors before they reach the `dev` branch and enforces consistent code quality.

### Development Build & Audit (`ci-dev.yml`)

This workflow runs on pushes to the `dev` branch.  In addition to the steps from the PR workflow, it:

* **Installs `pip-audit`** to scan installed dependencies for known vulnerabilities.
* **Performs a dependency security audit** with `pip-audit`.
* **Builds a Docker image** tagged with the current commit SHA.  Building the image ensures that changes which break the containerization process are detected early.

This workflow helps ensure that the development branch remains healthy and secure before promotion to the `main` branch.

### Main Release & Pages (`ci-main.yml`)

The most comprehensive workflow, triggered on pushes to the `main` branch, performs the following:

1. **Runs unit tests** to validate functionality.
2. **Runs `flake8` and `bandit`** for style checking and basic security linting.  The `bandit` step is configured to continue on error so it does not block deployment but still reports findings.
3. **Builds a Docker image** to ensure containerization remains functional.
4. **Injects the current commit SHA** into the documentation by replacing the `{{COMMIT_SHA}}` placeholder in `docs/index.md`.  This makes the commit visible on the published site.
5. **Builds the static site** using `mkdocs`.  The output is written to the `site` directory.
6. **Uploads the site** as an artifact using `actions/upload-pages-artifact`.  This step packages the built documentation so it can be deployed in a separate job.
7. **Deploys the site to GitHub Pages** using `actions/deploy-pages@v4`.  The deployment job runs with `pages: write` and `id-token: write` permissions and publishes the site to the `github-pages` environment.

Because this workflow builds the documentation on every push to `main` and injects the commit SHA, any new commit will be reflected on the live site immediately after the workflow completes.  No secrets are required — GitHub's built‑in token is sufficient for the deployment.

## Additional Notes

* The **Dockerfile** uses a multi‑stage build to minimize the size of the final image.
* The **`docs/`** directory contains the content for the GitHub Pages site.  The `mkdocs.yml` file configures navigation and theme.
* **Unit tests** reside in the `test/` directory.  They use Flask's test client to call endpoints without requiring a running server.

For more information on how to run the project locally or details about the API, consult the [home page](index.md) in the repository root.