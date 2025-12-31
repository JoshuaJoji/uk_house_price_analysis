import pandas as pd


DATA_PATH = "data/clean/Average_UK_houseprices_and_salary.csv"

def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df.columns = [c.strip() for c in df.columns]
    return df


def test_required_columns_exist():
    df = load_data()
    expected = {"Year", "Real_House_Price", "Real_Median_Salary"}
    assert expected.issubset(df.columns)


def test_year_is_integer_like_and_monotonic():
    df = load_data()
    years = pd.to_numeric(df["Year"], errors="coerce")
    assert years.notna().all()
    assert (years % 1 == 0).all()
    assert years.is_monotonic_increasing


def test_no_missing_values_in_core_columns():
    df = load_data()
    core = df[["Year", "Real_House_Price", "Real_Median_Salary"]]
    assert core.isnull().sum().sum() == 0


def test_values_are_positive():
    df = load_data()
    assert (df["Real_House_Price"] > 0).all()
    assert (df["Real_Median_Salary"] > 0).all()


def test_house_prices_exceed_salaries():
    df = load_data()
    assert (df["Real_House_Price"] > df["Real_Median_Salary"]).all()


def test_affordability_ratio_is_gt_one():
    df = load_data()
    ratio = df["Real_House_Price"] / df["Real_Median_Salary"]
    assert (ratio > 1).all()