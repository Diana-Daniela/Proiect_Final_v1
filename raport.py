import unittest
import HtmlTestRunner
from Suite_teste import Teste_Proiect_Final

class TestSuites(unittest.TestCase):
    def test_suite(self):
        test_to_run = unittest.TestSuite()
        test_to_run.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(Teste_Proiect_Final),
        ])
        runner = HtmlTestRunner.HTMLTestRunner(
            combine_reports=True,
            report_name='Raport proiect final',
            report_title='Raport 1'
        )
        runner.run(test_to_run)