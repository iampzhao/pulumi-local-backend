#!/usr/bin/env python3
"""
Pulumi Factory - Local Project Configuration Script

This script configures a Pulumi project for local backend usage:
1. Sets up appropriate configuration values for local development
2. Configures stack-specific settings
3. Ensures proper local backend configuration
4. Sets up development-friendly defaults

SECURITY NOTES:
- This script only modifies configuration files, never creates credential files
- All operations use local file system only - no network calls
- Configuration changes are logged for audit purposes
- No sensitive information is stored in configuration files

Author: Pulumi Factory - Local Backend
"""

import argparse
import json
import logging
import os
import subprocess
import sys
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class LocalProjectConfigurator:
    """
    Configures Pulumi projects for local backend development.
    
    This class handles:
    - Stack configuration setup
    - Local development defaults
    - Project-specific settings
    - Template-specific configuration
    """
    
    def __init__(self, project_name: str, stack_name: str, template: str):
        """
        Initialize the local project configurator.
        
        Args:
            project_name: Name of the Pulumi project
            stack_name: Name of the Pulumi stack
            template: Pulumi template type (python, typescript, etc.)
        """
        self.project_name = project_name
        self.stack_name = stack_name
        self.template = template
        
        # Configuration file paths
        self.pulumi_yaml_path = Path('Pulumi.yaml')
        self.stack_config_path = Path(f'Pulumi.{stack_name}.yaml')
        
        # Validate we're in a Pulumi project directory
        if not self.pulumi_yaml_path.exists():
            raise FileNotFoundError(f"Pulumi.yaml not found. Ensure you're in a Pulumi project directory.")
        
        logger.info(f"Initialized configurator for project: {project_name}, stack: {stack_name}, template: {template}")
    
    def _run_pulumi_command(self, command: List[str], check: bool = True) -> subprocess.CompletedProcess:
        """
        Run a Pulumi command with proper error handling and logging.
        
        Args:
            command: List of command arguments
            check: Whether to raise exception on non-zero exit code
            
        Returns:
            CompletedProcess instance
        """
        full_command = ['pulumi'] + command
        logger.info(f"Running command: {' '.join(full_command)}")
        
        try:
            result = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                check=check
            )
            
            if result.stdout:
                logger.debug(f"Command output: {result.stdout.strip()}")
            if result.stderr:
                logger.warning(f"Command stderr: {result.stderr.strip()}")
                
            return result
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed with exit code {e.returncode}")
            if e.stdout:
                logger.error(f"Stdout: {e.stdout}")
            if e.stderr:
                logger.error(f"Stderr: {e.stderr}")
            raise
    
    def configure_local_backend_settings(self):
        """
        Configure settings specific to local backend usage.
        """
        try:
            logger.info("Configuring local backend specific settings...")
            
            # Read current Pulumi.yaml
            with open(self.pulumi_yaml_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # Ensure we have metadata section
            if 'metadata' not in config:
                config['metadata'] = {}
            
            # Add local backend metadata
            config['metadata']['backend_type'] = 'local'
            config['metadata']['backend_storage'] = 'file'
            config['metadata']['configured_by'] = 'pulumi-factory-local'
            config['metadata']['local_backend'] = True
            config['metadata']['migration_ready'] = True  # Can be migrated to cloud backend later
            
            # Write updated configuration
            with open(self.pulumi_yaml_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False, indent=2)
            
            logger.info("Local backend settings configured successfully")
            
        except Exception as e:
            logger.error(f"Failed to configure local backend settings: {str(e)}")
            raise
    
    def set_development_configuration(self):
        """
        Set up development-friendly configuration values.
        """
        try:
            logger.info("Setting up development configuration...")
            
            # Common development settings for all templates
            common_configs = {
                'project:environment': 'development',
                'project:local-backend': 'true',
                'project:managed-by': 'pulumi-factory'
            }
            
            # Template-specific configurations
            template_configs = {
                'python': {
                    'aws:region': 'ap-southeast-2',  # Default region for AWS resources
                    'aws:defaultTags.tags.Environment': 'development',
                    'aws:defaultTags.tags.Project': self.project_name,
                    'aws:defaultTags.tags.Stack': self.stack_name,
                    'aws:defaultTags.tags.ManagedBy': 'Pulumi',
                    'aws:defaultTags.tags.Backend': 'local'
                },
                'typescript': {
                    'aws:region': 'ap-southeast-2',
                    'aws:defaultTags': json.dumps({
                        'Environment': 'development',
                        'Project': self.project_name,
                        'Stack': self.stack_name,
                        'ManagedBy': 'Pulumi',
                        'Backend': 'local'
                    })
                },
                'go': {
                    'aws:region': 'ap-southeast-2',
                    'environment': 'development',
                    'project': self.project_name,
                    'stack': self.stack_name
                },
                'csharp': {
                    'aws:region': 'ap-southeast-2',
                    'Environment': 'development',
                    'Project': self.project_name,
                    'Stack': self.stack_name
                },
                'yaml': {
                    'aws:region': 'ap-southeast-2',
                    'environment': 'development',
                    'project': self.project_name,
                    'stack': self.stack_name
                }
            }
            
            # Apply common configurations
            for key, value in common_configs.items():
                self._run_pulumi_command(['config', 'set', key, value])
            
            # Apply template-specific configurations
            if self.template in template_configs:
                for key, value in template_configs[self.template].items():
                    self._run_pulumi_command(['config', 'set', key, str(value)])
            
            logger.info("Development configuration set successfully")
            
        except Exception as e:
            logger.error(f"Failed to set development configuration: {str(e)}")
            raise
    
    def create_gitignore_entries(self):
        """
        Create or update .gitignore file with Pulumi-specific entries.
        """
        try:
            logger.info("Creating/updating .gitignore for Pulumi project...")
            
            # Pulumi-specific .gitignore entries
            pulumi_gitignore_entries = [
                "",
                "# Pulumi local backend files",
                ".pulumi/",
                "*.pulumi.json",
                "",
                "# Pulumi configuration files with secrets",
                "Pulumi.*.yaml",
                "!Pulumi.yaml",
                "",
                "# Local state backups",
                "*.backup",
                "",
                "# IDE and editor files",
                ".vscode/",
                ".idea/",
                "*.swp",
                "*.swo",
                "*~",
                "",
                "# OS-specific files",
                ".DS_Store",
                "Thumbs.db",
                ""
            ]
            
            # Template-specific entries
            template_entries = {
                'python': [
                    "# Python-specific",
                    "__pycache__/",
                    "*.pyc",
                    "*.pyo",
                    "*.pyd",
                    ".Python",
                    "venv/",
                    ".venv/",
                    "env/",
                    ".env",
                    "pip-log.txt",
                    "pip-delete-this-directory.txt"
                ],
                'typescript': [
                    "# Node.js specific",
                    "node_modules/",
                    "npm-debug.log*",
                    "yarn-debug.log*",
                    "yarn-error.log*",
                    ".npm",
                    ".yarn-integrity",
                    "dist/",
                    "build/"
                ],
                'go': [
                    "# Go specific",
                    "*.exe",
                    "*.exe~",
                    "*.dll",
                    "*.so",
                    "*.dylib",
                    "vendor/",
                    "go.work"
                ],
                'csharp': [
                    "# .NET specific",
                    "bin/",
                    "obj/",
                    "*.user",
                    "*.suo",
                    "*.cache",
                    "*.docstates",
                    "[Dd]ebug/",
                    "[Rr]elease/"
                ],
                'yaml': [
                    "# YAML template specific",
                    "*.tmp",
                    "*.temp"
                ]
            }
            
            gitignore_path = Path('.gitignore')
            
            # Read existing .gitignore if it exists
            existing_entries = []
            if gitignore_path.exists():
                with open(gitignore_path, 'r', encoding='utf-8') as f:
                    existing_entries = f.read().splitlines()
            
            # Combine all entries
            all_entries = existing_entries + pulumi_gitignore_entries
            if self.template in template_entries:
                all_entries.extend([""] + template_entries[self.template])
            
            # Remove duplicates while preserving order
            seen = set()
            unique_entries = []
            for entry in all_entries:
                if entry not in seen:
                    seen.add(entry)
                    unique_entries.append(entry)
            
            # Write updated .gitignore
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(unique_entries))
                f.write('\n')  # Ensure file ends with newline
            
            logger.info(".gitignore created/updated successfully")
            
        except Exception as e:
            logger.error(f"Failed to create/update .gitignore: {str(e)}")
            raise
    
    def create_development_scripts(self):
        """
        Create helpful development scripts for the project.
        """
        try:
            logger.info("Creating development helper scripts...")
            
            # Create scripts directory
            scripts_dir = Path('scripts')
            scripts_dir.mkdir(exist_ok=True)
            
            # Common development script content
            dev_script_content = {
                'preview.py': f'''#!/usr/bin/env python3
"""
Development script to preview Pulumi stack changes.
"""
import subprocess
import sys

def main():
    """Preview stack changes."""
    print("Previewing {self.project_name}/{self.stack_name} stack changes...")
    
    try:
        # Ensure we're using the correct stack
        subprocess.run(['pulumi', 'stack', 'select', '{self.stack_name}'], check=True)
        
        # Run preview
        result = subprocess.run(['pulumi', 'preview'], check=False)
        
        if result.returncode == 0:
            print("\\nPreview completed successfully!")
        else:
            print(f"\\nPreview failed with exit code {{result.returncode}}")
            sys.exit(result.returncode)
            
    except subprocess.CalledProcessError as e:
        print(f"Error running Pulumi commands: {{e}}")
        sys.exit(1)

if __name__ == '__main__':
    main()
''',
                'deploy.py': f'''#!/usr/bin/env python3
"""
Development script to deploy Pulumi stack.
"""
import subprocess
import sys

def main():
    """Deploy stack changes."""
    print("Deploying {self.project_name}/{self.stack_name} stack...")
    
    try:
        # Ensure we're using the correct stack
        subprocess.run(['pulumi', 'stack', 'select', '{self.stack_name}'], check=True)
        
        # Run deployment
        result = subprocess.run(['pulumi', 'up', '--yes'], check=False)
        
        if result.returncode == 0:
            print("\\nDeployment completed successfully!")
        else:
            print(f"\\nDeployment failed with exit code {{result.returncode}}")
            sys.exit(result.returncode)
            
    except subprocess.CalledProcessError as e:
        print(f"Error running Pulumi commands: {{e}}")
        sys.exit(1)

if __name__ == '__main__':
    main()
''',
                'destroy.py': f'''#!/usr/bin/env python3
"""
Development script to destroy Pulumi stack resources.
WARNING: This will destroy all resources managed by this stack!
"""
import subprocess
import sys

def main():
    """Destroy stack resources."""
    print("WARNING: This will destroy all resources in {self.project_name}/{self.stack_name}!")
    
    response = input("Are you sure you want to continue? (yes/no): ")
    if response.lower() != 'yes':
        print("Operation cancelled.")
        return
    
    try:
        # Ensure we're using the correct stack
        subprocess.run(['pulumi', 'stack', 'select', '{self.stack_name}'], check=True)
        
        # Run destroy
        result = subprocess.run(['pulumi', 'destroy', '--yes'], check=False)
        
        if result.returncode == 0:
            print("\\nDestroy completed successfully!")
        else:
            print(f"\\nDestroy failed with exit code {{result.returncode}}")
            sys.exit(result.returncode)
            
    except subprocess.CalledProcessError as e:
        print(f"Error running Pulumi commands: {{e}}")
        sys.exit(1)

if __name__ == '__main__':
    main()
'''
            }
            
            # Create script files
            for script_name, content in dev_script_content.items():
                script_path = scripts_dir / script_name
                with open(script_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Make scripts executable on Unix systems
                try:
                    os.chmod(script_path, 0o755)
                except OSError:
                    pass  # Windows doesn't support chmod
            
            logger.info("Development scripts created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create development scripts: {str(e)}")
            raise


def main():
    """
    Main function to configure Pulumi project for local development.
    """
    parser = argparse.ArgumentParser(
        description='Configure Pulumi project for local backend development'
    )
    parser.add_argument(
        '--project-name',
        required=True,
        help='Name of the Pulumi project'
    )
    parser.add_argument(
        '--stack-name',
        required=True,
        help='Name of the Pulumi stack'
    )
    parser.add_argument(
        '--template',
        required=True,
        choices=['python', 'typescript', 'go', 'csharp', 'yaml'],
        help='Pulumi template type'
    )
    parser.add_argument(
        '--create-docs',
        type=str,
        choices=['true', 'false'],
        default='true',
        help='Whether to create documentation files'
    )
    parser.add_argument(
        '--include-examples',
        type=str,
        choices=['true', 'false'],
        default='true',
        help='Whether to include example code'
    )
    
    args = parser.parse_args()
    
    logger.info("=== Pulumi Factory - Local Project Configuration ===")
    logger.info(f"Project: {args.project_name}")
    logger.info(f"Stack: {args.stack_name}")
    logger.info(f"Template: {args.template}")
    logger.info(f"Create docs: {args.create_docs}")
    logger.info(f"Include examples: {args.include_examples}")
    
    try:
        # Initialize configurator
        configurator = LocalProjectConfigurator(
            args.project_name,
            args.stack_name,
            args.template
        )
        
        # Configure local backend settings
        configurator.configure_local_backend_settings()
        
        # Set development configuration
        configurator.set_development_configuration()
        
        # Create .gitignore entries
        configurator.create_gitignore_entries()
        
        # Create development scripts
        configurator.create_development_scripts()
        
        logger.info("=== Local Project Configuration Complete ===")
        return 0
        
    except Exception as e:
        logger.error(f"Local project configuration failed: {str(e)}")
        return 1


if __name__ == '__main__':
    sys.exit(main())