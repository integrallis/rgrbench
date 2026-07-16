"""Alarm System Classes - TDD Ebook Object Composition Example
Demonstrates decorator pattern and object composition through TDD
"""


def test_loud_alarm_should_trigger_loudly() -> None:
    """Test 1: LoudAlarm should trigger loudly

    From the book: Basic alarm implementation to establish the interface
    """
    from alarm_system.loud_alarm import LoudAlarm

    # GIVEN
    alarm = LoudAlarm()

    # WHEN
    result = alarm.trigger()

    # THEN
    assert result == "LOUD ALARM!"


def test_day_night_switched_alarm_should_trigger_during_day() -> None:
    """Test 2: DayNightSwitchedAlarm should trigger during day

    From the book: Decorator pattern - wraps another alarm and modifies behavior
    based on time of day. During day it triggers, during night it doesn't.
    """
    from alarm_system.day_night_switched_alarm import DayNightSwitchedAlarm
    from alarm_system.loud_alarm import LoudAlarm

    # GIVEN
    wrapped_alarm = LoudAlarm()
    alarm = DayNightSwitchedAlarm(wrapped_alarm, is_day=True)

    # WHEN
    result = alarm.trigger()

    # THEN
    assert result == "LOUD ALARM!"


def test_day_night_switched_alarm_should_be_silent_during_night() -> None:
    """Test 3: DayNightSwitchedAlarm should be silent during night

    From the book: Decorator pattern - demonstrates conditional behavior
    based on the decorator's state (day/night).
    """
    from alarm_system.day_night_switched_alarm import DayNightSwitchedAlarm
    from alarm_system.loud_alarm import LoudAlarm

    # GIVEN
    wrapped_alarm = LoudAlarm()
    alarm = DayNightSwitchedAlarm(wrapped_alarm, is_day=False)

    # WHEN
    result = alarm.trigger()

    # THEN
    assert result == ""


def test_hybrid_alarm_should_combine_multiple_alarms() -> None:
    """Test 4: HybridAlarm should combine multiple alarms

    From the book: Object composition - combines multiple alarm sources
    into a single unified alarm output. Demonstrates composition over inheritance.
    """
    from alarm_system.hybrid_alarm import HybridAlarm
    from alarm_system.loud_alarm import LoudAlarm

    # GIVEN
    primary_alarm = LoudAlarm()
    secondary_alarm = LoudAlarm()
    alarm = HybridAlarm([primary_alarm, secondary_alarm])

    # WHEN
    result = alarm.trigger()

    # THEN
    assert result == "LOUD ALARM! LOUD ALARM!"
