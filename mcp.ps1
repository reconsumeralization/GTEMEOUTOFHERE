# PowerShell helper for managing MCP Docker services.
# Usage examples:
#   ./mcp.ps1 build
#   ./mcp.ps1 up backend
#   ./mcp.ps1 logs frontend
#   ./mcp.ps1 down

param(
    [ValidateSet('build','up','down','stop','logs','restart')]
    [string]$Action = 'up',
    [ValidateSet('backend','frontend','all')]
    [string]$Service = 'all'
)

$ComposeFile = "docker-compose.mcp.yml"

if (-not (Test-Path $ComposeFile)) {
    Write-Error "Compose file '$ComposeFile' not found. Run from repo root."
    exit 1
}

function Resolve-Service([string]$svc) {
    switch ($svc) {
        'backend'  { return 'mcp-backend' }
        'frontend' { return 'mcp-frontend' }
        default    { return @('mcp-backend','mcp-frontend') }
    }
}

$services = Resolve-Service $Service

switch ($Action) {
    'build' {
        docker compose -f $ComposeFile build $services
        break
    }
    'up' {
        docker compose -f $ComposeFile up $services
        break
    }
    'down' {
        docker compose -f $ComposeFile down
        break
    }
    'stop' {
        docker compose -f $ComposeFile stop $services
        break
    }
    'logs' {
        docker compose -f $ComposeFile logs -f $services
        break
    }
    'restart' {
        docker compose -f $ComposeFile restart $services
        break
    }
    default {
        Write-Error "Unknown action $Action"
    }
}

