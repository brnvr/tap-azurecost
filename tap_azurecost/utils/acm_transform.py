def merge_columns_and_rows(data:dict) -> list[dict]:
    """Receives a list[dict] in the format of the 'properties' returned by the ACM API and return a list[dict] in the format expected by the tap."""
    column_names = [col["name"] for col in data["columns"]]

    return [
        {column_names[i]: row[i] for i in range(len(column_names))}
        for row in data["rows"]
    ]