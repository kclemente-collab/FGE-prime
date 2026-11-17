# FGE signal emitters v0.1.0

Installation scope: ten on-demand event-family profiles from FGE-COMPILER-SIGNAL-EMISSION-REGISTRY-001 v0.1.0 section 12. This is a new adapter to the existing LARA bus; it does not replace bus.py or create another canonical ledger.

Source: https://docs.google.com/document/d/1bVfwfmBnjdZjHkB85EeSBKSU9QA0KSbjj1flpX7cnbE/edit

Run `python journalist/signal_bus/emitters.py catalog` for supported event types.
Run `python journalist/signal_bus/emitters.py prepare --event event.json` to inspect the native bus dispatch.
Run `python journalist/signal_bus/emitters.py emit --event event.json` to append and fsync to the existing local dispatch register.
Commit the changed register through the authorized repository workflow to reach GitHub. The existing bus workflow processes that register. Local append alone is not remote delivery.

Every event requires family, event_type, event_id, source_id, source_locator, source_version (UNKNOWN permitted), object_id, observation, why_it_matters, privacy_scope, classification, nonempty evidence_refs and route_to arrays, and occurred_at (timezone timestamp or explicit null). Preserve unknown timestamps and source hashes. Caller supplies evidence, routes and scope; this adapter does not authenticate source assertions. Unrecognized fields survive under original_event. Actual authorization of the caller belongs to the host runtime.

Duplicate event identity and identical bytes reuse the ingress record. Changed bytes under the same family/source/event ID raise IDEMPOTENCY_CONFLICT. Malformed existing ingress stops appends. POSIX advisory locking coordinates cooperating local emitter writers only; repository write concurrency still requires commit/rebase controls. Existing bus crash recovery limitations are unchanged.

All ten source producer hooks remain UNBOUND until installed inside the actual producers. Drive/GitHub/Notion subscriptions, automatic polling, renderer hooks and commercial release hooks are not activated by this file. No broad network discovery or broadcasts. No automatic canon changes, authority changes, receiver acknowledgments or verified source claims. No daemon installed on the iPhone.

Validation: `python -m unittest discover -s journalist/signal_bus -p test_emitters.py -v`. Ten synthetic families pass through the unmodified existing bus; replay emits zero duplicates. Negative cases cover conflicting event replay, malformed input, authority effects and corrupted ingress. Synthetic results are not live receiver proof.

Rollback: remove emitters.py and test_emitters.py and revert the emitter-test workflow step. Retain already appended records as history; correct them by new events rather than deletion.
