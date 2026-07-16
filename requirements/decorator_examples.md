# Function decoration: registration and result stringification

## Overview
A registration facility in which functions are enrolled at decoration time: marking a function records its activation status on the function itself and, when the function is active, adds it to a shared collection of registered functions. Registration can be declined by turning the activation flag off, in which case the function is marked inactive and stays out of the collection. Three sample subject functions ship with the package to demonstrate the pattern out of the box.
The package also provides a result-stringification facility: arithmetic helpers whose numeric
results are converted to their text form on the way out, without disturbing the underlying
calculation or the functions' published metadata.

## User Stories

### US-1: Mark functions with their activation status
As a developer, I want every decorated function to carry its activation status, so that I can see at a glance whether a function is active.

- AC-1.1: A decorated function carries a status attribute.
- AC-1.2: With default settings, the recorded status is exactly "active".
- AC-1.3: When the activation flag is turned off at decoration time, the recorded status is exactly "inactive".
- AC-1.4: Status values are exact, lowercase, undecorated strings.

### US-2: Collect active functions in a shared registry
As a developer, I want active functions gathered into one shared collection, so that the application can discover them.

- AC-2.1: A function decorated as active is added to the shared collection of registered functions.
- AC-2.2: A function decorated as inactive is not added to the collection.
- AC-2.3: The collection holds the function objects themselves, never a placeholder.
- AC-2.4: Decoration returns the very same function object, unchanged.
- AC-2.5: Decorated functions remain callable and behave as they did before decoration.

### US-3: Sample subjects demonstrate the pattern
As a learner, I want ready-made sample functions exercising both settings, so that the registration behavior is observable without writing any code.

- AC-3.1: The first sample subject is active and enrolled in the collection.
- AC-3.2: The second sample subject is inactive and stays out of the collection.
- AC-3.3: The collection contains exactly the first and third sample subjects, and nothing else.
- AC-3.4: All three sample subjects are callable and return nothing.
- AC-3.5: The samples carry exact statuses: the first and third are "active", the second is "inactive".


### US-4: Convert function results to text
As a developer, I want designated functions' return values converted to their text form, so that callers always receive strings.

- AC-4.1: A converted function returns a string.
- AC-4.2: The underlying calculation is preserved: the text is exactly the usual result (adding 5 and 6 yields "11"; multiplying them yields "30").
- AC-4.3: The conversion applies the standard text form of whatever the function returns.
- AC-4.4: A converted function keeps its published name and description metadata.

## Traceability
```json
{
  "test_subject_1_is_decorated": [
    "AC-1.1"
  ],
  "test_subject_1_is_registered": [
    "AC-2.1",
    "AC-3.1"
  ],
  "test_subject_1_is_active": [
    "AC-1.2",
    "AC-3.5"
  ],
  "test_subject_2_is_decorated": [
    "AC-1.1"
  ],
  "test_subject_2_is_not_registered": [
    "AC-2.2",
    "AC-3.2"
  ],
  "test_subjects_are_callable": [
    "AC-2.5",
    "AC-3.4"
  ],
  "test_register_default_marks_active_and_adds_to_registered": [
    "AC-1.2",
    "AC-2.1",
    "AC-2.3",
    "AC-2.4"
  ],
  "test_register_inactive_marks_inactive_and_does_not_register": [
    "AC-1.3",
    "AC-2.2",
    "AC-2.4"
  ],
  "test_registered_contains_exactly_the_active_subjects": [
    "AC-3.3"
  ],
  "test_module_level_subjects_have_exact_status_values": [
    "AC-1.4",
    "AC-3.5"
  ],
  "test_add_returns_string": [
    "AC-4.1"
  ],
  "test_add_does_right_calculation": [
    "AC-4.2"
  ],
  "test_multiply_returns_string": [
    "AC-4.1"
  ],
  "test_add_returns_exact_string_result": [
    "AC-4.2"
  ],
  "test_multiply_returns_exact_string_result": [
    "AC-4.2"
  ],
  "test_stringify_converts_any_result_to_its_str_form": [
    "AC-4.3"
  ],
  "test_stringify_preserves_function_metadata": [
    "AC-4.4"
  ]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
