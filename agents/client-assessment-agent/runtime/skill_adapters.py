#!/usr/bin/env python3
"""
Skill adapters for the Client Assessment Runtime (Option C).

Each adapter delegates to an existing, already-certified SkillExecutor class
from another runtime (the reusable *logic unit*), normalizing:
  - signature     (some source methods take state_mgr, some don't)
  - input fields  (CA intake vocabulary -> source executor vocabulary)
  - output fields (source key names -> CA envelope: quality_score / ecs /
                   pcs+ctcs+release_classification, plus markdown_output)

Adapters import source SkillExecutor *classes* only — never source Orchestrators.
Source modules are all named ``skill_executor`` and one lives in a hyphenated
directory, so each is loaded by file path under a unique module name via
importlib (avoids name collision and the non-importable hyphen path).

Adapters are pure I/O transformers. They never call ``state_mgr.transition_to``;
CA's orchestrator remains the sole owner of the state machine, gates, firewall,
and approvals.
"""

import importlib.util
from pathlib import Path

# agents/client-assessment-agent/runtime/skill_adapters.py -> repo root
REPO_ROOT = Path(__file__).resolve().parents[3]


class SkillAdapterError(Exception):
    """Raised for any adapter failure (import, execution, or contract violation).

    The orchestrator's per-skill try/except converts this to HALTED_ESCALATION,
    preserving the existing failure contract. Adapters never silently return a
    partial/defaulted payload — absence of a required field is an error.
    """


# ---------------------------------------------------------------------------
# Source-module loader (cached by absolute path)
# ---------------------------------------------------------------------------

_SOURCE_MODULE_CACHE: dict = {}


def _load_source_module(rel_path: str, module_alias: str):
    """Load a source runtime's skill_executor.py by file path under a unique alias."""
    abs_path = REPO_ROOT / rel_path
    cache_key = str(abs_path)
    if cache_key in _SOURCE_MODULE_CACHE:
        return _SOURCE_MODULE_CACHE[cache_key]
    if not abs_path.exists():
        raise SkillAdapterError(f"Source executor module not found: {abs_path}")
    spec = importlib.util.spec_from_file_location(module_alias, abs_path)
    if spec is None or spec.loader is None:
        raise SkillAdapterError(f"Could not build import spec for: {abs_path}")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:  # noqa: BLE001 — surface any import error as adapter error
        raise SkillAdapterError(f"Failed to import source module {abs_path}: {e}") from e
    _SOURCE_MODULE_CACHE[cache_key] = module
    return module


# ---------------------------------------------------------------------------
# Base adapter (template method)
# ---------------------------------------------------------------------------

class BaseSkillAdapter:
    # Concrete adapters set these:
    SOURCE_REL_PATH: str = ""        # relative path to source skill_executor.py
    SOURCE_MODULE_ALIAS: str = ""    # unique module alias for importlib
    REQUIRED_OUTPUT_KEYS: tuple = ()  # CA-envelope keys that must be present

    def __init__(self, runs_dir, logs_dir):
        self.runs_dir = runs_dir
        self.logs_dir = logs_dir
        self._source_executor = None

    # -- hooks overridden by concrete adapters --------------------------------

    def map_inputs(self, ca_inputs: dict, upstream: dict) -> dict:
        raise NotImplementedError

    def invoke(self, src, mapped: dict, state_mgr, logger) -> dict:
        raise NotImplementedError

    def map_output(self, raw: dict, mapped: dict, src, state_mgr) -> dict:
        raise NotImplementedError

    # -- shared machinery -----------------------------------------------------

    def source_executor(self):
        """Lazily import + construct the source SkillExecutor (class only)."""
        if self._source_executor is not None:
            return self._source_executor
        module = _load_source_module(self.SOURCE_REL_PATH, self.SOURCE_MODULE_ALIAS)
        cls = getattr(module, "SkillExecutor", None)
        if cls is None:
            raise SkillAdapterError(
                f"SkillExecutor class not found in {self.SOURCE_REL_PATH}"
            )
        self._source_executor = cls(self.runs_dir, self.logs_dir)
        return self._source_executor

    def _check_envelope(self, out: dict) -> None:
        if not isinstance(out, dict):
            raise SkillAdapterError("Adapter output is not a dict.")
        missing = [k for k in self.REQUIRED_OUTPUT_KEYS if k not in out]
        if missing:
            raise SkillAdapterError(
                f"{type(self).__name__} output missing required key(s): {missing}"
            )
        md = out.get("markdown_output")
        if not isinstance(md, str) or not md.strip():
            raise SkillAdapterError(
                f"{type(self).__name__} produced empty markdown_output."
            )

    def execute(self, state_mgr, ca_inputs: dict, logger) -> dict:
        """Template: map_inputs -> invoke -> map_output -> envelope check."""
        upstream = state_mgr.get_state().get("intermediate_data", {})
        try:
            src = self.source_executor()
            mapped = self.map_inputs(ca_inputs, upstream)
            raw = self.invoke(src, mapped, state_mgr, logger)
            out = self.map_output(raw, mapped, src, state_mgr)
        except SkillAdapterError:
            raise
        except Exception as e:  # noqa: BLE001
            raise SkillAdapterError(f"{type(self).__name__} execution failed: {e}") from e
        self._check_envelope(out)
        return out


# ---------------------------------------------------------------------------
# Skill 1 — regulatory-mapping (regulatory-watch-agent)
# ---------------------------------------------------------------------------

class Skill1Adapter(BaseSkillAdapter):
    SOURCE_REL_PATH = "agents/regulatory-watch-agent/runtime/skill_executor.py"
    SOURCE_MODULE_ALIAS = "ca_src_regulatory_watch"
    REQUIRED_OUTPUT_KEYS = (
        "quality_score", "risk_tier", "applicable_regulations",
        "applicable_frameworks", "regulatory_obligations", "control_requirements",
        "markdown_output",
    )

    def map_inputs(self, ca_inputs: dict, upstream: dict) -> dict:
        subject = ca_inputs.get("client_ai_portfolio", "")
        existing = ca_inputs.get("existing_policies", "")
        if existing:
            subject = f"{subject}\n\nExisting governance context: {existing}"
        return {
            "subject_description": subject,
            "subject_type": ca_inputs.get("subject_type", "AI Portfolio"),
            "jurisdictions": ca_inputs.get("jurisdictions", []),
            "industry": ca_inputs.get("industry", "General Enterprise"),
            "data_types": ca_inputs.get("data_types", []),
            "ai_technology": ca_inputs.get("ai_technology", ""),
            "target_maturity_level": ca_inputs.get("target_maturity_level", "L3"),
        }

    def invoke(self, src, mapped: dict, state_mgr, logger) -> dict:
        return src.execute_regulatory_mapping(mapped, logger)

    def map_output(self, raw: dict, mapped: dict, src, state_mgr) -> dict:
        out = dict(raw)
        out["quality_score"] = raw.get("score")
        risk_tier = raw.get("risk_tier", "")
        out["markdown_output"] = src.compile_regulatory_mapping_to_markdown(raw, risk_tier)
        return out


# ---------------------------------------------------------------------------
# Skill 2 — governance-control-mapping (regulatory-watch-agent)
# ---------------------------------------------------------------------------

class Skill2Adapter(BaseSkillAdapter):
    SOURCE_REL_PATH = "agents/regulatory-watch-agent/runtime/skill_executor.py"
    SOURCE_MODULE_ALIAS = "ca_src_regulatory_watch"
    REQUIRED_OUTPUT_KEYS = ("quality_score", "controls", "markdown_output")

    def map_inputs(self, ca_inputs: dict, upstream: dict) -> dict:
        mapping_output = upstream.get("skill_1_json")
        if not isinstance(mapping_output, dict):
            raise SkillAdapterError(
                "Skill 2 requires Skill 1 output (skill_1_json) in intermediate_data."
            )
        # Pre-execution check: Skill 1 control_requirements must be non-empty.
        if not mapping_output.get("control_requirements"):
            raise SkillAdapterError(
                "Skill 2 pre-check failed: Skill 1 control_requirements is empty."
            )
        return {"mapping_output": mapping_output}

    def invoke(self, src, mapped: dict, state_mgr, logger) -> dict:
        return src.execute_governance_control_mapping(mapped["mapping_output"], logger)

    def map_output(self, raw: dict, mapped: dict, src, state_mgr) -> dict:
        out = dict(raw)
        out["quality_score"] = raw.get("score")
        # Reshape control_taxonomy_matrix -> CA "controls" with platform_coverage,
        # so output_builder's orphan-control count is computed correctly.
        controls = []
        for row in raw.get("control_taxonomy_matrix", []):
            classification = row.get("coverage_classification", "")
            controls.append({
                "id": row.get("control_id"),
                "name": row.get("control_name"),
                "control_type": row.get("control_type"),
                "coverage_classification": classification,
                "platform_coverage": "Ethana" in classification,
            })
        out["controls"] = controls
        out["markdown_output"] = src.compile_control_mapping_to_markdown(raw)
        return out


# ---------------------------------------------------------------------------
# Skill 5 — ethana-capability-validation (capability_validation_agent)
# ---------------------------------------------------------------------------

class Skill5Adapter(BaseSkillAdapter):
    SOURCE_REL_PATH = "agents/capability_validation_agent/runtime/skill_executor.py"
    SOURCE_MODULE_ALIAS = "ca_src_capability_validation"
    REQUIRED_OUTPUT_KEYS = (
        "capability_name", "validated_status", "ecs", "ecs_band", "ecs_path",
        "allowed_claims", "prohibited_claims", "contradictions_count",
        "sources_checked", "escalation_required", "hard_disqualifiers_triggered",
        "phase_9_gate_completed", "validation_date", "markdown_output",
    )

    def _capability_list(self, ca_inputs: dict, upstream: dict) -> list:
        """Resolve the set of capabilities to validate.

        Preferred source is an explicit ``capabilities`` list. Until Skill 3
        (solution-mapping) is implemented, fall back to a single capability from
        ``capability_name``. Full extraction from solution-mapping Section 3
        lands when Skill 3 is built.
        """
        caps = ca_inputs.get("capabilities")
        if isinstance(caps, list) and caps:
            return caps
        single = ca_inputs.get("capability_name")
        if single:
            return [{
                "capability_name": single,
                "proposed_claim": ca_inputs.get("proposed_claim", ""),
            }]
        raise SkillAdapterError(
            "Skill 5 requires at least one capability "
            "(inputs['capabilities'] or inputs['capability_name'])."
        )

    def map_inputs(self, ca_inputs: dict, upstream: dict) -> dict:
        cap_list = self._capability_list(ca_inputs, upstream)
        jurisdictions = ca_inputs.get("jurisdictions", [])
        jurisdiction = jurisdictions[0] if jurisdictions else "Global"
        per_cap = []
        for cap in cap_list:
            per_cap.append({
                "capability_name": cap.get("capability_name", ""),
                "proposed_claim": cap.get("proposed_claim", ""),
                # Schema enum (ethana-capability-validation-output) requires one of
                # the documented claim contexts; the CA governance package is a
                # formal client deliverable -> "Formal Proposal".
                "claim_context": "Formal Proposal",
                "requesting_team": ca_inputs.get("industry", "Advisory"),
                "jurisdiction": jurisdiction,
            })
        return {"per_capability_inputs": per_cap}

    def invoke(self, src, mapped: dict, state_mgr, logger) -> dict:
        results = [
            src.execute_validation(cap_inputs, logger)
            for cap_inputs in mapped["per_capability_inputs"]
        ]
        if not results:
            raise SkillAdapterError("Skill 5 produced no validation results.")
        return {"results": results}

    def map_output(self, raw: dict, mapped: dict, src, state_mgr) -> dict:
        results = raw["results"]

        def _is_worse(candidate, current):
            # Any escalation / disqualifier dominates; else lowest ECS wins.
            cand_bad = bool(candidate.get("escalation_required")) or bool(
                candidate.get("hard_disqualifiers_triggered")
            )
            curr_bad = bool(current.get("escalation_required")) or bool(
                current.get("hard_disqualifiers_triggered")
            )
            if cand_bad != curr_bad:
                return cand_bad
            return candidate.get("ecs", 0) < current.get("ecs", 0)

        worst = results[0]
        for r in results[1:]:
            if _is_worse(r, worst):
                worst = r

        out = dict(worst)
        out["markdown_output"] = src.compile_report_to_markdown(worst)
        out["all_capability_results"] = results
        return out


# ---------------------------------------------------------------------------
# Skill 6 — ethana-proposal-review (ethana_proposal_agent)
# ---------------------------------------------------------------------------

class Skill6Adapter(BaseSkillAdapter):
    SOURCE_REL_PATH = "agents/ethana_proposal_agent/runtime/skill_executor.py"
    SOURCE_MODULE_ALIAS = "ca_src_ethana_proposal"
    REQUIRED_OUTPUT_KEYS = (
        "pcs", "ctcs", "release_classification", "markdown_output",
    )

    # Source 4-value classification -> CA 3-value release_classification.
    CLASSIFICATION_MAP = {
        "Approved": "Approved",
        "Approved with Revisions": "Conditional",
        "Conditional Release": "Conditional",
        "Rejected": "Rejected",
    }

    def map_inputs(self, ca_inputs: dict, upstream: dict) -> dict:
        md_parts = []
        for key in ("skill_1_md", "skill_2_md", "skill_3_md",
                    "skill_4_md", "skill_5_md"):
            content = upstream.get(key)
            if content:
                md_parts.append(content)
        draft_proposal = "\n\n".join(md_parts)
        jurisdictions = ca_inputs.get("jurisdictions", [])
        return {
            "draft_proposal": draft_proposal,
            "solution_mapping_output": upstream.get("skill_3_json"),
            "feature_mapping_output": None,  # documented architectural gap; never fabricated
            "capability_validation_output": upstream.get("skill_5_json"),
            "regulatory_mapping_output": upstream.get("skill_1_json"),
            "control_mapping_output": upstream.get("skill_2_json"),
            "output_mode": "Governance Assessment",
            "customer_sector": ca_inputs.get("industry", ""),
            "jurisdictions": jurisdictions,
        }

    def invoke(self, src, mapped: dict, state_mgr, logger) -> dict:
        # Source method takes state_mgr; it writes harmless extra keys
        # (proposal_review_json / proposal_review_md) and never transitions state.
        return src.execute_proposal_review(state_mgr, mapped, logger)

    def map_output(self, raw: dict, mapped: dict, src, state_mgr) -> dict:
        out = dict(raw)
        source_classification = raw.get("classification")
        if source_classification not in self.CLASSIFICATION_MAP:
            raise SkillAdapterError(
                f"Skill 6 unknown classification: {source_classification!r}"
            )
        out["release_classification"] = self.CLASSIFICATION_MAP[source_classification]
        # Markdown is delivered out-of-band via state_mgr, not in the return value.
        intermediate = state_mgr.get_state().get("intermediate_data", {})
        out["markdown_output"] = intermediate.get("proposal_review_md", "")
        return out


# ---------------------------------------------------------------------------
# Skill 3 — ethana-solution-mapping (CA-local net-new executor)
# ---------------------------------------------------------------------------

class Skill3Adapter(BaseSkillAdapter):
    """Wraps the CA-local SolutionMappingExecutor (no external source runtime).

    The net-new executor already returns the full CA envelope, so this adapter's
    map_output is a pass-through; the BaseSkillAdapter envelope check still runs.
    """
    REQUIRED_OUTPUT_KEYS = (
        "matched_capabilities", "overall_coverage_summary",
        "quality_score", "overall_ccs", "production_coverage_percent",
        "commercial_motion", "markdown_output",
    )

    def source_executor(self):
        if self._source_executor is not None:
            return self._source_executor
        try:
            from solution_mapping_executor import SolutionMappingExecutor  # noqa: PLC0415
        except ImportError:
            from skills.solution_mapping_executor import (  # noqa: PLC0415
                SolutionMappingExecutor,
            )
        self._source_executor = SolutionMappingExecutor(self.runs_dir, self.logs_dir)
        return self._source_executor

    def map_inputs(self, ca_inputs: dict, upstream: dict) -> dict:
        control_mapping_output = upstream.get("skill_2_json")
        if not isinstance(control_mapping_output, dict) or not control_mapping_output.get("controls"):
            raise SkillAdapterError(
                "Skill 3 requires Skill 2 output (skill_2_json with controls) in "
                "intermediate_data."
            )
        return {
            "control_mapping_output": control_mapping_output,
            "regulatory_mapping_output": upstream.get("skill_1_json"),
            "customer_sector": ca_inputs.get("industry", ""),
            "jurisdictions": ca_inputs.get("jurisdictions", []),
            "existing_policies": ca_inputs.get("existing_policies", ""),
            "target_certification": ca_inputs.get("target_certification", ""),
        }

    def invoke(self, src, mapped: dict, state_mgr, logger) -> dict:
        return src.execute_solution_mapping(mapped, logger)

    def map_output(self, raw: dict, mapped: dict, src, state_mgr) -> dict:
        return dict(raw)


# ---------------------------------------------------------------------------
# Skill 4 — iso-42001-gap-assessment (CA-local net-new executor)
# ---------------------------------------------------------------------------

class Skill4Adapter(BaseSkillAdapter):
    """Wraps the CA-local Iso42001GapAssessmentExecutor (no external source runtime)."""
    REQUIRED_OUTPUT_KEYS = (
        "ams", "ars", "critical_gaps", "major_gaps", "minor_gaps",
        "certification_classification", "months_to_readiness",
        "quality_score", "markdown_output",
    )

    def source_executor(self):
        if self._source_executor is not None:
            return self._source_executor
        try:
            from iso42001_executor import Iso42001GapAssessmentExecutor  # noqa: PLC0415
        except ImportError:
            from skills.iso42001_executor import (  # noqa: PLC0415
                Iso42001GapAssessmentExecutor,
            )
        self._source_executor = Iso42001GapAssessmentExecutor(self.runs_dir, self.logs_dir)
        return self._source_executor

    def map_inputs(self, ca_inputs: dict, upstream: dict) -> dict:
        ai_portfolio = ca_inputs.get("client_ai_portfolio", "")
        if not (ai_portfolio or "").strip():
            raise SkillAdapterError(
                "Skill 4 requires client_ai_portfolio; an undefined portfolio "
                "cannot receive a valid AMS."
            )
        client_name = ca_inputs.get("client_name", "")
        existing = ca_inputs.get("existing_policies", "")
        return {
            "ai_portfolio": ai_portfolio,
            "organisation_description": f"{client_name}. {existing}".strip(),
            "existing_documentation": existing,
            "existing_policies": existing,
            "regulatory_mapping_output": upstream.get("skill_1_json"),
            "control_mapping_output": upstream.get("skill_2_json"),
            "jurisdictions": ca_inputs.get("jurisdictions", []),
            "industry": ca_inputs.get("industry", ""),
            "target_certification": ca_inputs.get("target_certification", ""),
        }

    def invoke(self, src, mapped: dict, state_mgr, logger) -> dict:
        return src.execute_gap_assessment(mapped, logger)

    def map_output(self, raw: dict, mapped: dict, src, state_mgr) -> dict:
        return dict(raw)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

ADAPTER_CLASSES = {
    1: Skill1Adapter,
    2: Skill2Adapter,
    3: Skill3Adapter,
    4: Skill4Adapter,
    5: Skill5Adapter,
    6: Skill6Adapter,
}


def build_adapter_registry(runs_dir, logs_dir) -> dict:
    """Construct one adapter instance per wired skill (1, 2, 3, 4, 5, 6)."""
    return {num: cls(runs_dir, logs_dir) for num, cls in ADAPTER_CLASSES.items()}
