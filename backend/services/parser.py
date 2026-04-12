import pandas as pd

def detect_column(df, keywords):
    for col in df.columns:
        for key in keywords:
            if key in col.lower():
                return col
    return None


def parse_file(path):
    if path.endswith(".csv"):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)

    df.columns = df.columns.str.strip()

    print("ORIGINAL COLUMNS:", df.columns)

    mapping = {
        "course": detect_column(df, ["course", "subject", "module"]),
        "lecturer": detect_column(df, ["lecturer", "teacher", "instructor"]),
        "room": detect_column(df, ["room", "hall", "venue"]),
        "capacity": detect_column(df, ["capacity", "size"]),
        "students": detect_column(df, ["students", "enrollment"]),
        "group": detect_column(df, ["group", "class", "level"])
    }

    print("AUTO MAPPING:", mapping)

    rename_map = {v: k for k, v in mapping.items() if v is not None}

    df = df.rename(columns=rename_map)

    print("FINAL COLUMNS:", df.columns)

    return df