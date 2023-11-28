import pandas as pd


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [col.lower().replace(" ", "_").replace(".", "") for col in df.columns]
    return df


def clean_domain(url: str) -> str:
    if url is None or url == "":
        return None

    url = url.lower().strip()
    url = url.replace("http://", "").replace("https://", "").replace("www.", "")
    parts = url.split("/")[0].split(".")

    if len(parts) > 2:
        return ".".join(parts[1:])
    else:
        return ".".join(parts)


def domain_is_none(url: str) -> bool:
    return url is None or url == ""
