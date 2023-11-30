
from simba.mixins.config_reader import ConfigReader
from simba.mixins.feature_extraction_mixin import FeatureExtractionMixin
from simba.mixins.geometry_mixin import GeometryMixin

from simba.utils.errors import NoFilesFoundError


class PiotrFeatureExtractor(ConfigReader, FeatureExtractionMixin, GeometryMixin):

    def __init__(self,
                 config_path: str):

        ConfigReader.__init__(self, config_path=config_path)
        FeatureExtractionMixin.__init__(self)
        GeometryMixin.__init__(self)
        if len(self.outlier_corrected_paths) == 0:
            raise NoFilesFoundError(msg=f'No files found in {self.outlier_corrected_dir}')

    def run(self):
        for file_cnt, file_path in enumerate(self.outlier_corrected_paths):
            print(file_path)








PiotrFeatureExtractor(config_path='/Users/simon/Desktop/envs/troubleshooting/piotr/project_folder/train-20231108-sh9-frames-with-p-lt-2_plus3-&3_best-f1.ini')