@echo off
REM Windows helper to lint/format/type-check
call "%~dp0..\python\.venv\Scripts\python.exe" -m ruff check ..\python
if errorlevel 1 exit /b 1
call "%~dp0..\python\.venv\Scripts\python.exe" -m black ..\python
if errorlevel 1 exit /b 1
call "%~dp0..\python\.venv\Scripts\python.exe" -m isort ..\python
if errorlevel 1 exit /b 1
call "%~dp0..\python\.venv\Scripts\python.exe" -m mypy ..\python
