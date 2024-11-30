from sqlalchemy import Column, Integer, String
from dal.models import Base

class DownloadedAudio(Base):
    __tablename__ = "downloaded_audio"
    id = Column(Integer, primary_key=True, autoincrement=True)
    yt_id = Column(Integer)
    file_path = Column(String)
    search_query_used = Column(String)