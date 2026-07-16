"""In-memory social network kata.

Requirements summary (paraphrased): users interact with a console-style social
network where accounts come into existence the first time they act. A user can
publish messages to a personal timeline; anyone can read any user's timeline,
which lists only that user's own messages, most recent first. A user can follow
other users, and their wall aggregates their own posts plus the posts of
everyone they follow, most recent first, each entry prefixed with its author.
Mentioning a user with an ``@name`` token inside a post makes the post appear
on the mentioned user's wall even without a follow relationship. Users can
also exchange direct messages, which are private: they are visible only in the
recipient's inbox and never on timelines or walls. All timestamps come from an
injected clock so behaviour is deterministic.

Kata catalogued at tddbuddy.com/katas/social-network; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Callable

Clock = Callable[[], datetime]

_TRAILING_PUNCTUATION = ".,!?;:"


@dataclass(frozen=True)
class _Post:
    author: str
    message: str
    timestamp: datetime
    sequence: int


class SocialNetwork:
    """Social network with timelines, walls, follows, mentions and DMs."""

    def __init__(self, clock: Clock) -> None:
        self._clock = clock
        self._posts: list[_Post] = []
        self._following: dict[str, set[str]] = {}
        self._inboxes: dict[str, list[_Post]] = {}
        self._sequence = 0

    def post(self, author: str, message: str) -> None:
        """Publish ``message`` to ``author``'s personal timeline."""
        self._posts.append(self._new_post(author, message))

    def timeline(self, user: str) -> list[str]:
        """Return ``user``'s own messages, most recent first."""
        own = [post for post in self._posts if post.author == user]
        return [post.message for post in _newest_first(own)]

    def follow(self, follower: str, followee: str) -> None:
        """Subscribe ``follower`` to ``followee``'s posts."""
        self._following.setdefault(follower, set()).add(followee)

    def wall(self, user: str) -> list[str]:
        """Return ``"author: message"`` entries visible to ``user``.

        A post is visible on the wall when ``user`` wrote it, follows its
        author, or is mentioned in it. Entries are most recent first.
        """
        followed = self._following.get(user, set())
        visible = [
            post
            for post in self._posts
            if post.author == user
            or post.author in followed
            or user in _mentions(post.message)
        ]
        return [f"{post.author}: {post.message}" for post in _newest_first(visible)]

    def send_direct_message(self, sender: str, recipient: str, message: str) -> None:
        """Deliver a private message from ``sender`` to ``recipient``."""
        self._inboxes.setdefault(recipient, []).append(self._new_post(sender, message))

    def direct_messages(self, user: str) -> list[str]:
        """Return ``user``'s inbox as ``"sender: message"``, most recent first."""
        inbox = self._inboxes.get(user, [])
        return [f"{post.author}: {post.message}" for post in _newest_first(inbox)]

    def _new_post(self, author: str, message: str) -> _Post:
        self._sequence += 1
        return _Post(author, message, self._clock(), self._sequence)


def _newest_first(posts: list[_Post]) -> list[_Post]:
    return sorted(posts, key=lambda post: (post.timestamp, post.sequence), reverse=True)


def _mentions(message: str) -> set[str]:
    names: set[str] = set()
    for token in message.split():
        if token.startswith("@"):
            name = token[1:].rstrip(_TRAILING_PUNCTUATION)
            if name:
                names.add(name)
    return names
