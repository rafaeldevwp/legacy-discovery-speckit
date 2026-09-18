@echo off
setlocal
chcp 65001 >nul
cls
echo ================================================================
echo   Legacy Discovery + Spec Kit - Instalador Unico
echo ================================================================
echo.
echo Informe a pasta RAIZ do seu repositorio legado.
echo Exemplo: C:\Projetos\MeuSistemaLegado
echo.
set /p TARGET=Repositorio: 
if "%TARGET%"=="" set "TARGET=%CD%"

echo.
if exist "C:\Program Files\Python314\python.exe" (
  "C:\Program Files\Python314\python.exe" "%~dp0install.py" --target "%TARGET%"
  goto :done
)

where py >nul 2>nul
if %ERRORLEVEL%==0 (
  py -3.11 "%~dp0install.py" --target "%TARGET%"
  goto :done
)
where python >nul 2>nul
if %ERRORLEVEL%==0 (
  python "%~dp0install.py" --target "%TARGET%"
  goto :done
)

echo ERRO: Python 3.11+ nao foi encontrado.
echo Instale Python 3.11 ou superior e execute este arquivo novamente.
set ERRORLEVEL=1

:done
echo.
if not "%ERRORLEVEL%"=="0" (
  echo A instalacao encontrou um erro. Leia a mensagem acima.
) else (
  echo Instalacao finalizada. Abra o repositorio no VS Code.
)
echo.
pause
endlocal
