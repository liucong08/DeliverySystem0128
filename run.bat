cd ./testCase
pytest -s --alluredir ../outFiles/report/tmp
allure serve ../outFiles/report/tmp