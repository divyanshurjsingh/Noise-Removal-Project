import sqlalchemy
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
Base=declarative_base()
class AudioFile(Base):
    __tablename__="audio_file"
    id=Column(Integer, primary_key=True)
    file_name=Column(String)
    file_path=Column(String)
    date_of_upload=Column(DateTime,default=datetime.utcnow, nullable=False )
    file_extension=Column(String)
if __name__ == "__main__":
    engine=create_engine('sqlite:///audio_database.sqlite3')    # this create an empty database
    Base.metadata.create_all(engine)                            # this create all the tables and their columns inside our database.
                                                                