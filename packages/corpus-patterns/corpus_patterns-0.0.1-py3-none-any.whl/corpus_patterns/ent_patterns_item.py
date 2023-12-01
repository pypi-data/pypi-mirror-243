between_node = {"ORTH": {"IN": ["of", "the", ","]}, "OP": "*"}


def create_item_patterns(unit_label: str, container_labels: list[str]):
    for pattern in [
        [
            {"ENT_TYPE": unit_label, "OP": "+"},
            between_node,
            {"ENT_TYPE": {"IN": container_labels}},
        ],
        [
            {"ENT_TYPE": {"IN": container_labels}},
            between_node,
            {"ENT_TYPE": unit_label, "OP": "+"},
        ],
    ]:
        yield pattern
