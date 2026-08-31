#requires -Version 5.1

[CmdletBinding()]
param(
    [string]$DatabaseName = "school_db",
    [string]$AppUser = "school_user",
    [string]$AdminUser = "postgres",
    [string]$PgHost = "localhost",
    [int]$Port = 5432
)

$ErrorActionPreference = "Stop"

function Get-DatabaseUrlFromFile {
    param(
        [string]$Path
    )

    if (-not $Path -or -not (Test-Path -Path $Path)) {
        return $null
    }

    foreach ($line in Get-Content -Path $Path) {
        if ($line -match '^\s*DATABASE_URL\s*=\s*(.+?)\s*$') {
            return $Matches[1].Trim().Trim('"').Trim("'")
        }
    }

    return $null
}

function Get-DatabaseConnectionInfo {
    param(
        [string]$DatabaseUrl
    )

    if ([string]::IsNullOrWhiteSpace($DatabaseUrl)) {
        return $null
    }

    try {
        $uri = [System.Uri]::new($DatabaseUrl)
    }
    catch {
        return $null
    }

    if ($uri.Scheme -notmatch 'postgres') {
        return $null
    }

    if ([string]::IsNullOrWhiteSpace($uri.UserInfo)) {
        return $null
    }

    $userInfoParts = $uri.UserInfo.Split(':', 2)
    $user = [System.Uri]::UnescapeDataString($userInfoParts[0])
    $password = if ($userInfoParts.Count -gt 1) { [System.Uri]::UnescapeDataString($userInfoParts[1]) } else { $null }

    $databaseName = $uri.AbsolutePath.TrimStart('/')

    return [pscustomobject]@{
        User = $user
        Password = $password
        Host = $uri.Host
        Port = if ($uri.Port -gt 0) { $uri.Port } else { 5432 }
        Database = $databaseName
    }
}

function Resolve-PsqlExecutable {
    $cmd = Get-Command psql -ErrorAction SilentlyContinue
    if ($cmd) {
        return $cmd.Source
    }

    $candidates = @(
        "$env:ProgramFiles\PostgreSQL\*\bin\psql.exe",
        "$env:ProgramFiles(x86)\PostgreSQL\*\bin\psql.exe"
    )

    foreach ($pattern in $candidates) {
        $matches = Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue
        if ($matches -and $matches.Count -gt 0) {
            return $matches[0].FullName
        }
    }

    throw "psql.exe was not found. Ensure PostgreSQL is installed and the PostgreSQL bin directory is on PATH."
}

function Invoke-Psql {
    param(
        [string]$PsqlPath,
        [string]$User,
        [string]$Database,
        [string]$Sql,
        [string]$Password
    )

    $previousPassword = $env:PGPASSWORD
    if (-not [string]::IsNullOrWhiteSpace($Password)) {
        $env:PGPASSWORD = $Password
    }

    try {
        & $PsqlPath -h $PgHost -p $Port -U $User -d $Database -v ON_ERROR_STOP=1 -w -c $Sql
        if ($LASTEXITCODE -ne 0) {
            throw "psql command failed for user '$User' on database '$Database'."
        }
    }
    finally {
        if ($null -eq $previousPassword) {
            Remove-Item Env:PGPASSWORD -ErrorAction SilentlyContinue
        }
        else {
            $env:PGPASSWORD = $previousPassword
        }
    }
}

$backendDir = $PSScriptRoot
$envCandidates = @(
    (Join-Path $backendDir '.env'),
    (Join-Path (Split-Path -Parent $backendDir) '.env')
)

$envFile = $envCandidates | Where-Object { $_ -and (Test-Path -Path $_) } | Select-Object -First 1
$dbUrl = Get-DatabaseUrlFromFile -Path $envFile
$dbInfo = if ($dbUrl) { Get-DatabaseConnectionInfo -DatabaseUrl $dbUrl } else { $null }

Write-Host "Checking PostgreSQL local development setup..." -ForegroundColor Cyan
Write-Host "Database: $DatabaseName" -ForegroundColor Cyan
Write-Host "App user: $AppUser" -ForegroundColor Cyan
Write-Host "Host: ${PgHost}:$Port" -ForegroundColor Cyan

$psqlPath = Resolve-PsqlExecutable

$roleCheckSql = @"
SELECT 1
FROM pg_roles
WHERE rolname = '$AppUser';
"@

$databaseCheckSql = @"
SELECT 1
FROM pg_database
WHERE datname = '$DatabaseName';
"@

$adminPassword = $env:PGPASSWORD
if (-not $adminPassword) {
    Write-Host "Administrator authentication is required once to grant the required schema privileges." -ForegroundColor Yellow
    $securePassword = Read-Host "Enter PostgreSQL admin password for user '$AdminUser'" -AsSecureString
    $adminPassword = [System.Net.NetworkCredential]::new([string]::Empty, $securePassword).Password
}

Write-Host "Checking that the target database and app role exist..." -ForegroundColor Cyan
Invoke-Psql -PsqlPath $psqlPath -User $AdminUser -Database "postgres" -Sql $databaseCheckSql -Password $adminPassword
Invoke-Psql -PsqlPath $psqlPath -User $AdminUser -Database "postgres" -Sql $roleCheckSql -Password $adminPassword

# Ensure the database and role actually exist before trying to grant privileges.
$databaseExists = (& $psqlPath -h $PgHost -p $Port -U $AdminUser -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname = '$DatabaseName';")
$roleExists = (& $psqlPath -h $PgHost -p $Port -U $AdminUser -d postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname = '$AppUser';")

if (($databaseExists -ne "1") -or ($roleExists -ne "1")) {
    throw "Database '$DatabaseName' or role '$AppUser' does not exist. Create them first or confirm the local PostgreSQL setup matches the project configuration."
}

$grantSql = @"
GRANT USAGE ON SCHEMA public TO "$AppUser";
GRANT CREATE ON SCHEMA public TO "$AppUser";
ALTER SCHEMA public OWNER TO "$AppUser";
"@

Write-Host "Granting the minimal required privileges on the public schema..." -ForegroundColor Cyan
Invoke-Psql -PsqlPath $psqlPath -User $AdminUser -Database $DatabaseName -Sql $grantSql -Password $adminPassword

$appPassword = $null
if ($dbInfo -and $dbInfo.User -eq $AppUser -and -not [string]::IsNullOrWhiteSpace($dbInfo.Password)) {
    $appPassword = $dbInfo.Password
}

if (-not $appPassword) {
    $secureAppPassword = Read-Host "Enter the password for PostgreSQL user '$AppUser' to verify connectivity" -AsSecureString
    $appPassword = [System.Net.NetworkCredential]::new([string]::Empty, $secureAppPassword).Password
}

$verifySql = "SELECT current_user, current_database();"
Write-Host "Verifying that '$AppUser' can connect to '$DatabaseName'..." -ForegroundColor Cyan
Invoke-Psql -PsqlPath $psqlPath -User $AppUser -Database $DatabaseName -Sql $verifySql -Password $appPassword

Write-Host ""
Write-Host "Local PostgreSQL setup is complete." -ForegroundColor Green
Write-Host "Use this Alembic command from the backend folder:" -ForegroundColor Green
Write-Host "alembic revision --autogenerate -m \"create school table\"" -ForegroundColor Yellow
