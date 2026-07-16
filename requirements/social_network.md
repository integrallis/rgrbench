# Social networking timelines, walls, mentions, and direct messages

## Overview
A small social network in the spirit of the console-era kata. Members publish short messages to a personal timeline, follow other members to aggregate posts on a wall, reach non-followers by mentioning them by name inside a post, and exchange private direct messages. Recency comes from timestamps taken from a clock the network is given, so ordering is deterministic.

## User Stories

### US-1: Publishing to a personal timeline
As a member, I want my posts collected on my own timeline, so that anyone can read what I have said.

- AC-1.1: A posted message appears on its author's timeline.
- AC-1.2: A timeline lists only that member's own posts; different members' timelines are independent.
- AC-1.3: A timeline is ordered most recent first.
- AC-1.4: A member who has never posted has an empty timeline.

### US-2: Following members and reading a wall
As a member, I want a wall that merges my posts with those of everyone I follow, so that I can catch up in one place.

- AC-2.1: A wall entry is formatted as the author's name, a colon and a space, then the message — for example "Alice: What a wonderfully sunny day!".
- AC-2.2: After following a member, that member's posts appear on the follower's wall.
- AC-2.3: A wall merges the member's own posts with all followed members' posts, most recent first.
- AC-2.4: Posts by members who are not followed stay off the wall.
- AC-2.5: Following is one-directional: the follower's posts do not appear on the followed member's wall.
- AC-2.6: Following the same member twice creates no duplicate wall entries.
- AC-2.7: A member with no posts and no follows has an empty wall.

### US-3: Reaching members through mentions
As a member, I want to flag a post to someone by mentioning them, so that they see it without having to follow me.

- AC-3.1: A post containing an at-sign directly before a member's name lands on that member's wall even though they follow no one.
- AC-3.2: Punctuation immediately after a mention does not break it.
- AC-3.3: Mentions affect walls only: the post never appears on the mentioned member's timeline.

### US-4: Exchanging direct messages
As a member, I want private direct messages, so that some conversations stay out of public view.

- AC-4.1: A direct message is delivered to the recipient's inbox, formatted as the sender's name, a colon and a space, then the message.
- AC-4.2: An inbox lists direct messages most recent first.
- AC-4.3: Direct messages are private: they never appear on any timeline or wall, neither the sender's nor the recipient's.
- AC-4.4: A member who has received no direct messages has an empty inbox.

### US-5: Ordering everything by the clock
As a member, I want recency decided by timestamps, so that feeds read newest first even when the clock behaves oddly.

- AC-5.1: Recency comes from the supplied clock's timestamps rather than insertion order: an entry stamped earlier lists after one stamped later, even if it was posted afterwards.
- AC-5.2: Entries sharing the same timestamp are ordered latest-posted first.

## Traceability
```json
{
  "test_posted_message_appears_on_own_timeline": ["AC-1.1"],
  "test_timeline_excludes_other_users_posts": ["AC-1.2"],
  "test_timeline_is_most_recent_first": ["AC-1.3"],
  "test_timeline_of_user_without_posts_is_empty": ["AC-1.4"],
  "test_users_have_independent_timelines": ["AC-1.2", "AC-1.3"],
  "test_wall_shows_own_posts_with_author_prefix": ["AC-2.1"],
  "test_wall_includes_followed_users_posts": ["AC-2.2"],
  "test_wall_aggregates_own_and_followed_posts_most_recent_first": ["AC-2.3"],
  "test_wall_excludes_posts_from_unfollowed_users": ["AC-2.4"],
  "test_following_is_one_directional": ["AC-2.5"],
  "test_duplicate_follow_does_not_duplicate_wall_entries": ["AC-2.6"],
  "test_wall_of_unknown_user_is_empty": ["AC-2.7"],
  "test_posts_with_equal_timestamps_show_latest_posted_first": ["AC-5.2"],
  "test_mention_places_post_on_mentioned_users_wall": ["AC-3.1"],
  "test_mention_with_trailing_punctuation_is_recognised": ["AC-3.2"],
  "test_mention_does_not_appear_on_mentioned_users_timeline": ["AC-3.3"],
  "test_direct_message_is_delivered_to_recipient": ["AC-4.1"],
  "test_direct_messages_are_most_recent_first": ["AC-4.2"],
  "test_direct_messages_are_private": ["AC-4.3"],
  "test_empty_inbox_returns_empty_list": ["AC-4.4"],
  "test_ordering_follows_clock_timestamps_not_insertion_order": ["AC-5.1"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
