"""Registration Decorator Tests - An4ik Python TDD Port

Demonstrates decorator pattern for function registration through TDD
"""


def test_subject_1_is_decorated() -> None:
    """Test 1: subject_1 should have status attribute when decorated

    From An4ik example: Functions decorated with @register should have status attribute
    """
    from decorator_examples import subject_1

    # WHEN checking for status attribute
    status = getattr(subject_1, "status", None)

    # THEN it should have status attribute
    assert status is not None, "subject_1 should have status attribute"


def test_subject_1_is_registered() -> None:
    """Test 2: subject_1 should be in registered set

    From An4ik example: Active functions should be added to registered set
    """
    from decorator_examples import registered, subject_1

    # THEN subject_1 should be in registered set
    assert subject_1 in registered, "subject_1 should be in registered set"


def test_subject_1_is_active() -> None:
    """Test 3: subject_1 should have active status

    From An4ik example: Functions decorated with @register() should be active
    """
    from decorator_examples import subject_1

    # WHEN checking status attribute
    status = subject_1.status  # type: ignore

    # THEN status should be active
    assert status == "active", f"subject_1 should be active, but is {status}"


def test_subject_2_is_decorated() -> None:
    """Test 4: subject_2 should have status attribute when decorated

    From An4ik example: Functions decorated with @register(is_active=False) should have status
    """
    from decorator_examples import subject_2

    # WHEN checking for status attribute
    status = getattr(subject_2, "status", None)

    # THEN it should have status attribute
    assert status is not None, "subject_2 should have status attribute"


def test_subject_2_is_not_registered() -> None:
    """Test 5: subject_2 should NOT be in registered set

    From An4ik example: Inactive functions should not be added to registered set
    """
    from decorator_examples import registered, subject_2

    # THEN subject_2 should NOT be in registered set
    assert subject_2 not in registered, "subject_2 should not be in registered set"


def test_subjects_are_callable() -> None:
    """Test 6: All subjects should be callable and return None

    From An4ik example: Decorated functions should remain callable
    This test ensures 100% coverage by executing function bodies.
    """
    from decorator_examples import subject_1, subject_2, subject_3

    # WHEN calling each subject
    result_1 = subject_1()
    result_2 = subject_2()
    result_3 = subject_3()

    # THEN they should all return None (do nothing)
    assert result_1 is None, "subject_1 should return None"
    assert result_2 is None, "subject_2 should return None"
    assert result_3 is None, "subject_3 should return None"


def test_register_default_marks_active_and_adds_to_registered() -> None:
    """Test 7: register() with defaults activates and registers the function

    Calling the decorator directly (not at import time) pins the full
    registration contract: the function object is returned unchanged, its
    status attribute is exactly "active", and the function itself (not some
    other object) is added to the registered set.
    """
    from decorator_examples import register, registered

    def probe() -> None:
        pass

    try:
        # WHEN decorating with the default is_active
        decorated = register()(probe)

        # THEN the same function object is returned
        assert decorated is probe, "decorate should return the function unchanged"

        # AND its status is exactly "active"
        assert probe.status == "active", f"expected 'active', got {probe.status!r}"  # type: ignore[attr-defined]

        # AND the function itself is in the registered set
        assert probe in registered, "active function should be in registered set"
        assert None not in registered, "registered set must hold functions, not None"
    finally:
        registered.discard(probe)
        registered.discard(None)  # type: ignore[arg-type]


def test_register_inactive_marks_inactive_and_does_not_register() -> None:
    """Test 8: register(is_active=False) deactivates without registering

    The status attribute is exactly "inactive" and the function is kept out
    of the registered set.
    """
    from decorator_examples import register, registered

    def probe() -> None:
        pass

    try:
        # WHEN decorating with is_active=False
        decorated = register(is_active=False)(probe)

        # THEN the same function object is returned
        assert decorated is probe, "decorate should return the function unchanged"

        # AND its status is exactly "inactive"
        assert probe.status == "inactive", f"expected 'inactive', got {probe.status!r}"  # type: ignore[attr-defined]

        # AND it is not registered
        assert probe not in registered, "inactive function must not be registered"
        assert None not in registered, "registered set must hold functions, not None"
    finally:
        registered.discard(probe)
        registered.discard(None)  # type: ignore[arg-type]


def test_registered_contains_exactly_the_active_subjects() -> None:
    """Test 9: registered set holds exactly the active module-level subjects

    subject_1 and subject_3 are decorated with @register() (active),
    subject_2 with @register(is_active=False), so the set contains exactly
    {subject_1, subject_3}.
    """
    from decorator_examples import registered, subject_1, subject_2, subject_3

    # THEN the set contents match exactly
    assert registered == {
        subject_1,
        subject_3,
    }, f"registered should be exactly {{subject_1, subject_3}}, got {registered!r}"
    assert subject_2 not in registered


def test_module_level_subjects_have_exact_status_values() -> None:
    """Test 10: module-level subjects carry exact status strings

    subject_1/subject_3 are "active", subject_2 is "inactive" (exact,
    lowercase, undecorated strings).
    """
    from decorator_examples import subject_1, subject_2, subject_3

    assert subject_1.status == "active"  # type: ignore[attr-defined]
    assert subject_2.status == "inactive"  # type: ignore[attr-defined]
    assert subject_3.status == "active"  # type: ignore[attr-defined]
