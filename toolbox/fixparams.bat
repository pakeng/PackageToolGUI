@echo off
echo ----------------------
echo fix appid and package
echo ----------------------
python fixparams.py %1
echo %1
echo ----------------------
echo  rebuild apk 
echo ----------------------
apktool b decompile

pause