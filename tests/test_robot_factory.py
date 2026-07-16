"""Tests for the Robot Factory kata.

Supplier catalogs are injected as plain data and robot names come from an
injected random.Random, so costing, purchasing, and naming are deterministic.
"""


def _suppliers() -> list:
    """Three suppliers with overlapping catalogs; no supplier carries every part."""
    from robot_factory import Supplier

    return [
        Supplier(
            "robo_mart",
            {
                "standard vision": 20.0,
                "infrared vision": 30.0,
                "square": 10.0,
                "round": 12.0,
                "hands": 15.0,
                "wheels": 8.0,
                "legs": 12.0,
                "solar": 25.0,
            },
        ),
        Supplier(
            "gear_works",
            {
                "standard vision": 18.0,
                "night vision": 45.0,
                "square": 11.0,
                "triangular": 14.0,
                "hands": 16.0,
                "pinchers": 13.0,
                "wheels": 9.0,
                "tracks": 22.0,
                "rechargeable battery": 28.0,
            },
        ),
        Supplier(
            "parts_r_us",
            {
                "infrared vision": 27.0,
                "night vision": 50.0,
                "rectangular": 16.0,
                "hands": 15.0,
                "boxing gloves": 19.0,
                "legs": 11.0,
                "solar": 24.0,
                "biomass": 30.0,
            },
        ),
    ]


def _spec() -> dict[str, str]:
    """A complete, valid robot configuration."""
    return {
        "head": "standard vision",
        "body": "square",
        "arms": "hands",
        "movement": "wheels",
        "power": "solar",
    }


def test_factory_requires_at_least_three_suppliers() -> None:
    """Test 1: Fewer than three suppliers raises ValueError"""
    import random

    import pytest

    from robot_factory import RobotFactory

    with pytest.raises(ValueError) as excinfo:
        RobotFactory(_suppliers()[:2], random.Random(1))
    assert str(excinfo.value) == "at least 3 suppliers are required, got [2]"


def test_duplicate_supplier_names_are_rejected() -> None:
    """Test 2: Two suppliers sharing a name raises ValueError"""
    import random

    import pytest

    from robot_factory import RobotFactory, Supplier

    suppliers = _suppliers()[:2] + [Supplier("robo_mart", {"legs": 5.0})]

    with pytest.raises(ValueError) as excinfo:
        RobotFactory(suppliers, random.Random(1))
    assert str(excinfo.value) == "duplicate supplier name [robo_mart]"


def test_costing_picks_the_cheapest_supplier_for_each_part() -> None:
    """Test 3: Each part is sourced from the supplier with the lowest price"""
    import random

    from robot_factory import RobotFactory

    factory = RobotFactory(_suppliers(), random.Random(1))

    quote = factory.cost_robot(_spec())

    sourced = {part.category: (part.supplier, part.price) for part in quote.parts}
    assert sourced["head"] == ("gear_works", 18.0)  # 18 beats robo_mart's 20
    assert sourced["body"] == ("robo_mart", 10.0)  # 10 beats gear_works' 11
    assert sourced["movement"] == ("robo_mart", 8.0)  # 8 beats gear_works' 9
    assert sourced["power"] == ("parts_r_us", 24.0)  # 24 beats robo_mart's 25


def test_quote_total_is_the_sum_of_the_cheapest_parts() -> None:
    """Test 4: The quote total is 18 + 10 + 15 + 8 + 24 = 75.0"""
    import random

    from robot_factory import RobotFactory

    factory = RobotFactory(_suppliers(), random.Random(1))

    quote = factory.cost_robot(_spec())

    assert quote.total == 75.0


def test_price_ties_go_to_the_supplier_listed_first() -> None:
    """Test 5: robo_mart and parts_r_us both sell hands at 15.0; robo_mart wins"""
    import random

    from robot_factory import RobotFactory

    factory = RobotFactory(_suppliers(), random.Random(1))

    quote = factory.cost_robot(_spec())

    arms = next(part for part in quote.parts if part.category == "arms")
    assert arms.supplier == "robo_mart"
    assert arms.price == 15.0


def test_costing_works_when_no_single_supplier_carries_everything() -> None:
    """Test 6: A configuration spanning gaps in every catalog is still quotable"""
    import random

    from robot_factory import RobotFactory

    factory = RobotFactory(_suppliers(), random.Random(1))

    quote = factory.cost_robot(
        {
            "head": "night vision",  # only gear_works and parts_r_us
            "body": "round",  # only robo_mart
            "arms": "boxing gloves",  # only parts_r_us
            "movement": "tracks",  # only gear_works
            "power": "biomass",  # only parts_r_us
        }
    )

    assert quote.total == 45.0 + 12.0 + 19.0 + 22.0 + 30.0


def test_part_carried_by_no_supplier_is_unavailable() -> None:
    """Test 7: A part missing from every catalog raises PartUnavailableError"""
    import random

    import pytest

    from robot_factory import PartUnavailableError, RobotFactory, Supplier

    suppliers = [
        Supplier("a", {"standard vision": 1.0, "square": 1.0, "hands": 1.0}),
        Supplier("b", {"wheels": 1.0}),
        Supplier("c", {"solar": 1.0}),
    ]
    factory = RobotFactory(suppliers, random.Random(1))
    spec = dict(_spec(), power="biomass")  # nobody carries biomass

    with pytest.raises(PartUnavailableError) as excinfo:
        factory.cost_robot(spec)
    assert str(excinfo.value) == "no supplier carries [biomass]"


def test_missing_part_category_is_rejected() -> None:
    """Test 8: A configuration without a power choice raises ValueError"""
    import random

    import pytest

    from robot_factory import RobotFactory

    factory = RobotFactory(_suppliers(), random.Random(1))
    spec = _spec()
    del spec["power"]

    with pytest.raises(ValueError) as excinfo:
        factory.cost_robot(spec)
    assert str(excinfo.value) == "missing part category [power]"


def test_unknown_part_category_is_rejected() -> None:
    """Test 9: A category outside head/body/arms/movement/power raises ValueError"""
    import random

    import pytest

    from robot_factory import RobotFactory

    factory = RobotFactory(_suppliers(), random.Random(1))
    spec = dict(_spec(), antenna="long range")

    with pytest.raises(ValueError) as excinfo:
        factory.cost_robot(spec)
    assert str(excinfo.value) == "unknown part category [antenna]"


def test_invalid_option_for_a_category_is_rejected() -> None:
    """Test 10: An option not offered for its category raises ValueError"""
    import random

    import pytest

    from robot_factory import RobotFactory

    factory = RobotFactory(_suppliers(), random.Random(1))
    spec = dict(_spec(), head="x-ray vision")

    with pytest.raises(ValueError) as excinfo:
        factory.cost_robot(spec)
    assert str(excinfo.value) == "invalid head option [x-ray vision]"


def test_purchased_robot_matches_its_quote() -> None:
    """Test 11: Purchasing sources the same parts and total as costing"""
    import random

    from robot_factory import RobotFactory

    factory = RobotFactory(_suppliers(), random.Random(1))
    quote = factory.cost_robot(_spec())

    robot = factory.purchase_robot(_spec())

    assert robot.parts == quote.parts
    assert robot.total == 75.0


def test_purchasing_places_orders_with_the_respective_suppliers() -> None:
    """Test 12: Each supplier records exactly the parts bought from it"""
    import random

    from robot_factory import RobotFactory

    factory = RobotFactory(_suppliers(), random.Random(1))

    factory.purchase_robot(_spec())

    robo_mart_orders = factory.orders_for("robo_mart")
    assert [(order.option, order.price) for order in robo_mart_orders] == [
        ("square", 10.0),
        ("hands", 15.0),
        ("wheels", 8.0),
    ]
    gear_works_orders = factory.orders_for("gear_works")
    assert [(order.option, order.price) for order in gear_works_orders] == [
        ("standard vision", 18.0)
    ]
    parts_r_us_orders = factory.orders_for("parts_r_us")
    assert [(order.option, order.price) for order in parts_r_us_orders] == [
        ("solar", 24.0)
    ]


def test_costing_alone_places_no_orders() -> None:
    """Test 13: cost_robot only queries suppliers; nothing is purchased"""
    import random

    from robot_factory import RobotFactory

    factory = RobotFactory(_suppliers(), random.Random(1))

    factory.cost_robot(_spec())

    assert factory.orders_for("robo_mart") == ()
    assert factory.orders_for("gear_works") == ()
    assert factory.orders_for("parts_r_us") == ()


def test_orders_for_unknown_supplier_is_rejected() -> None:
    """Test 14: Asking for orders of an unlisted supplier raises ValueError"""
    import random

    import pytest

    from robot_factory import RobotFactory

    factory = RobotFactory(_suppliers(), random.Random(1))

    with pytest.raises(ValueError) as excinfo:
        factory.orders_for("acme")
    assert str(excinfo.value) == "unknown supplier [acme]"


def test_robot_names_are_two_uppercase_letters_and_three_digits() -> None:
    """Test 15: Serial names match the pattern AA000"""
    import random
    import re

    from robot_factory import RobotFactory

    factory = RobotFactory(_suppliers(), random.Random(7))

    robot = factory.purchase_robot(_spec())

    assert re.fullmatch(r"[A-Z]{2}[0-9]{3}", robot.name) is not None


def test_robot_names_are_unique_within_a_factory() -> None:
    """Test 16: Thirty purchases yield thirty distinct serial names"""
    import random

    from robot_factory import RobotFactory

    factory = RobotFactory(_suppliers(), random.Random(7))

    names = [factory.purchase_robot(_spec()).name for _ in range(30)]

    assert len(set(names)) == 30


def test_same_seed_reproduces_the_same_name_sequence() -> None:
    """Test 17: Factories seeded identically stamp identical name sequences"""
    import random

    from robot_factory import RobotFactory

    first = RobotFactory(_suppliers(), random.Random(42))
    second = RobotFactory(_suppliers(), random.Random(42))

    first_names = [first.purchase_robot(_spec()).name for _ in range(5)]
    second_names = [second.purchase_robot(_spec()).name for _ in range(5)]

    assert first_names == second_names


def test_every_name_in_a_production_run_keeps_the_serial_format() -> None:
    """Test 18: Ten purchases all stamp two uppercase letters and three digits"""
    import random
    import re

    from robot_factory import RobotFactory

    factory = RobotFactory(_suppliers(), random.Random(30))

    names = [factory.purchase_robot(_spec()).name for _ in range(10)]

    assert all(re.fullmatch(r"[A-Z]{2}[0-9]{3}", name) for name in names)


def test_names_stay_unique_across_a_long_production_run() -> None:
    """Test 19: Fifty purchases yield fifty distinct serial names"""
    import random

    from robot_factory import RobotFactory

    factory = RobotFactory(_suppliers(), random.Random(390))

    names = [factory.purchase_robot(_spec()).name for _ in range(50)]

    assert len(set(names)) == 50
