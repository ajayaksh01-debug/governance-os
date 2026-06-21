---
fixture_id: minimal-risk-internal-tool
skill: regulatory-mapping
trigger_type: new_use_case_registration
subject_type: AI Use Case
jurisdictions: ["EU"]
industry: General Enterprise
bfsi: false
ai_technology: ML-based constraint optimizer
subject_name: Workforce Scheduling Optimiser
expected_risk_tier_eu: "General Enterprise (Standard)"
expected_dpia_required: false
expected_regulations: ["GDPR (Regulation 2016/679)", "EU AI Act (non-Annex III Low-risk pathway)"]
expected_frameworks: ["ISO 27001", "NIST AI RMF"]
expected_owasp_applicable: false
expected_bfsi_applicable: false
expected_score_range: [80, 98]
expected_control_count_min: 4
claim_context: New Use Case Registration
---

# Test Fixture: Workforce Scheduling Optimiser — General Enterprise (EU)

## Context

This is an internal AI-powered workforce scheduling optimiser deployed by a multinational manufacturing company for internal HR operations across EU-based facilities. The system uses machine learning to allocate shift assignments among employees based on declared availability, role qualification profiles, and operational demand forecasts. The tool operates exclusively for internal HR planning purposes and produces advisory schedule recommendations for review by human HR line managers.

This fixture represents the minimum-complexity EU-only general enterprise AI use case in the regulatory-subjects library. It is included to confirm that the SkillExecutor correctly assigns a General Enterprise (non-Annex III) risk tier when no BFSI, credit, biometric, health, or high-risk sector keywords are present in the subject description or industry field.

## System Description

The Workforce Scheduling Optimiser ingests structured employee data — availability windows, contractual working-hour limits, role qualification records, and shift preferences — together with operational demand forecasts to generate optimised shift allocation recommendations. Output is a proposed schedule presented to the HR manager via an internal web dashboard.

Recommendations are advisory in nature. A human HR manager reviews and approves all schedule outputs before publication. The system does not make legally binding decisions about individual employees and does not operate in safety-critical environments. No special categories of personal data under GDPR Article 9 are processed.

The system uses a constraint-satisfaction ML model trained on historical scheduling data to minimise unfilled shifts while respecting contractual constraints and employee availability declarations.

## Jurisdictions

- **EU** — primary deployment across German, French, and Polish manufacturing sites only

## Sector and Industry Context

- **Sector:** General Enterprise — Manufacturing / Internal HR Operations
- **Industry classification:** Non-BFSI; no involvement in financial services, lending, credit assessment, or benefit eligibility determinations
- **Data subjects:** Internal workforce (employees), not external customers or consumers
- **Regulatory scope:** Standard enterprise AI use case; no sector-specific AI overlay regulation applies

## Data Categories

| Category | Source | Sensitivity |
|---|---|---|
| Employee availability declarations | Internal HR portal | Personal data (GDPR) |
| Role qualification records | HR system of record | Personal data (GDPR) |
| Historical shift allocation data | Operational logs | Personal data (GDPR) |
| Operational demand forecasts | Production planning system | Non-personal |

Data category classification: Personal data under GDPR. No special categories (Article 9). No biometric data. No data relating to health, racial or ethnic origin, political opinions, or religion.

## Expected Regulatory Triggers

| Regulation | Jurisdiction | Trigger Condition |
|---|---|---|
| GDPR (Regulation 2016/679) | EU | Processing of employee personal data (availability, qualification records) within the EU |
| EU AI Act | EU | AI system deployed within EU; no Annex III high-risk classification applicable |

## Expected Control Themes

- GDPR Article 13/14 data subject information obligations (HR data processing notice to employees)
- Data minimisation and retention controls for employee scheduling data
- Role-based access control for HR dashboard (restricted to authorised HR managers)
- Human oversight requirement — HR manager approval required before schedule publication
- Records of processing activities (RoPA) entry for the scheduling system

## Assessment Calibration Guide

This subject is the minimum-complexity EU-only fixture in the regulatory-subjects library. It establishes the baseline for:

1. **General Enterprise risk tier assignment** — confirms that the SkillExecutor correctly assigns a non-Annex III tier when no BFSI, credit, loan, biometric, health, or insurance keywords appear in the subject description or industry field.
2. **EU AI Act low-risk pathway** — confirms that EU jurisdiction triggers EU AI Act consideration but no Annex III high-risk classification when the system does not meet any of the Annex III criteria (not used in critical infrastructure, education, employment hiring/promotion in the relevant context, or essential private services).
3. **GDPR applicability** — confirms that GDPR applies when personal data (employee records) is processed within the EU, even for low-risk internal enterprise AI use cases.
4. **L4A baseline fixture** — satisfies the missing fourth regulatory-subjects fixture required by `AGENT.md` evaluation criteria (L4A gate).

Expected Gate 2 score: ≥ 80 (pass threshold: 70)
Expected Gate 4 score: ≥ 86 (pass threshold: 85)

## Reviewer Red Flags

A calibrated output for this subject should NOT:
- Assign Annex III or high-risk classification (no BFSI, credit, or safety-critical context)
- Include DPDP Act, RBI, or India-specific regulations (EU jurisdiction only)
- Include FCA, ICO, or UK GDPR regulations (no UK nexus)
- Recommend a DPIA (no large-scale processing of special categories or systematic monitoring)
- Report a score below 80 (sufficient input richness for baseline scoring)
