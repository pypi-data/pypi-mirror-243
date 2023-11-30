from typing import List, Dict


def pick_by_id(
    llist: List[object], id_value: str, id_field: str = "id"
) -> Dict[object, object]:
    """
    Returns the requested of a list of dictionaries with an identifier field.

    NOTE: if the identifier field is not unique, only the first occurrence is returned

    Args:
        llist (List[object]): list to iterate on.
        id_value (str): value of the id.
        id_field (str): name of the id field to be used to match id_value. Defaults to 'id'.

    Returns:
        Dict[object, object]: first found element.
    """
    return [ll for ll in llist if ll[id_field] == id_value][0]
