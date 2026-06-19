#!/usr/bin/env python3
import random
from datetime import datetime

try:
    from skill_adapters import build_adapter_registry
except ImportError:  # pragma: no cover - direct package import fallback
    from .skill_adapters import build_adapter_registry


class SkillExecutor:
    """
    Defines the execution interface for all 6 skills in the Client Assessment chain.

    Skills 1, 2, 5, 6 are wired via the Option C adapter layer (delegating to the
    existing certified executors in other runtimes). Skills 3 and 4 remain
    NotImplementedError stubs until their net-new executors are built.

    Tests may still override individual methods with lambda fixtures (the adapter
    is only invoked when a method is not overridden):
        orchestrator.executor.execute_skill_1 = lambda sm, inp, lg: FIXTURE_OUTPUT
    """

    def __init__(self, runs_dir, logs_dir):
        self.runs_dir = runs_dir
        self.logs_dir = logs_dir
        self.adapters = build_adapter_registry(runs_dir, logs_dir)

    def generate_traceability_id(self) -> str:
        year = datetime.now().year
        seq = random.randint(1, 9999)
        return f"TR-CA-{year}-{seq:04d}"

    def execute_skill_1(self, state_mgr, inputs: dict, logger) -> dict:
        """Skill 1: regulatory-mapping. Returns regulatory_mapping_output JSON."""
        return self.adapters[1].execute(state_mgr, inputs, logger)

    def execute_skill_2(self, state_mgr, inputs: dict, logger) -> dict:
        """Skill 2: governance-control-mapping. Returns control_mapping_output JSON."""
        return self.adapters[2].execute(state_mgr, inputs, logger)

    def execute_skill_3(self, state_mgr, inputs: dict, logger) -> dict:
        """Skill 3: ethana-solution-mapping. Returns solution_mapping_output JSON."""
        return self.adapters[3].execute(state_mgr, inputs, logger)

    def execute_skill_4(self, state_mgr, inputs: dict, logger) -> dict:
        """Skill 4: iso-42001-gap-assessment. Returns iso42001_output JSON."""
        return self.adapters[4].execute(state_mgr, inputs, logger)

    def execute_skill_5(self, state_mgr, inputs: dict, logger) -> dict:
        """Skill 5: ethana-capability-validation. Returns capability_validation_output JSON."""
        return self.adapters[5].execute(state_mgr, inputs, logger)

    def execute_skill_6(self, state_mgr, inputs: dict, logger) -> dict:
        """Skill 6: ethana-proposal-review. Returns proposal_review_output JSON."""
        return self.adapters[6].execute(state_mgr, inputs, logger)
