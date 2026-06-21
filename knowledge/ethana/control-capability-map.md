# Ethana Control-to-Capability Map

**Authority:** Authoritative source for regulatory control-to-Ethana-capability attribution.
**Maintained by:** Cursory Governance Team
**Synchronized with:** knowledge/ethana/canonical-product-model.md
**CPM key format:** Lowercase base name as returned by parse_canonical_model()
**Control name contract:** The `Control Name` column is a shared string contract with
  `execute_regulatory_mapping()` in the RWA executor. Values must match Skill 1 output
  exactly (modulo case). Any change to Skill 1 control name literals requires a simultaneous
  update to this file. T6(e) enforces this contract in CI.

---

## Format Notes

- `Primary Capability`: The CPM key of the Ethana capability that is the primary implementation
  of this regulatory control. Must match a key returned by parse_canonical_model() exactly.
  Empty string if no Ethana capability is the primary implementation.
- `Phase B: Secondary Capabilities`: Comma-separated CPM keys for supporting capabilities.
  Pre-populate with full knowledge on Day 1. The Phase A loader reads this column but does not
  consume it — the loader always returns `"secondary": []` regardless of column content in Phase A.
  Complete knowledge belongs in the file from the start; which columns the code consumes is a code
  concern, not a knowledge concern.
- `Notes`: Compliance rationale. Must reference CPM primary source notes where relevant.

---

## Control-to-Capability Mappings

| Control Name | Framework Reference | Primary Capability | Phase B: Secondary Capabilities | Notes |
|---|---|---|---|---|
| Human Oversight Gate | EU AI Act Art.14 | immutable audit log | | Audit Log provides the tamper-proof record for every human-override decision on AI output. CPM: "Every [BB] production scenario references it." |
| Drift Monitoring | EU AI Act Art.72; ISO 42001 Annex A.9 | immutable audit log | | Gateway telemetry (logged to Audit Log) is the primary detection source for performance drift. Alerting thresholds are customer-configured against the log export. |
| Fairness and Bias Monitoring | FCA PRIN 12; Equality Act 2010 | runtime guardrails | immutable audit log | Guardrails bias scanner is the primary detection mechanism. CPM mandatory caveat: runtime text filter only; does not audit model weights or test disparate impact across demographic groups. EU AI Act Art.10 bias audit obligations cannot be met by this scanner alone. |
| Prompt Injection Filter | OWASP LLM01; NIST AI RMF | runtime guardrails | | Guardrails prompt injection and jailbreak detection scanners are the primary prevention mechanism. CPM: "One of six confirmed native scanners." |
| Consent Verification | DPDP Act 2023 §6 | | | No primary Ethana capability. Customer-owned control; consent database is customer infrastructure. Cursory advisory service for consent architecture design. |
| Vendor Risk Assessment | RBI IT Governance MD 2023 | | | No primary Ethana capability. Customer-owned process control. Cursory advisory service for supply-chain risk assessment. |
