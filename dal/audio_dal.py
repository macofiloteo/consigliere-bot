from sqlalchemy import select
from dal.models.downloaded_audio import DownloadedAudio
from sqlalchemy.orm import Session

class AudioDAL():
    def __init__(self, session: Session) -> None:
        self.session = session

    def insert(self, yt_id: int, file_path: str, search_query_used: str) -> None:
        new_downloaded_audio = DownloadedAudio(
            yt_id=yt_id, 
            file_path=file_path,
            search_query_used=search_query_used
        )
        self.session.add(new_downloaded_audio)

    def get(self, search_query: str):
        query = (
            select(DownloadedAudio)
            .where(DownloadedAudio.search_query_used == search_query)
        )
        query_results = self.session.execute(query)
        return query_results.scalars().unique().all()