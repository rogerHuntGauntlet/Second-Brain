@echo off
:: PhD Research Proposal Folder Structure and README Files Setup

:: Prompt user for project name
set /p PROJECT_NAME=Enter the title of your PhD Research Proposal: 
set PROJECT_DIR=C:\Users\roger\PhdResearch\%PROJECT_NAME%



:: Check if the project folder already exists
if exist "%PROJECT_DIR%" (
    echo Project "%PROJECT_NAME%" already exists. Aborting!
    exit /b
)

:: Create the project folder structure
mkdir "%PROJECT_DIR%"
mkdir "%PROJECT_DIR%\literature_review"
mkdir "%PROJECT_DIR%\methodology"
mkdir "%PROJECT_DIR%\experiments"
mkdir "%PROJECT_DIR%\data_analysis"
mkdir "%PROJECT_DIR%\results"
mkdir "%PROJECT_DIR%\conclusion"
mkdir "%PROJECT_DIR%\references"
mkdir "%PROJECT_DIR%\appendix"
mkdir "%PROJECT_DIR%\proposal"

:: Create README files for each folder
echo # PhD Research Proposal > "%PROJECT_DIR%\README.md"
echo This project is dedicated to developing a comprehensive PhD research proposal. >> "%PROJECT_DIR%\README.md"
echo. >> "%PROJECT_DIR%\README.md"
echo ## Sections >> "%PROJECT_DIR%\README.md"
echo - [Literature Review](literature_review/README.md) >> "%PROJECT_DIR%\README.md"
echo - [Methodology](methodology/README.md) >> "%PROJECT_DIR%\README.md"
echo - [Experiments](experiments/README.md) >> "%PROJECT_DIR%\README.md"
echo - [Data Analysis](data_analysis/README.md) >> "%PROJECT_DIR%\README.md"
echo - [Results](results/README.md) >> "%PROJECT_DIR%\README.md"
echo - [Conclusion](conclusion/README.md) >> "%PROJECT_DIR%\README.md"
echo - [References](references/README.md) >> "%PROJECT_DIR%\README.md"
echo - [Appendix](appendix/README.md) >> "%PROJECT_DIR%\README.md"
echo - [Proposal](proposal/README.md) >> "%PROJECT_DIR%\README.md"

echo # Literature Review > "%PROJECT_DIR%\literature_review\README.md"
echo In this section, you will summarize the existing research and literature related to your PhD topic. >> "%PROJECT_DIR%\literature_review\README.md"

echo # Methodology > "%PROJECT_DIR%\methodology\README.md"
echo This section outlines the research methods you will use to conduct your study. >> "%PROJECT_DIR%\methodology\README.md"

echo # Experiments > "%PROJECT_DIR%\experiments\README.md"
echo This section outlines the experiments or trials you plan to conduct for your research. >> "%PROJECT_DIR%\experiments\README.md"

echo # Data Analysis > "%PROJECT_DIR%\data_analysis\README.md"
echo This section outlines how you will analyze the data collected from your experiments. >> "%PROJECT_DIR%\data_analysis\README.md"

echo # Results > "%PROJECT_DIR%\results\README.md"
echo This section is dedicated to documenting the findings from your research. >> "%PROJECT_DIR%\results\README.md"

echo # Conclusion > "%PROJECT_DIR%\conclusion\README.md"
echo The conclusion summarizes your findings and discusses their significance. >> "%PROJECT_DIR%\conclusion\README.md"

echo # References > "%PROJECT_DIR%\references\README.md"
echo This section will list all the references cited throughout your research proposal. >> "%PROJECT_DIR%\references\README.md"

echo # Appendix > "%PROJECT_DIR%\appendix\README.md"
echo This section stores supplementary materials supporting your research proposal. >> "%PROJECT_DIR%\appendix\README.md"

echo # Proposal > "%PROJECT_DIR%\proposal\README.md"
echo This section is an overview of your interest and approach. >> "%PROJECT_DIR%\proposal\README.md"

echo PhD Research Proposal Project "%PROJECT_NAME%" initialized at "%PROJECT_DIR%".
