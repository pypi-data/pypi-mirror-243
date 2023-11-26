def remove_nulls(d):
    return {k: remove_nulls(v) if isinstance(v, dict) else v for k, v in d.items() if v is not None}
