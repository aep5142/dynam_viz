import duckdb
import pandas as pd
from pathlib import Path
import altair as alt

DOLLAR = 950  # 1 dollar is $950 CLP


# Helper Function 1: Automates filters
def automates_where_clause(kwargs):
    # Extract dynamic filters
    min_year = kwargs.get("min_year")
    max_year = kwargs.get("max_year")
    regions = kwargs.get("regions")

    # Build SQL filters dynamically
    filters = []

    if min_year is not None:
        filters.append(f"año_solicitud >= {min_year}")

    if max_year is not None:
        filters.append(f"año_solicitud <= {max_year}")

    if regions:
        regions_sql = ", ".join(f"'{r}'" for r in regions)
        filters.append(f"region IN ({regions_sql})")

    # Final WHERE clause
    where_clause = ""
    if filters:
        where_clause = "WHERE " + " AND ".join(filters)
    return where_clause


# Helper 2: Watch the parquet db
def query_view_db(
    db: duckdb.DuckDBPyConnection, path_parquet="data/summary_table.parquet", **kwargs
) -> pd.DataFrame:
    where_clause = automates_where_clause(kwargs)

    # SQL query
    query = f"""
        SELECT *
        FROM read_parquet('{path_parquet}')
        limit 10
        {where_clause}
    """

    # Return scalar value
    return db.execute(query).fetchdf()


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


def query_total_borrowed(
    db: duckdb.DuckDBPyConnection, path_parquet="data/summary_table.parquet", **kwargs
) -> int:
    where_clause = automates_where_clause(kwargs)

    # SQL query
    query = f"""
        SELECT SUM(total_prestado) / {DOLLAR} AS total
        FROM read_parquet('{path_parquet}')
        {where_clause}
    """

    # Return scalar value
    return db.execute(query).fetchone()[0]


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


def query_total_requests_granted(
    db: duckdb.DuckDBPyConnection, path_parquet="data/summary_table.parquet", **kwargs
) -> int:
    where_clause = automates_where_clause(kwargs)

    # SQL query
    query = f"""
        SELECT año_solicitud as año,
            quintil as quintil,
            SUM(total_prestamos) as total_prestamos
        FROM read_parquet('{path_parquet}')
        GROUP BY año, quintil
        {where_clause}
    """

    solicitations = db.execute(query).fetchdf()

    values = ["quintil 1 y 2", "quintil 3", "quintil 4", "quintil 5"]
    colors = ["#1d7874ff", "#679289ff", "#b2cec8ff", "#cfe795ff"]

    chart_solicitations = (
        alt.Chart(solicitations)
        .mark_area()
        .encode(
            x=alt.X(
                "año_licitacion",
                axis=alt.Axis(
                    format=".0f",
                    grid=False,
                    labelFontSize=14,
                    titleFontSize=16,
                    values=list(range(2006, 2026, 2)),
                ),
            ).title("Year"),
            y=alt.Y(
                "total_count",
                axis=alt.Axis(grid=False, labelFontSize=14, titleFontSize=16),
            ).title("Total granted loans (thousands)"),
            color=alt.Color(
                "quintil",
                scale=alt.Scale(domain=values, range=colors),
                legend=alt.Legend(title="Quintile", orient="top-right"),
            ),
        )
        .properties(
            title="CAE loans by income quintile (thousands)",
            height=400,
            width=500,
        )
        .configure_axis(grid=False, labelFontSize=12, titleFontSize=18)
        .configure_view(strokeWidth=0)
        .configure(background="transparent")
        .configure_legend(labelFontSize=14)
        .configure_title(fontSize=20)
    )

    return chart_solicitations


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


def query_average_loan(
    db: duckdb.DuckDBPyConnection, path_parquet="data/summary_table.parquet", **kwargs
) -> int:
    where_clause = automates_where_clause(kwargs)

    # SQL query
    query = f"""
        SELECT AVG(total_prestado)/ {DOLLAR} AS avg_loan
        FROM read_parquet('{path_parquet}')
        {where_clause}
    """

    # Return scalar value
    return db.execute(query).fetchone()[0]


def query_average_financed_years(
    db: duckdb.DuckDBPyConnection, path_parquet="data/summary_table.parquet", **kwargs
) -> int:
    where_clause = automates_where_clause(kwargs)

    # SQL query
    query = f"""
        SELECT AVG(años_financiados)
        FROM read_parquet('{path_parquet}')
        {where_clause}
    """

    # Return scalar value
    return db.execute(query).fetchone()[0]


def query_prob_desertion(
    db: duckdb.DuckDBPyConnection, path_parquet="data/summary_table.parquet", **kwargs
) -> int:
    where_clause = automates_where_clause(kwargs)

    # SQL query
    query = f"""
        SELECT SUM(total_deserciones) / SUM(cantidad_carreras)
        FROM read_parquet('{path_parquet}')
        {where_clause}
    """

    # Return scalar value
    return db.execute(query).fetchone()[0]


def query_prob_graduation(
    db: duckdb.DuckDBPyConnection, path_parquet="data/summary_table.parquet", **kwargs
) -> int:
    where_clause = automates_where_clause(kwargs)

    # SQL query
    query = f"""
        SELECT SUM(total_egresos) / SUM(cantidad_carreras)
        FROM read_parquet('{path_parquet}')
        {where_clause}
    """

    # Return scalar value
    return db.execute(query).fetchone()[0]


def query_percentage_financed(
    db: duckdb.DuckDBPyConnection, path_parquet="data/summary_table.parquet", **kwargs
) -> int:
    where_clause = automates_where_clause(kwargs)

    # SQL query
    query = f"""
        SELECT AVG(
            CASE WHEN porcentaje_financiado <=1 AND porcentaje_financiado > 0
                THEN porcentaje_financiado END)
            as porcentaje_financiado
        FROM read_parquet('{path_parquet}')
        {where_clause}
    """

    # Return scalar value
    return db.execute(query).fetchone()[0]



db = duckdb.connect()
print(query_view_db(db)["quintil"].unique())
