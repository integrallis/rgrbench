"""
Tests for the Social Network kata (tddbuddy.com/katas/social-network).
Timestamps are supplied through an injected clock for deterministic ordering.
"""


def test_posted_message_appears_on_own_timeline() -> None:
    """Test 1: A posted message appears on the author's timeline"""
    from datetime import datetime

    from social_network import SocialNetwork

    network = SocialNetwork(clock=lambda: datetime(2026, 1, 1, 12, 0))
    network.post("Alice", "What a wonderfully sunny day!")

    assert network.timeline("Alice") == ["What a wonderfully sunny day!"]


def test_timeline_excludes_other_users_posts() -> None:
    """Test 2: A timeline lists only the requested user's own posts"""
    from datetime import datetime

    from social_network import SocialNetwork

    network = SocialNetwork(clock=lambda: datetime(2026, 1, 1, 12, 0))
    network.post("Alice", "Alice's post")
    network.post("Bob", "Bob's post")

    assert network.timeline("Alice") == ["Alice's post"]


def test_timeline_is_most_recent_first() -> None:
    """Test 3: Timeline messages are ordered most recent first"""
    from datetime import datetime, timedelta

    from social_network import SocialNetwork

    now = [datetime(2026, 1, 1, 12, 0)]
    network = SocialNetwork(clock=lambda: now[0])
    network.post("Alice", "first post")
    now[0] += timedelta(minutes=5)
    network.post("Alice", "second post")
    now[0] += timedelta(minutes=5)
    network.post("Alice", "third post")

    assert network.timeline("Alice") == ["third post", "second post", "first post"]


def test_timeline_of_user_without_posts_is_empty() -> None:
    """Test 4: A user who has never posted has an empty timeline"""
    from datetime import datetime

    from social_network import SocialNetwork

    network = SocialNetwork(clock=lambda: datetime(2026, 1, 1, 12, 0))

    assert network.timeline("Ghost") == []


def test_users_have_independent_timelines() -> None:
    """Test 5: Each user's timeline holds only their own messages"""
    from datetime import datetime, timedelta

    from social_network import SocialNetwork

    now = [datetime(2026, 1, 1, 12, 0)]
    network = SocialNetwork(clock=lambda: now[0])
    network.post("Alice", "sunny day")
    now[0] += timedelta(minutes=1)
    network.post("Bob", "rainy day")
    now[0] += timedelta(minutes=1)
    network.post("Alice", "picnic time")

    assert network.timeline("Alice") == ["picnic time", "sunny day"]
    assert network.timeline("Bob") == ["rainy day"]


def test_wall_shows_own_posts_with_author_prefix() -> None:
    """Test 6: A wall entry is formatted as 'author: message'"""
    from datetime import datetime

    from social_network import SocialNetwork

    network = SocialNetwork(clock=lambda: datetime(2026, 1, 1, 12, 0))
    network.post("Alice", "What a wonderfully sunny day!")

    assert network.wall("Alice") == ["Alice: What a wonderfully sunny day!"]


def test_wall_includes_followed_users_posts() -> None:
    """Test 7: After following a user, their posts appear on the follower's wall"""
    from datetime import datetime

    from social_network import SocialNetwork

    network = SocialNetwork(clock=lambda: datetime(2026, 1, 1, 12, 0))
    network.post("Alice", "What a wonderfully sunny day!")
    network.follow("Charlie", "Alice")

    assert network.wall("Charlie") == ["Alice: What a wonderfully sunny day!"]


def test_wall_aggregates_own_and_followed_posts_most_recent_first() -> None:
    """Test 8: A wall merges own posts and all followed users' posts in
    reverse chronological order"""
    from datetime import datetime, timedelta

    from social_network import SocialNetwork

    now = [datetime(2026, 1, 1, 9, 0)]
    network = SocialNetwork(clock=lambda: now[0])
    network.post("Alice", "sunny day")
    now[0] += timedelta(minutes=10)
    network.post("Charlie", "off to the gym")
    now[0] += timedelta(minutes=10)
    network.post("Bob", "coffee break")
    network.follow("Charlie", "Alice")
    network.follow("Charlie", "Bob")

    assert network.wall("Charlie") == [
        "Bob: coffee break",
        "Charlie: off to the gym",
        "Alice: sunny day",
    ]


def test_wall_excludes_posts_from_unfollowed_users() -> None:
    """Test 9: Posts from users who are not followed stay off the wall"""
    from datetime import datetime

    from social_network import SocialNetwork

    network = SocialNetwork(clock=lambda: datetime(2026, 1, 1, 12, 0))
    network.post("Alice", "hello")
    network.post("Bob", "hi there")
    network.follow("Charlie", "Alice")

    assert network.wall("Charlie") == ["Alice: hello"]


def test_following_is_one_directional() -> None:
    """Test 10: Following does not make the follower's posts visible to the followee"""
    from datetime import datetime

    from social_network import SocialNetwork

    network = SocialNetwork(clock=lambda: datetime(2026, 1, 1, 12, 0))
    network.post("Charlie", "I follow Alice")
    network.follow("Charlie", "Alice")

    assert network.wall("Alice") == []


def test_duplicate_follow_does_not_duplicate_wall_entries() -> None:
    """Test 11: Following the same user twice yields no duplicate wall entries"""
    from datetime import datetime

    from social_network import SocialNetwork

    network = SocialNetwork(clock=lambda: datetime(2026, 1, 1, 12, 0))
    network.post("Alice", "hello")
    network.follow("Charlie", "Alice")
    network.follow("Charlie", "Alice")

    assert network.wall("Charlie") == ["Alice: hello"]


def test_wall_of_unknown_user_is_empty() -> None:
    """Test 12: A user with no posts and no follows has an empty wall"""
    from datetime import datetime

    from social_network import SocialNetwork

    network = SocialNetwork(clock=lambda: datetime(2026, 1, 1, 12, 0))
    network.post("Alice", "hello")

    assert network.wall("Ghost") == []


def test_posts_with_equal_timestamps_show_latest_posted_first() -> None:
    """Test 13: Posts sharing a timestamp are ordered by recency of posting"""
    from datetime import datetime

    from social_network import SocialNetwork

    network = SocialNetwork(clock=lambda: datetime(2026, 1, 1, 12, 0))
    network.post("Alice", "first")
    network.post("Alice", "second")

    assert network.timeline("Alice") == ["second", "first"]


def test_mention_places_post_on_mentioned_users_wall() -> None:
    """Test 14: A mentioned user sees the post on their wall without following"""
    from datetime import datetime

    from social_network import SocialNetwork

    network = SocialNetwork(clock=lambda: datetime(2026, 1, 1, 12, 0))
    network.post("Bob", "@Charlie what are your plans tonight?")

    assert network.wall("Charlie") == ["Bob: @Charlie what are your plans tonight?"]


def test_mention_with_trailing_punctuation_is_recognised() -> None:
    """Test 15: Punctuation directly after a mention does not break it"""
    from datetime import datetime

    from social_network import SocialNetwork

    network = SocialNetwork(clock=lambda: datetime(2026, 1, 1, 12, 0))
    network.post("Alice", "great game, @Dave!")

    assert network.wall("Dave") == ["Alice: great game, @Dave!"]


def test_mention_does_not_appear_on_mentioned_users_timeline() -> None:
    """Test 16: Mentions affect walls only, never the mentioned user's timeline"""
    from datetime import datetime

    from social_network import SocialNetwork

    network = SocialNetwork(clock=lambda: datetime(2026, 1, 1, 12, 0))
    network.post("Bob", "@Charlie what are your plans tonight?")

    assert network.timeline("Charlie") == []


def test_direct_message_is_delivered_to_recipient() -> None:
    """Test 17: A direct message shows in the recipient's inbox as 'sender: message'"""
    from datetime import datetime

    from social_network import SocialNetwork

    network = SocialNetwork(clock=lambda: datetime(2026, 1, 1, 12, 0))
    network.send_direct_message("Mallory", "Alice", "meet me at noon")

    assert network.direct_messages("Alice") == ["Mallory: meet me at noon"]


def test_direct_messages_are_most_recent_first() -> None:
    """Test 18: The inbox lists direct messages most recent first"""
    from datetime import datetime, timedelta

    from social_network import SocialNetwork

    now = [datetime(2026, 1, 1, 12, 0)]
    network = SocialNetwork(clock=lambda: now[0])
    network.send_direct_message("Mallory", "Alice", "first note")
    now[0] += timedelta(minutes=3)
    network.send_direct_message("Bob", "Alice", "second note")

    assert network.direct_messages("Alice") == [
        "Bob: second note",
        "Mallory: first note",
    ]


def test_direct_messages_are_private() -> None:
    """Test 19: Direct messages never appear on timelines or walls"""
    from datetime import datetime

    from social_network import SocialNetwork

    network = SocialNetwork(clock=lambda: datetime(2026, 1, 1, 12, 0))
    network.send_direct_message("Mallory", "Alice", "secret plan")

    assert network.timeline("Mallory") == []
    assert network.timeline("Alice") == []
    assert network.wall("Alice") == []
    assert network.wall("Mallory") == []


def test_empty_inbox_returns_empty_list() -> None:
    """Test 20: A user who received no direct messages has an empty inbox"""
    from datetime import datetime

    from social_network import SocialNetwork

    network = SocialNetwork(clock=lambda: datetime(2026, 1, 1, 12, 0))

    assert network.direct_messages("Alice") == []


def test_ordering_follows_clock_timestamps_not_insertion_order() -> None:
    """Test 21: Recency comes from the injected clock's timestamps, so a post
    stamped earlier lists after one stamped later even if posted afterwards"""
    from datetime import datetime, timedelta

    from social_network import SocialNetwork

    now = [datetime(2026, 1, 1, 12, 0)]
    network = SocialNetwork(clock=lambda: now[0])
    network.post("Alice", "stamped noon")
    now[0] -= timedelta(minutes=5)
    network.post("Alice", "stamped before noon")

    assert network.timeline("Alice") == ["stamped noon", "stamped before noon"]
