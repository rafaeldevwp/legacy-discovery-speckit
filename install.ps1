param(
    [string]$TargetPath = (Get-Location).Path,
    [switch]$SkipSpecKitInstall,
    [switch]$SkipSpecKitInit,
    [switch]$KeepLegacyV1
)

$ErrorActionPreference = "Stop"
$installer = Join-Path $PSScriptRoot "install.py"
$argsList = @($installer, "--target", $TargetPath)
if ($SkipSpecKitInstall) { $argsList += "--skip-speckit-install" }
if ($SkipSpecKitInit) { $argsList += "--skip-speckit-init" }
if ($KeepLegacyV1) { $argsList += "--keep-legacy-v1" }

if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3.11 @argsList
    exit $LASTEXITCODE
}
if (Get-Command python -ErrorAction SilentlyContinue) {
    & python @argsList
    exit $LASTEXITCODE
}
throw "Python 3.11+ não encontrado. Instale Python 3.11+ e tente novamente."
