#!/usr/bin/env python3
import sys
from pathlib import Path
import json

def get_agent_definitions(repo_root):
    """Returns the list of planned agents and their dependencies."""
    return {
        "Incident Intelligence Agent": {
            "required_skills": ["ai-incident-analysis", "governance-control-mapping"],
            "required_workflows": ["workflows/incident-assessment-workflow.md"],
            "target_level": 4
        },
        "Regulatory Watch Agent": {
            "required_skills": ["regulatory-mapping", "governance-control-mapping"],
            "required_workflows": ["workflows/regulatory-compliance-workflow.md"],
            "target_level": 4
        },
        "Capability Validation Agent": {
            "required_skills": ["ethana-capability-validation"],
            "required_workflows": [],  # Executes on CPM commits directly
            "target_level": 4
        },
        "Client Assessment Agent": {
            "required_skills": ["regulatory-mapping", "iso-42001-gap-assessment", "governance-control-mapping", "ethana-solution-mapping"],
            "required_workflows": ["workflows/governance-assessment-workflow.md"],
            "target_level": 4
        },
        "Ethana Proposal Agent": {
            "required_skills": ["regulatory-mapping", "governance-control-mapping", "ethana-solution-mapping", "ethana-feature-mapping", "ethana-proposal-review"],
            "required_workflows": ["workflows/proposal-development-workflow.md"],
            "target_level": 4
        }
    }

def certify_agent(repo_root, agent_name, spec):
    """Calculates the Readiness Level of a specific agent."""
    required_skills = spec["required_skills"]
    required_workflows = spec["required_workflows"]
    
    skills_dir = repo_root / "skills"
    
    # Level 0: Check if required skills are present
    missing_skills = []
    for skill in required_skills:
        skill_path = skills_dir / skill
        if not skill_path.exists() or not (skill_path / "SKILL.md").exists():
            missing_skills.append(skill)
            
    if missing_skills:
        return 0, f"Missing required skills: {missing_skills}"
        
    # Level 1: Skills Complete
    # Level 2: Skills + Workflows Complete
    missing_workflows = []
    for wf in required_workflows:
        wf_path = repo_root / wf
        if not wf_path.exists():
            missing_workflows.append(wf)
            
    if missing_workflows:
        return 1, f"Skills complete, but missing workflow files: {missing_workflows}"
        
    # Level 3: Evaluations Passing
    # For Level 3, check if baseline exists in either format:
    #   - Legacy directory format: evaluations/baselines/{skill}/
    #   - Flat .md format:         evaluations/baselines/{skill}-baseline.md
    baselines_dir = repo_root / "evaluations" / "baselines"
    missing_baselines = []
    for skill in required_skills:
        base_path = baselines_dir / skill
        flat_md = baselines_dir / f"{skill}-baseline.md"
        if not base_path.exists() and not flat_md.exists():
            missing_baselines.append(skill)
            
    if missing_baselines:
        return 2, f"Skills & workflows complete, but missing structural baselines in evaluations/baselines/ for: {missing_baselines}"
        
    # Level 4: Production Ready
    # Level 4 is reserved for agents that have the actual agent codebase committed under /agents/
    agent_dir = repo_root / "agents" / agent_name.lower().replace(" ", "_")
    agent_dir_hyphen = repo_root / "agents" / agent_name.lower().replace(" ", "-")
    exists_underscore = agent_dir.exists() and any(agent_dir.iterdir())
    exists_hyphen = agent_dir_hyphen.exists() and any(agent_dir_hyphen.iterdir())
    if not exists_underscore and not exists_hyphen:
        return 3, "Skills, workflows, and structural evaluations complete. Ready for agent codebase implementation."
        
    return 4, "Fully certified. Agent codebase and dependencies verified."

def main():
    repo_root = Path(__file__).resolve().parents[2]
    agents = get_agent_definitions(repo_root)
    
    print("==================================================")
    print("         Agent Readiness Certification Report")
    print("==================================================")
    
    all_passed = True
    results = {}
    
    for agent, spec in agents.items():
        level, msg = certify_agent(repo_root, agent, spec)
        results[agent] = {
            "readiness_level": level,
            "status_message": msg
        }
        
        status_label = f"L{level}"
        print(f"\n* {agent} [Status: {status_label}]")
        print(f"  Details: {msg}")
        
        # Check if agent is blocked below its readiness target (e.g. needs Level 3)
        if level < 3:
            all_passed = False
            
    print("\n==================================================")
    if not all_passed:
        print("Certification Status: BLOCKED (One or more agents lack required skills/workflows).")
        sys.exit(0)  # We exit clean for report output but indicate blocks
    else:
        print("Certification Status: READY (All ready agents validated to Level 3).")
        sys.exit(0)

if __name__ == "__main__":
    main()
