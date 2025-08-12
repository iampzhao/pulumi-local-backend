# Local Backend Workflow Location Guide

This guide explains the file locations and structure for the local backend workflow.

## Workflow File Location

The local backend workflow file is located at:
```
/.github/workflows/local-init.yml
```

**Why in the root?** GitHub Actions only discovers workflows in `.github/workflows/` at the repository root. Workflows in subdirectories are not executable.

## Supporting Files Location

All supporting files remain in the `local-backend/` directory:

```
local-backend/
├── scripts/
│   ├── configure_local_project.py
│   ├── generate_documentation.py
│   └── create_examples.py
├── docs/
│   ├── COMPLETE_LOCAL_WALKTHROUGH.md
│   └── examples/json-configs/
├── requirements.txt
└── README.md
```

## How It Works

1. **Workflow Discovery**: GitHub finds and displays the workflow from `.github/workflows/local-init.yml`
2. **Dependency Installation**: Workflow installs Python packages from `local-backend/requirements.txt`
3. **Script Execution**: Workflow runs Python scripts from `local-backend/scripts/`
4. **Documentation**: Users reference docs in `local-backend/` directory

## Workflow References

The workflow file references the local-backend directory in these steps:

- **Dependencies**: `pip install -r local-backend/requirements.txt`
- **Configuration**: `python ../../local-backend/scripts/configure_local_project.py`
- **Documentation**: `python ../../local-backend/scripts/generate_documentation.py`
- **Examples**: `python ../../local-backend/scripts/create_examples.py`

## Running the Workflow

1. Navigate to your repository's Actions tab
2. Find "Pulumi Project Factory - Initialize Local Backend Project"
3. Click "Run workflow"
4. Provide JSON configuration
5. The workflow will execute using files from both locations

## Benefits of This Structure

- **GitHub Compatibility**: Workflow is discoverable and runnable
- **Organized Code**: Related files kept together in `local-backend/` directory
- **Clear Separation**: Distinguishes local backend from AWS backend workflows
- **Maintainable**: Easy to find and update related components

---

**Note**: This structure allows you to run the local backend workflow directly from GitHub Actions while keeping all related code organized in the `local-backend/` directory.