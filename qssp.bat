@echo off
setlocal
cd /d "%~dp0"

:: Request Admin
net session >nul 2>&1 || (powershell start -verb runas '%~f0' & exit /b)

:: Launch the tool
start "" "bin\alacritty.exe" --config-file "config\alacritty.toml" --hold -e python main.py