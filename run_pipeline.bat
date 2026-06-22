@echo off
cd /d C:\Users\hp\Desktop\smart-hr-analytics\etl
C:\Users\hp\anaconda3\envs\smart-hr\python.exe pipeline.py
exit %ERRORLEVEL%