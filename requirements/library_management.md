# Community library circulation

## Overview
A circulation system for a lending library. Librarians maintain a catalogue of titles and the physical copies on the shelves; registered members check copies out, return them (paying a fine when late), and reserve titles that are unavailable. Returned copies go to reservers first, held for a limited time and handed over first-come first-served, with members notified when a copy becomes theirs to collect.

## User Stories

### US-1: Catalogue and inventory
As a librarian, I want to manage titles and their physical copies, so that the collection is accurately tracked.

- AC-1.1: A newly added copy of a title is available.
- AC-1.2: A title can have several copies, each tracked individually, and the count of available copies reflects all of them.
- AC-1.3: The catalogue records each title's ISBN, title, category and shelf location, retrievable together.
- AC-1.4: Copy identifiers combine the ISBN with a 1-based sequence number: the first copy of ISBN 978-1 is "978-1/1" and the second is "978-1/2".
- AC-1.5: Asking the status of an unknown copy identifier is refused with an error naming that identifier.
- AC-1.6: An available copy can be removed from the inventory, shrinking the available count.
- AC-1.7: A checked-out copy cannot be removed; the attempt is refused with a message saying the copy is "not available for removal".

### US-2: Checkout
As a member, I want to borrow an available copy of a title, so that I can read it at home.

- AC-2.1: A checkout lends one available copy of the requested title to the member and sets the due date to the checkout day plus the loan period.
- AC-2.2: The loan period defaults to fourteen days when not configured.
- AC-2.3: A checked-out copy leaves the available pool; its status is "checked_out".
- AC-2.4: A checkout finds an available copy of the title even when other copies of the same title are checked out.
- AC-2.5: Checking out a title with no free copies is refused with an error stating "No copies of" the requested ISBN are available.
- AC-2.6: Checking out an ISBN that is not in the catalogue is refused with an unknown-book error naming the ISBN.
- AC-2.7: A checkout by an unregistered member is refused with an unknown-member error naming the member.

### US-3: Returns and fines
As a librarian, I want returns processed with fair late fines, so that copies circulate on time.

- AC-3.1: A return on or before the due date costs nothing.
- AC-3.2: A late return owes the configured per-day fine multiplied by the number of days overdue (for example, at 0.50 per day, three days late owes 1.50).
- AC-3.3: A returned copy is available again and can be checked out by another member.
- AC-3.4: Returning a copy that is not checked out is refused with a message saying it is "not checked out".

### US-4: Reservations and holds
As a member, I want to reserve a title that is unavailable, so that I get the next returned copy.

- AC-4.1: When a copy of a reserved title is returned, the first member in the reservation queue is notified and the copy is held for them, with status "reserved".
- AC-4.2: A copy held under a reservation cannot be checked out by any other member; to everyone else the title has no available copies.
- AC-4.3: The reserving member can check out the copy held for them, which then becomes a normal loan.
- AC-4.4: The reservation queue serves members first-come first-served: each returned copy goes to the earliest remaining reserver, in order.
- AC-4.5: Reserving a title while a copy sits on the shelf claims that copy immediately: it is held, leaves the available pool, and the member is notified at once.
- AC-4.6: A member cannot reserve the same title twice — whether still queued or already holding a copy; the attempt is refused with a duplicate-reservation error saying the member "already has a reservation".
- AC-4.7: A copy held for one member does not prevent another member from placing their own reservation for the same title.
- AC-4.8: A member collects the specific copy held for them even when a different copy of the title is held for someone else.

### US-5: Cancellations and hold expiry
As a librarian, I want holds to be cancellable and to lapse when uncollected, so that copies do not sit idle.

- AC-5.1: A cancelled queued reservation is never served: when a copy comes back it goes to the shelf (or the next reserver), and the cancelled member is not notified.
- AC-5.2: Cancelling a reservation after its hold was granted releases the held copy back to availability.
- AC-5.3: Cancelling a reservation the member does not have is refused with an error stating that the member has no reservation for that ISBN.
- AC-5.4: A member cannot cancel a hold granted to someone else; the attempt is refused and the hold stays in place for its owner.
- AC-5.5: An uncollected hold lapses once the hold period has fully passed: on the last day of the period the copy is still held, and the day after it is available again.
- AC-5.6: The hold period defaults to three days when not configured.
- AC-5.7: When a hold lapses and other reservers are queued, the next member is notified and the copy is held for them instead of returning to the shelf.

## Traceability
```json
{
  "test_added_copy_is_available": ["AC-1.1"],
  "test_multiple_copies_of_the_same_title_are_tracked": ["AC-1.2"],
  "test_book_info_keeps_category_and_location": ["AC-1.3"],
  "test_checkout_sets_due_date_from_loan_period": ["AC-2.1"],
  "test_checkout_marks_the_copy_checked_out": ["AC-2.3"],
  "test_checkout_without_available_copies_is_refused": ["AC-2.5"],
  "test_checkout_of_unregistered_book_is_refused": ["AC-2.6"],
  "test_checkout_by_unregistered_member_is_refused": ["AC-2.7"],
  "test_return_on_or_before_the_due_date_costs_nothing": ["AC-3.1"],
  "test_late_return_incurs_a_per_day_fine": ["AC-3.2"],
  "test_returned_copy_is_available_again": ["AC-3.3"],
  "test_returning_a_copy_that_is_not_checked_out_is_refused": ["AC-3.4"],
  "test_available_copy_can_be_removed": ["AC-1.6"],
  "test_checked_out_copy_cannot_be_removed": ["AC-1.7"],
  "test_return_hands_the_copy_to_the_first_reserver_and_notifies": ["AC-4.1"],
  "test_held_copy_cannot_be_checked_out_by_another_member": ["AC-4.2"],
  "test_holder_can_check_out_the_held_copy": ["AC-4.3"],
  "test_reservation_queue_serves_members_in_order": ["AC-4.4"],
  "test_reserving_an_available_copy_holds_it_immediately": ["AC-4.5"],
  "test_cancelled_queued_reservation_is_not_served": ["AC-5.1"],
  "test_cancelling_an_active_hold_releases_the_copy": ["AC-5.2"],
  "test_cancelling_a_nonexistent_reservation_is_refused": ["AC-5.3"],
  "test_hold_lapses_after_the_hold_period": ["AC-5.5"],
  "test_lapsed_hold_passes_to_the_next_reserver": ["AC-5.7"],
  "test_duplicate_reservation_is_refused": ["AC-4.6"],
  "test_default_loan_period_is_fourteen_days": ["AC-2.2"],
  "test_default_hold_period_is_three_days": ["AC-5.6"],
  "test_copy_ids_number_copies_of_a_title_sequentially": ["AC-1.4"],
  "test_querying_an_unknown_copy_id_is_refused": ["AC-1.5"],
  "test_second_copy_remains_available_when_the_first_is_checked_out": ["AC-2.4"],
  "test_holder_checks_out_their_copy_even_behind_anothers_hold": ["AC-4.8"],
  "test_cancelling_anothers_hold_is_refused_and_keeps_the_hold": ["AC-5.4"],
  "test_duplicate_reservation_while_holding_a_copy_is_refused": ["AC-4.6"],
  "test_second_member_can_reserve_while_a_copy_is_held_for_another": ["AC-4.7"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
