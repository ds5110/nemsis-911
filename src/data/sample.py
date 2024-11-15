import pandas as pd
import numpy as np
from pathlib import Path

# Since script is in root/src/data/ and pickle is in root/data/processed/
# We need to go up two levels from script location (src/data) to reach root, then down to data/processed
pickle_path = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'events_renamed.pickle'

print(f"Looking for pickle file at: {pickle_path}")
print(f"Pickle file exists: {pickle_path.exists()}")