# Import the dependencies.
from pathlib import Path
from sqlalchemy import create_engine
import pandas as pd


#################################################
# Database Setup
#################################################
# Create a reference to the file. 
database_path = Path("Resources/hawaii.sqlite")

# Create Engine
engine = create_engine(f"sqlite:///{database_path}")
conn = engine.connect()

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with = engine, reflect = True)

# Save references to each table
Measurement = Base.classes.measurement

Station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
