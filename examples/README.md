# COSURVIVAL Examples

This directory contains example scripts and sample data for using COSURVIVAL.

## Example Scripts

### `example_usage.py`

Basic example of running the COSURVIVAL pipeline.

```bash
python examples/example_usage.py
```

## Sample Data Format

Your CSV should include columns matching these patterns:

### Required Columns
- **User ID**: `uid`, `userid`, `UserId`, etc.
- **Timestamp**: `date`, `timestamp`, `DateTime`, etc.
- **Activity Type**: `type`, `activitytype`, `Action`, etc.

### Optional Columns
- **User Name**: `name`, `username`, `DisplayName`
- **Email**: `email`, `EmailAddress`
- **Company**: `companyid`, `companyname`
- **Group**: `groupid`, `groupname`
- **Provider**: `pid`, `providerid`, `providername`
- **State Changes**: `stateold`, `statenew`
- **Relationships**: `uidopp`, `uidreq`, `roleid`

See the main [README.md](../README.md) for complete column patterns.

## Creating Sample Data

You can create sample data in CSV format:

```csv
uid,date,type,companyid,groupid,providerid
user001,2024-01-01,login,company1,team1,provider1
user001,2024-01-01,access,company1,team1,provider1
user002,2024-01-01,login,company1,team2,provider2
user001,2024-01-02,collaborate,company1,team1,provider1
```

## Running Examples

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variable:**
   ```bash
   # Windows (PowerShell)
   $env:COSURVIVAL_SECRET_KEY = "dev-secret-key"
   
   # macOS/Linux
   export COSURVIVAL_SECRET_KEY="dev-secret-key"
   ```

3. **Run example:**
   ```bash
   python examples/example_usage.py
   ```

## Next Steps

- Read the main [README.md](../README.md) for full documentation
- Check [CONTRIBUTING.md](../CONTRIBUTING.md) to contribute examples
- Review [PROJECT_STRUCTURE.md](../PROJECT_STRUCTURE.md) for architecture details

