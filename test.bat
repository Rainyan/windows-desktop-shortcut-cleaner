@ECHO off

:: Uncomment this to use your dev env of choice locally...
::SET SCLEANER=uv run src\cleaner.py
:: ...or else, use this line below, if installed globally (CI default):
SET SCLEANER=scleaner

FOR /F "tokens=* USEBACKQ" %%F IN (`%SCLEANER% --print-my-desktop-dir`) DO (
  SET DESKTOP=%%F
)
SET PUSH=PUSHD "%DESKTOP%"

SET TEST_FILE_LNK=foo.lnk
SET TEST_FILE_URL=bar.url

%PUSH%

FOR %%f in ("%TEST_FILE_LNK%") DO SET TEST_FILE_LNK_NO_EXT=%%~nf
REM .lnk file already exists
IF EXIST ".\%TEST_FILE_LNK%" (ECHO EXIT 1 & GOTO end)

FOR %%f in ("%TEST_FILE_URL%") DO SET TEST_FILE_URL_NO_EXT=%%~nf
REM .url file already exists
IF EXIST ".\%TEST_FILE_URL%" (ECHO EXIT 2 & GOTO end)

ECHO NUL > %TEST_FILE_LNK%
REM .lnk doesn't exist after creation
IF NOT EXIST ".\%TEST_FILE_LNK%" (ECHO EXIT 3 & GOTO end)

ECHO NUL > %TEST_FILE_URL%
REM .url doesn't exist after creation
IF NOT EXIST ".\%TEST_FILE_URL%" (ECHO EXIT 4 & GOTO end)


:: uncomment to just create the test files from above, without running any of the tests below
::GOTO end


POPD
%SCLEANER%
%PUSH%
REM Dry-run fails
IF NOT EXIST ".\%TEST_FILE_LNK%" (ECHO EXIT 5 & GOTO end)
IF NOT EXIST ".\%TEST_FILE_URL%" (ECHO EXIT 6 & GOTO end)

POPD
%SCLEANER% -e %TEST_FILE_LNK_NO_EXT%,%TEST_FILE_URL_NO_EXT% -f
%PUSH%
REM Filename exception fails
IF NOT EXIST ".\%TEST_FILE_LNK%" (ECHO EXIT 7 & GOTO end)
IF NOT EXIST ".\%TEST_FILE_URL%" (ECHO EXIT 8 & GOTO end)

POPD
%SCLEANER% -f -e %TEST_FILE_LNK_NO_EXT%
%PUSH%
REM Filename exception fails
IF NOT EXIST ".\%TEST_FILE_LNK%" (ECHO EXIT 9 & GOTO end)
IF NOT EXIST ".\%TEST_FILE_URL%" (ECHO EXIT 10 & GOTO end)

POPD
%SCLEANER% -f -d "PublicDesktop"
%PUSH%
REM Wrong desktop folder is cleaned
IF NOT EXIST ".\%TEST_FILE_LNK%" (ECHO EXIT 11 & GOTO end)
IF NOT EXIST ".\%TEST_FILE_URL%" (ECHO EXIT 12 & GOTO end)

POPD
%SCLEANER% --print-my-desktop-dir
%PUSH%
REM Print-my-desktop doesn't exit correctly
IF NOT EXIST ".\%TEST_FILE_LNK%" (ECHO EXIT 13 & GOTO end)

POPD
%SCLEANER% -f -E "lnk,url"
%PUSH%
REM The file is not removed even though it should
IF EXIST ".\%TEST_FILE_LNK%" (ECHO EXIT 14 & GOTO end)
IF EXIST ".\%TEST_FILE_URL%" (ECHO EXIT 15 & GOTO end)

:end
POPD
