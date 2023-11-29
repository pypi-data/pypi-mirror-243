from coverage import Coverage
from multiprocessing import Process
import os


class CoverageProcess(Process):
    def run(self):
        cov = Coverage(config_file=True, data_suffix=os.getpid(), auto_data=True)
        cov._warn_no_data = False
        cov.start()

        try:
            super().run()
        finally:
            cov.stop()
            cov.save()
