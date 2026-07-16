# Shared laundry room reservations

## Overview
A reservation service for a residential laundry room whose numbered washing machines are fitted with remotely controlled smart locks. A resident reserves a machine for a chosen time slot; the service picks a machine, issues an access PIN, confirms the booking by email, and engages the machine's lock. At the machine, the resident enters the PIN to claim the reservation and unlock the machine. Repeated wrong PIN entries trigger a security reset delivered by text message.

## User Stories

### US-1: Reserve a machine
As a resident, I want to reserve a laundry machine for a chosen time slot, so that a machine is guaranteed to be ready for me.

- AC-1.1: Creating a reservation assigns one machine from the room, identified by a machine number between 1 and the number of machines in the room (25 in the standard room).
- AC-1.2: Every reservation carries an access PIN of exactly five digits.
- AC-1.3: Every reservation carries a non-empty identifier of the form "RSV-" followed by eight uppercase hexadecimal digits; identifiers never collide.
- AC-1.4: A new reservation starts active and can be looked up by its identifier.
- AC-1.5: The reservation records exactly the slot date and time the resident asked for.
- AC-1.6: PINs are not confined near zero: across many reservations they are drawn from the full five-digit range.
- AC-1.7: Machine choice, PIN and identifier are drawn from a caller-supplied source of randomness, so two services supplied with identically seeded sources produce identical reservations.

### US-2: Confirmation and machine locking
As a resident, I want a confirmation message and a locked machine, so that only I can use the machine I reserved.

- AC-2.1: Exactly one confirmation email is sent to the resident's email address, and it contains the machine number, the reservation identifier and the PIN.
- AC-2.2: Creating the reservation engages the reserved machine's lock with the reservation identifier, the slot time and the PIN.
- AC-2.3: No machine other than the reserved one is touched while the reservation is created.

### US-3: Fair allocation
As a building manager, I want allocation rules enforced automatically, so that machines are shared fairly among residents.

- AC-3.1: A user may hold only one active reservation at a time; a second attempt is refused with a reservation error whose message is exactly "a user may only have a single active reservation at a time".
- AC-3.2: Two active reservations never share a machine: concurrent users each get a different machine.
- AC-3.3: When every machine is already reserved, a further reservation attempt is refused with a reservation error whose message is exactly "no machines available".

### US-4: Claim the machine with the PIN
As a resident, I want to unlock my reserved machine by entering my PIN at the machine, so that I can start my laundry.

- AC-4.1: Entering the correct PIN at the reserved machine succeeds: the claim is accepted, and the reservation is marked used and is no longer active.
- AC-4.2: A successful claim unlocks the machine.
- AC-4.3: Entering a wrong PIN is rejected: the reservation stays active and the machine stays locked.
- AC-4.4: Claiming a machine that has no reservation is rejected.
- AC-4.5: A reservation that has already been used no longer accepts its PIN.
- AC-4.6: Only active reservations count toward the one-per-user limit: after claiming, the same user may reserve again, receiving a fresh reservation with a different identifier.

### US-5: Five-attempt PIN reset
As a building manager, I want repeated failed PIN entries to trigger a PIN reset, so that guessing attacks are cut off while the resident keeps access.

- AC-5.1: The first four consecutive failed attempts change nothing: the PIN stays the same and no text message is sent.
- AC-5.2: On the fifth consecutive failed attempt a new PIN replaces the old one, and exactly one text message containing the new PIN is sent to the resident's cell phone number.
- AC-5.3: The reset re-engages the machine's lock with the same reservation identifier and slot time and the fresh PIN.
- AC-5.4: The regenerated PIN is accepted for claiming the reservation.
- AC-5.5: The failed-attempt count restarts after each reset: another five fresh failures are needed before the next reset and text message.

## Traceability
```json
{
  "test_reservation_assigns_a_machine_between_one_and_twenty_five": ["AC-1.1"],
  "test_reservation_generates_a_five_digit_pin": ["AC-1.2"],
  "test_reservation_has_an_id_and_is_active": ["AC-1.3", "AC-1.4"],
  "test_reservation_stores_the_injected_slot_time": ["AC-1.5"],
  "test_confirmation_email_contains_machine_id_and_pin": ["AC-2.1"],
  "test_lock_instruction_is_sent_to_the_reserved_machine": ["AC-2.2"],
  "test_only_the_reserved_machine_receives_a_lock": ["AC-2.3"],
  "test_user_cannot_hold_two_active_reservations": ["AC-3.1"],
  "test_different_users_get_different_machines": ["AC-3.2"],
  "test_no_machines_available_raises_reservation_error": ["AC-3.3"],
  "test_claim_with_correct_pin_succeeds_and_marks_reservation_used": ["AC-4.1"],
  "test_claim_with_correct_pin_unlocks_the_machine": ["AC-4.2"],
  "test_claim_with_wrong_pin_fails_and_keeps_reservation_active": ["AC-4.3"],
  "test_pin_is_unchanged_before_the_fifth_failed_attempt": ["AC-5.1"],
  "test_fifth_failed_attempt_texts_a_new_pin_to_the_patron": ["AC-5.2"],
  "test_fifth_failed_attempt_syncs_the_new_pin_to_the_machine_lock": ["AC-5.3"],
  "test_new_pin_claims_the_reservation_after_a_reset": ["AC-5.4"],
  "test_failed_attempt_counter_restarts_after_a_pin_reset": ["AC-5.5"],
  "test_claim_on_a_machine_without_a_reservation_fails": ["AC-4.4"],
  "test_used_reservation_cannot_be_claimed_again": ["AC-4.5"],
  "test_user_may_reserve_again_after_claiming": ["AC-4.6"],
  "test_same_seed_produces_the_same_machine_pin_and_id": ["AC-1.7"],
  "test_reservation_ids_are_eight_hex_digits_and_unique": ["AC-1.3"],
  "test_pins_are_five_digits_drawn_from_the_full_range": ["AC-1.2", "AC-1.6"],
  "test_double_booking_error_names_the_single_reservation_rule": ["AC-3.1"],
  "test_full_house_error_says_no_machines_available": ["AC-3.3"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
