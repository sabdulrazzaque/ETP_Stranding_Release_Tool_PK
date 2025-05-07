@echo off
REM Absolute path to python.exe inside your NED environment
SET PYTHON_EXE="C:\Users\Shoaib\anaconda3\envs\NED\python.exe"

REM Navigate to your project
cd /d D:\Turlte_Monitoring\turtle_monitor

REM Force Streamlit to run using NED's python
%PYTHON_EXE% -m streamlit run main.py

PAUSE
