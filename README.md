# Pulumi Factory - Local Backend

This directory contains the local backend workflow for the Pulumi Factory. The local backend workflow creates Pulumi projects without any cloud dependencies, using local file-based state storage. This is perfect for development, testing, and getting started with Pulumi.

## Overview

The local backend workflow provides:

- **No AWS Dependencies**: No cloud accounts or credentials required
- **Local State Storage**: State files stored in local `.pulumi/` directory
- **Rapid Development**: Fast iteration without cloud API calls
- **Cost-Free Development**: No charges for state storage or API usage
- **Educational**: Great for learning Pulumi concepts
- **Migration Ready**: Easy migration to cloud backends when needed

## Quick Start

### Example JSON Configuration

```json
{
  "project_name": "my-app",
  "stack_name": "dev", 
  "pulumi_template": "python",
  "project_description": "My application infrastructure",
  "target_repo_url": "https://github.com/myorg/my-app.git",
  "target_github_token": "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "create_documentation": true,
  "include_examples": true
}
```

### JSON Formatting Notes

**Important**: Ensure your JSON is properly formatted:
- All field names and string values must be in double quotes
- Use commas between fields (but not after the last field)
- Boolean values are `true`/`false` (lowercase, no quotes)
- Project names with hyphens: `"test-01"` (hyphen inside quotes)

**Common Mistakes**:
- ❌ `"project_name": "test"-01` (hyphen outside quotes)
- ✅ `"project_name": "test-01"` (hyphen inside quotes)
- ❌ `"create_documentation": "true"` (boolean in quotes)
- ✅ `"create_documentation": true` (boolean without quotes)

### GitHub Actions Workflow

1. Navigate to your GitHub repository with the Pulumi Factory
2. Go to Actions → "Pulumi Project Factory - Initialize Local Backend Project"
3. Click "Run workflow"
4. Paste your JSON configuration
5. Click "Run workflow"

**Note**: The workflow file is located at `.github/workflows/local-init.yml` in the repository root, but it references scripts and configuration from the `local-backend/` directory.

The workflow will:
1. Create a Pulumi project with local backend
2. Generate comprehensive documentation
3. Create example infrastructure code
4. Push to a new branch in your target repository

## Directory Structure

```
local-backend/
├── scripts/
│   ├── configure_local_project.py  # Project configuration script
│   ├── generate_documentation.py   # Documentation generation script
│   └── create_examples.py          # Example code generation script
├── docs/
│   ├── COMPLETE_LOCAL_WALKTHROUGH.md  # Complete simulation
│   └── examples/
│       └── json-configs/           # Example JSON configurations
├── requirements.txt                # Python dependencies
└── README.md                      # This file

# Main workflow file (located in repository root)
/.github/workflows/local-init.yml       # GitHub Actions workflow
```

## Configuration Reference

### Required Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `project_name` | string | Name of the Pulumi project | `"my-app"` |
| `stack_name` | string | Name of the Pulumi stack | `"dev"` |
| `target_repo_url` | string | Target GitHub repository URL | `"https://github.com/org/repo.git"` |
| `target_github_token` | string | GitHub personal access token | `"ghp_xxx..."` |

### Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `pulumi_template` | string | `"python"` | Pulumi template type |
| `project_description` | string | Auto-generated | Project description |
| `create_documentation` | boolean | `true` | Generate documentation files |
| `include_examples` | boolean | `true` | Include example infrastructure code |

### Supported Templates

- **python**: Python with AWS provider
- **typescript**: TypeScript/Node.js with AWS provider  
- **go**: Go with AWS provider
- **csharp**: C#/.NET with AWS provider
- **yaml**: YAML-based infrastructure definition

## Generated Project Structure

The workflow creates a complete Pulumi project:

```
target-repo/
└── project-name/
    ├── .pulumi/                    # Local state storage (excluded from git)
    ├── scripts/                    # Development helper scripts
    │   ├── preview.py             # Preview infrastructure changes
    │   ├── deploy.py              # Deploy infrastructure
    │   └── destroy.py             # Destroy infrastructure
    ├── examples/                   # Additional example code (optional)
    ├── Pulumi.yaml                # Project configuration
    ├── Pulumi.stack-name.yaml     # Stack configuration
    ├── __main__.py                # Main infrastructure code (Python example)
    ├── requirements.txt           # Dependencies (Python example)
    ├── .gitignore                 # Git ignore rules
    ├── README.md                  # Project documentation
    ├── DEVELOPMENT.md             # Development guide
    ├── MIGRATION.md               # Cloud backend migration guide
    └── [template-specific files]  # Additional files based on template
```

## Features

### Local Backend Benefits

1. **No External Dependencies**: Works without any cloud accounts
2. **Fast Iteration**: No network calls for state operations
3. **Complete Control**: Direct access to state files
4. **Cost-Free**: No cloud charges for development
5. **Offline Capable**: Works without internet connection
6. **Educational**: Perfect for learning and experimentation

### Generated Documentation

Each project includes comprehensive documentation:

- **README.md**: Complete project overview and setup instructions
- **DEVELOPMENT.md**: Detailed development workflow guide
- **MIGRATION.md**: Step-by-step cloud backend migration guide

### Development Tools

Generated projects include helpful scripts:

- **preview.py**: Preview infrastructure changes
- **deploy.py**: Deploy infrastructure 
- **destroy.py**: Destroy all resources (with confirmation)

### Example Infrastructure

Projects include working examples of:

- S3 buckets with encryption and versioning
- IAM roles and policies
- Security groups with common rules
- CloudWatch log groups
- SSM parameters for configuration
- Additional examples in `examples/` directory

## Local Development Workflow

After project creation:

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd project-name
   ```

2. **Install dependencies** (template-specific):
   ```bash
   # Python
   pip install -r requirements.txt
   
   # TypeScript
   npm install
   
   # Go
   go mod tidy
   
   # C#
   dotnet restore
   ```

3. **Select the stack**:
   ```bash
   pulumi stack select stack-name
   ```

4. **Preview infrastructure**:
   ```bash
   pulumi preview
   # or
   python scripts/preview.py
   ```

5. **Deploy infrastructure**:
   ```bash
   pulumi up
   # or  
   python scripts/deploy.py
   ```

## State Management

### Local State Storage

- State files stored in `.pulumi/` directory
- Each stack has its own state file
- State is portable between machines
- No automatic backup or versioning

### State Backup

Regular backups recommended:

```bash
# Export state to backup file
pulumi stack export --file backup-$(date +%Y%m%d).json

# Store backups securely
mkdir -p ~/pulumi-backups
mv backup-*.json ~/pulumi-backups/
```

### State Recovery

If state becomes corrupted:

```bash
# Import from backup
pulumi stack import --file backup-20231207.json

# Refresh state from actual infrastructure
pulumi refresh
```

## Migration to Cloud Backends

When ready for production, migrate to cloud backends:

1. **Pulumi Cloud** (easiest):
   ```bash
   pulumi login
   pulumi stack init organization/project/stack
   pulumi stack import --file state-backup.json
   ```

2. **AWS S3 Backend**:
   ```bash
   pulumi login s3://my-pulumi-state-bucket
   pulumi stack init stack-name
   pulumi stack import --file state-backup.json
   ```

3. **Other Backends**: Azure Blob, Google Cloud Storage, etc.

See the generated `MIGRATION.md` in each project for detailed instructions.

## Security Considerations

### Local Backend Security

- State files may contain sensitive resource information
- Use disk encryption for additional security
- Backup state files to secure, encrypted storage
- Don't commit `.pulumi/` directory to version control
- Consider cloud backends for production workloads

### Secrets Management

- Use `pulumi config set --secret` for sensitive values
- Secrets are encrypted in local state files
- Consider external secret management for production

## Troubleshooting

### Common Issues

1. **Template not supported**: Check supported templates list
2. **GitHub token issues**: Ensure token has repository access
3. **Pulumi CLI issues**: Verify Pulumi CLI installation
4. **State file corruption**: Restore from backup

### Getting Help

- Review generated project documentation
- Check [Pulumi Documentation](https://www.pulumi.com/docs/)
- Join [Pulumi Community Slack](https://slack.pulumi.com/)
- Open issues in [Pulumi GitHub](https://github.com/pulumi/pulumi/issues)

## Comparison with AWS Backend Workflow

| Feature | Local Backend | AWS Backend |
|---------|---------------|-------------|
| **Setup Complexity** | Simple | Moderate |
| **AWS Credentials** | Not required | Required |
| **State Storage** | Local files | S3 bucket |
| **State Backup** | Manual | Automatic |
| **Collaboration** | Single user | Multi-user |
| **State Locking** | None | Available |
| **Cost** | Free | S3/KMS charges |
| **Migration** | Easy to cloud | Already cloud |
| **Use Cases** | Dev, learning, testing | Production, teams |

## Example Configurations

### Python Web Application

```json
{
  "project_name": "webapp",
  "stack_name": "development", 
  "pulumi_template": "python",
  "project_description": "Web application infrastructure with S3, EC2, and RDS",
  "target_repo_url": "https://github.com/mycompany/webapp.git",
  "target_github_token": "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "create_documentation": true,
  "include_examples": true
}
```

### TypeScript Microservices

```json
{
  "project_name": "microservices",
  "stack_name": "local",
  "pulumi_template": "typescript", 
  "project_description": "Microservices infrastructure with Lambda and API Gateway",
  "target_repo_url": "https://github.com/mycompany/microservices-infra.git",
  "target_github_token": "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "create_documentation": true,
  "include_examples": true
}
```

### Go Infrastructure

```json
{
  "project_name": "infrastructure",
  "stack_name": "dev",
  "pulumi_template": "go",
  "project_description": "Core infrastructure components in Go",
  "target_repo_url": "https://github.com/mycompany/core-infrastructure.git", 
  "target_github_token": "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "create_documentation": false,
  "include_examples": false
}
```

## Best Practices

### Development

1. **Regular Backups**: Export state daily during active development
2. **Version Control**: Commit infrastructure code, not state files
3. **Configuration**: Use Pulumi config for environment-specific values
4. **Testing**: Use preview before applying changes
5. **Documentation**: Keep project documentation updated

### State Management

1. **Backup Strategy**: Automated daily state exports
2. **Secure Storage**: Encrypt backups and store securely
3. **State Validation**: Regular `pulumi refresh` operations
4. **Clean Deployments**: Avoid manual infrastructure changes

### Migration Planning

1. **Test Migration**: Practice with project copies
2. **Backup Everything**: State, config, and code
3. **Team Coordination**: Plan migrations during low activity
4. **Gradual Migration**: Migrate non-critical projects first

## Contributing

To contribute to the local backend workflow:

1. Fork the repository
2. Create a feature branch
3. Test with the provided examples
4. Submit a pull request

## Support

For issues with the local backend workflow:

1. Check the generated project documentation
2. Review the complete walkthrough guide
3. Search existing GitHub issues
4. Open a new issue with detailed information

---

**Pulumi Factory - Local Backend**  
Generated by Pulumi Factory  