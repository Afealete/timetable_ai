import pandas as pd
import re

REQUIRED_COLUMNS = ["course", "lecturer", "group"]
OPTIONAL_COLUMNS = ["capacity", "students", "room"]

# Keywords to detect columns
COLUMN_KEYWORDS = {
    "course": ["course", "subject", "class", "module", "title"],
    "lecturer": ["lecturer", "teacher", "instructor", "professor", "staff"],
    "room": ["room", "venue", "location", "hall", "classroom"],
    "capacity": ["capacity", "size", "seats", "max_students"],
    "students": ["students", "enrolled", "count", "number"],
    "group": ["group", "batch", "section", "class_group", "cohort"]
}

def detect_column(df_columns, logical_name):
    """Detect the best matching column for a logical name."""
    keywords = COLUMN_KEYWORDS.get(logical_name, [])
    for col in df_columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in keywords):
            return col
    return None

def parse_file(filepath, column_map=None):
    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)

    # If column_map is provided, use it
    if column_map and isinstance(column_map, dict):
        rename_map = {}
        for logical in REQUIRED_COLUMNS + OPTIONAL_COLUMNS:
            if logical in column_map and column_map[logical]:
                source = column_map[logical]
                if source in df.columns:
                    rename_map[source] = logical
                else:
                    raise KeyError(f"Mapped column '{source}' for '{logical}' not found in file")
            else:
                # Auto-detect if not mapped
                detected = detect_column(df.columns, logical)
                if detected:
                    rename_map[detected] = logical
                elif logical in REQUIRED_COLUMNS:
                    raise KeyError(f"Could not detect or map column for '{logical}'")
        df = df.rename(columns=rename_map)
    else:
        # Auto-detect all columns
        rename_map = {}
        for logical in REQUIRED_COLUMNS + OPTIONAL_COLUMNS:
            detected = detect_column(df.columns, logical)
            if detected:
                rename_map[detected] = logical
            elif logical in REQUIRED_COLUMNS:
                raise KeyError(f"Could not detect column for '{logical}'")
        df = df.rename(columns=rename_map)

    # Ensure required normalized columns exist
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise KeyError(f"Required columns missing after processing: {missing}")

    # Add optional columns if not present
    for col in OPTIONAL_COLUMNS:
        if col not in df.columns:
            if col == "capacity":
                df[col] = 100
            elif col == "students":
                df[col] = 50
            else:
                df[col] = None

    # Filter out rows with NaN or empty values in required columns
    df = df.dropna(subset=REQUIRED_COLUMNS)
    df = df[df[REQUIRED_COLUMNS].apply(lambda x: x.str.strip() != '' if x.dtype == 'object' else True).all(axis=1)]

    return df