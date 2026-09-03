"""Simple state management utilities."""

import os
from datetime import datetime

def update_project_state(current_phase, phase_name, status, overview="", completed_phases=None, next_phase=None, details=""):
    """Update PROJECT_STATE.md."""
    if completed_phases is None:
        completed_phases = []
    
    with open('PROJECT_STATE.md', 'w') as f:
        f.write(f'''# Project State: LunaAlign AI
**Last Updated**: {datetime.now().strftime('%Y-%m-%d')}
**Current Phase**: {current_phase} ({phase_name})
**Status**: {status}
**Overview**: 
{overview}

**Completed Phases**:
''')
        for phase in sorted(completed_phases):
            f.write(f'- Phase {get_phase_name(phase)} (COMPLETE)\n')
        
        f.write(f'''
**Current Phase**: {current_phase} ({phase_name})
**Next Phase**: {next_phase if next_phase is not None else 'TBD'} - {get_phase_name(next_phase) if next_phase is not None else 'To Be Determined'}\n\n''')
        
        if details:
            f.write(f'**Details of Phase {current_phase}**:\n{details}\n')

def record_technical_decision(date, decision, rationale, status="Approved"):
    """Record a technical decision."""
    try:
        with open('TECHNICAL_DECISIONS.md', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        content = '# Technical Decisions: LunaAlign AI\n**Last Updated**: {date}\n**Project**: LunaAlign AI - SIH26166\n**Purpose**: Records key architectural and technical decisions made during development.\n\n## Decisions Log\n\n'
    
    if '## Decisions Log' not in content:
        if content.strip() == '':
            new_content = f'''# Technical Decisions: LunaAlign AI
**Last Updated**: {date}
**Project**: LunaAlign AI - SIH26166
**Purpose**: Records key architectural and technical decisions made during development.

## Decisions Log

### {date}
- **Decision**: {decision}
- **Rationale**: {rationale}
- **Status**: {status}

'''
        else:
            new_content = content + f'''

## Decisions Log

### {date}
- **Decision**: {decision}
- **Rationale**: {rationale}
- **Status**: {status}

'''
    else:
        lines = content.split('\n')
        insert_index = -1
        for i, line in enumerate(lines):
            if line.strip() == '## Decisions Log':
                insert_index = i + 1
                break
        
        if insert_index != -1:
            lines.insert(insert_index + 1, f'### {date}')
            lines.insert(insert_index + 2, f'- **Decision**: {decision}')
            lines.insert(insert_index + 3, f'- **Rationale**: {rationale}')
            lines.insert(insert_index + 4, f'- **Status**: {status}')
            lines.insert(insert_index + 5, '')
            new_content = '\n'.join(lines)
        else:
            new_content = content + f'''

### {date}
- **Decision**: {decision}
- **Rationale**: {rationale}
- **Status**: {status}

'''
    
    with open('TECHNICAL_DECISIONS.md', 'w') as f:
        f.write(new_content)

def get_phase_name(phase_num):
    """Get phase name from number."""
    phase_names = {
        0: "Project Analysis and Architecture",
        1: "Repository Initialization and Environment Setup",
        2: "Project Configuration and Persistent Documentation System",
        3: "Dataset Acquisition Strategy and Data Inventory System",
        4: "Synthetic Lunar Dataset Generation",
        5: "Scientific Image Ingestion and Format Handling",
        6: "Metadata Management and Image Pair Construction",
        7: "Data Visualization and Dataset Quality Validation",
        8: "Baseline Preprocessing Pipeline",
        9: "Classical Feature Matching Baselines",
        10: "Geometric Verification and Outlier Rejection",
        11: "Image Registration Baseline",
        12: "Deep Learning Correspondence Engine",
        13: "Illumination-Invariant Structural Feature Engine",
        14: "Multi-Scale and Multi-Modal Matching",
        15: "Uniform Spatial Distribution Engine",
        16: "Sub-Pixel Correspondence Refinement",
        17: "Adaptive Transformation Model Selection",
        18: "Complete Evaluation and Benchmarking Framework",
        19: "Explainable Correspondence System",
        20: "Interactive Visualization Dashboard",
        21: "Backend API Integration",
        22: "Frontend Integration",
        23: "End-to-End System Integration",
        24: "Real Dataset Experiments",
        25: "Performance Optimization",
        26: "Testing and Edge Cases",
        27: "Automated Technical Reporting",
        28: "Final SIH Demonstration Preparation",
        29: "Documentation and Final Project Polish",
        30: "Contingency and Knowledge Transfer"
    }
    return phase_names.get(phase_num, f"Phase {phase_num}")

# Test
if __name__ == "__main__":
    print("Testing state utilities...")
    update_project_state(2, "Test Phase", "Testing", "Test overview", [0, 1], 3, "Test details")
    record_technical_decision("2026-09-02", "Test Decision", "Test Rationale")
    print("State utilities test completed!")
