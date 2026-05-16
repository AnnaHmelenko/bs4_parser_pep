from pathlib import Path


BASE_DIR = Path(__file__).parent

MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_URL = 'https://peps.python.org/'
PEP_NUMERICAL_URL = 'https://peps.python.org/numerical/'

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'

RESULTS_DIR_NAME = 'results'
DOWNLOADS_DIR_NAME = 'downloads'

OUTPUT_PRETTY = 'pretty'
OUTPUT_FILE = 'file'

MODE_WHATS_NEW = 'whats-new'
MODE_LATEST_VERSIONS = 'latest-versions'
MODE_DOWNLOAD = 'download'
MODE_PEP = 'pep'

MIN_PEP_TABLE_COLUMNS = 2

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
