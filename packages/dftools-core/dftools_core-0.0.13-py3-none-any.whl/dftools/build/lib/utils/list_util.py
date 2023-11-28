
def get_all_sub_sets_from_start(array) -> list:
    return [array[:i] for i in range(1, len(array) + 1)]
