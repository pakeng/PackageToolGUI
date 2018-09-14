@echo off

java -jar "signerApk.jar" -XX:-UseSplitVerifier
zipalign -f 4 signed.apk zipaligned_signed.apk  
call clean.bat