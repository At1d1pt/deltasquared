@echo off
cls
set /p token="Bot Token: "
set /p prefix="Bot Prefix: ",
set /p log="Log Channel: "
echo {"bot-token": "%token%" , "prefix": %prefix% , "log_channel": %log%}>config.json
cls
@echo on