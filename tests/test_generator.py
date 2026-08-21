import random

import pytest

from pythonesque import UnifiedFoundationalGenerator


def test_same_seed_reproduces_the_same_sequence():
    first = UnifiedFoundationalGenerator("repeatable")
    second = UnifiedFoundationalGenerator("repeatable")
    assert [first.generate() for _ in range(20)] == [second.generate() for _ in range(20)]


def test_different_seeds_are_not_the_same_sequence():
    first = UnifiedFoundationalGenerator("a")
    second = UnifiedFoundationalGenerator("b")
    assert [first.generate() for _ in range(3)] != [second.generate() for _ in range(3)]


def test_slug_is_lowercase_and_url_safe():
    value = UnifiedFoundationalGenerator("slug").generate(slugify=True)
    assert value == value.lower()
    assert value.replace("-", "").isalnum()


def test_instance_does_not_change_global_random_state():
    random.seed(12345); expected = random.random()
    random.seed(12345); UnifiedFoundationalGenerator().generate(); assert random.random() == expected


def test_seed_must_be_text():
    with pytest.raises(TypeError, match="seed must be a string"):
        UnifiedFoundationalGenerator(4)  # type: ignore[arg-type]


def test_nested_generated_legal_actions_are_fully_expanded():
    generator = UnifiedFoundationalGenerator("legal")
    assert "{{" not in generator._resolve("generated_legal_action")
