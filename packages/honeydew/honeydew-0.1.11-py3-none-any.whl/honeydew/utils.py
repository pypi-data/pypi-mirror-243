import calendar
from datetime import datetime
import os
class Utils:
    """Instantiate utilities.
    """    
    def __init__(self, name=''):
        """Instantiate utilities.
        """    
        
    def convert_dt_to_epoch(self, dt):
        """
        Convert datetime in UTC time zone to epoch (unix time)
        Args:
            dt (datetime): datetime
        Returns:
            result (int): epoch or unix time
        """
        return calendar.timegm(dt.utctimetuple())

    def convert_epoch_to_dt(self, epoch):
        """
        Convert epoch to datetime
        Args:
            epoch (int): epoch or unix time
        Returns:
            result (datetime): datetime
        """
        if epoch > 9999999999:
            epoch = round(epoch/1000)
        return datetime.fromtimestamp(s)
    
def compress(dir_path, file_pattern='*', delete_after_compression=False):
    """Compress files with pattern or prefix from a directory. Type "*" for all files.
    Args:
        dir_path (str): Directory path
        file_pattern (str): File pattern or prefix
        delete_after_zip (bool): Delete original files after compression
    """

    import gzip
    import shutil
    from pathlib import Path
    for p in Path(dir_path).glob(file_pattern):
        with open(p, 'rb') as f_in:
            with gzip.open(f"{p}.gz", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        if delete_after_compression:
            os.remove(p)

def compress_parallel(dir_path, file_pattern='*', delete_after_compressing=False):
    """Compress files with pattern or prefix from a directory parallely. Type "*" for all files."""
    from pathlib import Path  
    from pigz_python import PigzFile
    import os
    for p in Path(dir_path).glob(file_pattern):
        pigz_file = PigzFile(p)
        pigz_file.process_compression_target()
        if delete_after_compressing:
            os.remove(p)            