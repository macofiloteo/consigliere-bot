from sqlalchemy.orm import Session

from dal.audio_dal import AudioDAL
from workers.downloader_thread import download_video

def get_audio_path(session: Session, search_query: str):
    audio_dal = AudioDAL(session=session)
    retrieved_audios = audio_dal.get(search_query=search_query)
    if retrieved_audios:
        downloaded_file_path = str(retrieved_audios[0].file_path)
    else:
        downloaded_file_path, yt_id = download_video(search_query)
        audio_dal.insert(
            yt_id=yt_id,
            file_path=downloaded_file_path,
            search_query_used=search_query
        )
    if not downloaded_file_path:
        raise FileNotFoundError

    return downloaded_file_path