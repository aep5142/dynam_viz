Dynam Viz — Interactive visualizations for CAE student paths

**What is the CAE (Crédito con Aval del Estado)?**
- **Short definition:** The CAE (Crédito con Aval del Estado) is a government-backed student loan program in Chile that helps students finance tertiary education (universities, professional institutes, technical centers). The loan is guaranteed by the State, often with subsidized conditions for students meeting specific criteria.
- **Why it matters:** CAE is a major mechanism for access to higher education in Chile. Analyzing CAE data helps answer policy-relevant questions about access, equity, loan uptake across income quintiles and regions, loan size and duration, graduation and dropout patterns, and the distributional impacts of public support for higher education.

**Project purpose**
- **Objective:** Produce reproducible analytics and interactive visualizations to describe how CAE loans are distributed across regions, income quintiles, and student paths (egress, desertion, career changes), and to create datasets suitable for web visualization.
- **Audience:** researchers, policy analysts, instructors and students in data visualization courses, and anyone interested in student finance and educational outcomes in Chile.

**Repository layout**
- **`README.md`**: this file.
- **`src/`**: Jupyter notebooks and small Python scripts used for data preparation and analysis.
  - `src/query_cae.ipynb`: main analysis notebook — loads raw CAE data, aggregates with DuckDB, exports JSON/Parquet outputs.
  - `src/hello.py`, `src/prueba.ipynb`: utilities and experiments.
- **`css/`**: styling used by the web front-end (e.g., `css/main.css`).
- **`www/`**: web assets and generated data.
  - `www/data/` (generated): JSON files consumed by the visualization front-end (not committed by default).
- **`data/`**: generated Parquet files and other intermediate outputs.
- **`milestones/`**: notes, proposals and project planning documents (e.g., `interactive-proposal.md`).

**Data sources & expected paths**
- **Raw CAE dataset**: The primary raw file used in the notebook is expected at `../../kids_chances/data/raw/cae_history.txt` (relative to `src/`). If you keep raw files elsewhere, update the `cae_path` variable in `src/query_cae.ipynb`.
- **DuckDB database**: The notebook writes/reads a DuckDB DB at `../www/data/cae_db.duckdb` by default.
- **Generated outputs**: `www/data/*.json` and `data/*.parquet` (examples: `percent_financed.json`, `total_borrowed.json`, `summary_table.parquet`).

**Dependencies & environment**
- **Python:** >= 3.13 (declared in `pyproject.toml`). Use a virtual environment.
- **Main packages:** `altair`, `duckdb`, `pandas`, `pyarrow`, `ipykernel`.
- **Install (recommended):**

  python -m venv .venv
  source .venv/bin/activate
  python -m pip install --upgrade pip
  python -m pip install altair duckdb pandas pyarrow ipykernel ruff

  Alternatively use Poetry or another dependency manager and the `pyproject.toml` file.

**How to run the analysis (quick start)**
1. Create & activate the virtual environment as shown above.
2. Ensure the raw CAE file is available at the path used by the notebook (or edit `cae_path` in `src/query_cae.ipynb`).
3. Open `src/query_cae.ipynb` in Jupyter Lab / Notebook and run cells sequentially to generate processed outputs in `www/data/` and `data/`.

  jupyter lab

4. After successful execution, the generated `www/data/*.json` files can be used directly by the project's front-end.

**Reproducible script (suggestion)**
- If you want non-interactive reproduction, I can add a script `scripts/generate_data.py` that:
  - reads the raw file, loads/creates the DuckDB DB,
  - runs the SQL queries (same logic as the notebook),
  - writes JSON and Parquet outputs to `www/data/` and `data/`.

**Common issues & troubleshooting**
- **SQL syntax errors:** Complex query strings often contain extra parentheses or trailing commas (these produce DuckDB errors). Inspect the exception and the query string to spot misplaced `)` or commas.
- **Missing files / wrong paths:** Notebooks use relative paths. Run from the `src/` folder or update path variables.
- **Permission errors writing outputs:** ensure `www/data/` and `data/` directories exist and are writable.

**Development & contribution**
- Want me to do next?
  - Fix queries in `src/query_cae.ipynb` and re-run the notebook to generate `www/data/*.json`.
  - Add `scripts/generate_data.py` for reproducible processing.
  - Create a `requirements.txt` or adapt `pyproject.toml` for Poetry usage.

**License & contact**
- No license file is included. Add a `LICENSE` if you plan to publish.
- For help or changes, ask me to: (a) run the notebook end-to-end, (b) correct SQL queries, or (c) scaffold the reproducible script.

**Acknowledgements**
- Built as part of coursework for the UChicago Fall 2025 Data Visualization course. Analysis depends on the external `kids_chances` raw dataset for CAE histories.
