# ui_api_template

## Test automation template (Python)

This is a Python test automation template that includes UI and API tests, as well as class methods and configuration files. For example, the site [Trello.com](https://trello.com/) is taken. You can use the code to suit your needs by replacing the test data.

---

Dies ist eine Vorlage für die Python-Testautomatisierung, die UI- und API-Tests sowie Klassenmethoden und Konfigurationsdateien enthält. Für einen Beispiel würde die Seite [Trello.com](https://trello.com/) genommen. Sie können den Code entsprechend Ihren Anforderungen verwenden, indem Sie die Testdaten ersetzen.

---

### INSTRUCTION
1. Clone repository: 
***command*** - `git clone https://github.com/vladicom/ui_api_template.git`
2. Install libraries:
   - ``python install pip``
   - ``pip install pytest``
   - ``pip install selenium``
   - ``pip install webdriver-manager``
   - ``pip install allure``
3. Registration on the website [Trello.com](https://trello.com/)
4. Fill files (test_data) with your test data
5. Start tests:
   1. all tests
    - ``python -m pytest``
    - or ``py -m pytest``
   2. Ui tests
   - ``py -m pytest test\test_ui.py``
   3. API tests
    - ``py -m pytest test\test_api.py``
6. For Test-report start:
   - ``allure serve allure-files``
  
### Useful links:
- [PYTEST -Full pytest documentation](https://docs.pytest.org/en/stable/contents.html)
- [PyPi-for libraries](https://pypi.org)
- [Selenium](https://www.selenium.dev/documentation/)
- [Allure-Report](https://allurereport.org/)

---

### Stack:
- pytest
- selenium
- request
- allure
- config

### Structure:
- ./test - testfiles
- ./pages - page methods
- ./configurations - configuration method
- ./testdata - test-data method
- test_config.ini - configuration file
- test_data.json - file with your test-data
