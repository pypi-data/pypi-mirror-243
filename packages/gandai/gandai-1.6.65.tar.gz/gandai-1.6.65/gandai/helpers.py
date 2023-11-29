import pandas as pd
import tldextract

def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [col.lower().replace(" ", "_").replace(".", "") for col in df.columns]
    return df


def clean_domain(url: str) -> str:
    ext = tldextract.extract(url.strip())
    return ext.registered_domain


# def clean_domain(url: str) -> str:
#     if url is None or url == "":
#         return None

#     url = url.lower().strip()
#     url = url.replace("http://", "").replace("https://", "").replace("www.", "")
#     parts = url.split("/")[0].split(".")

#     # Check for country code
#     if len(parts) > 2 and len(parts[-1]) == 2:
#         return ".".join(parts[-2:])
#     else:
#         return ".".join(parts)

def domain_is_none(url: str) -> bool:
    return url is None or url == ""
