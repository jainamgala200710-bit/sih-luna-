"""
Experiment tracking utilities for LunaAlign AI.
Simple version to get started.
"""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

def create_experiment(name: str, description: str = "", 
                     tags: List[str] = None, creator: str = "Unknown",
                     configuration: Dict[str, Any] = None,
                     project_root: Optional[str] = None) -> str:
    """Create a new experiment record.
    
    Args:
        name: Name of the experiment
        description: Description of the experiment
        tags: List of tags for categorization
        creator: Creator of the experiment
        configuration: Configuration used for the experiment
        project_root: Root directory of the project
        
    Returns:
        str: Unique experiment ID
    """
    if project_root is None:
        project_root = Path.cwd()
    else:
        project_root = Path(project_root)
    
    experiments_dir = project_root / 'experiments'
    experiments_dir.mkdir(parents=True, exist_ok=True)
    
    experiments_file = experiments_dir / 'experiments.json'
    
    # Load existing data or create new
    if experiments_file.exists():
        try:
            with open(experiments_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            data = {"experiments": [], "last_updated": "", "version": "1.0.0"}
    else:
        data = {"experiments": [], "last_updated": "", "version": "1.0.0"}
    
    # Create experiment data
    if tags is None:
        tags = []
    if configuration is None:
        configuration = {}
    
    experiment_id = str(uuid.uuid4())
    experiment_data = {
        "id": experiment_id,
        "name": name,
        "description": description,
        "tags": tags,
        "creator": creator,
        "created_at": datetime.now().isoformat(),
        "configuration": configuration,
        "results": {},
        "status": "created",
        "notes": ""
    }
    
    # Add to experiments list
    data["experiments"].append(experiment_data)
    data["last_updated"] = datetime.now().isoformat()
    
    # Save back to file
    try:
        with open(experiments_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Warning: Could not save experiment: {e}")
    
    return experiment_id

def list_experiments(project_root: Optional[str] = None) -> List[Dict[str, Any]]:
    """List all experiments.
    
    Args:
        project_root: Root directory of the project
        
    Returns:
        list: List of experiment dictionaries
    """
    if project_root is None:
        project_root = Path.cwd()
    else:
        project_root = Path(project_root)
    
    experiments_file = project_root / 'experiments' / 'experiments.json'
    
    if not experiments_file.exists():
        return []
    
    try:
        with open(experiments_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("experiments", [])
    except (json.JSONDecodeError, IOError):
        return []

# Test the functions
if __name__ == "__main__":
    # Test creating an experiment
    exp_id = create_experiment(
        name="Test Experiment",
        description="A test experiment to verify the tracking system",
        tags=["test", "verification"],
        creator="LunaAlign AI",
        configuration={"test_param": "value"}
    )
    print(f"Created experiment with ID: {exp_id}")
    
    # Test listing experiments
    experiments = list_experiments()
    print(f"Found {len(experiments)} experiments")
    for exp in experiments:
        print(f"  - {exp['name']} ({exp['id']})")
