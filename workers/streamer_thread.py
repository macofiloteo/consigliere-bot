from threading import Thread
from time import sleep

from discord import FFmpegPCMAudio

from exceptions import NoWorkerExists
from logger import logger

class StatusEnum(str):
    IDLE = "IDLE"
    PLAYING = "PLAYING"

class AudioStreamerWorker:
    def __init__(self, guild, voice_client) -> None:
        self.guild = guild
        self.voice_client = voice_client
        self.stream_thread: Thread | None = None
        self.queued_files: list[str] = []
        self.now_playing: str | None = None
        self.status = StatusEnum.IDLE
        self.stream_thread = Thread(target=self.start_stream)
        self.stream_thread.start()


    def queue(self, file_path: str) -> None:
        self.queued_files.append(file_path)
        logger.info(f"Queued With New Added Entry: {file_path}")

    def skip(self) -> None:
        logger.info(f"Stopped Playing: {self.now_playing}")
        self.voice_client.stop()
        self._clear_now_playing()

    def _clear_now_playing(self) -> None:
        self.now_playing = None

    def play(self) -> None:
        self.status = StatusEnum.PLAYING

    def start_stream(self) -> None:
        while True:
            if not self.queued_files or self.now_playing or self.status == StatusEnum.IDLE:
                sleep(1)
                continue
            file_path = self.queued_files.pop(0)
            logger.info(f"Queued: {self.queued_files}")
            self.now_playing = file_path
            logger.info(f"Now Playing: {file_path}")
            try:
                self.voice_client.play(FFmpegPCMAudio(executable='/usr/bin/ffmpeg', source=file_path), after=lambda e: self._clear_now_playing())
            except Exception as e:
                raise e


class AudioStreamerManager:
    def __init__(self) -> None:
        self.workers: dict[int, AudioStreamerWorker] = {}

    def get_worker(self, guild_id: int) -> AudioStreamerWorker:
        return self.workers.get(guild_id)

    def create_worker(self, guild, voice_client) -> AudioStreamerWorker:
        guild_id = guild.id
        worker = AudioStreamerWorker(guild, voice_client)
        self.workers[guild_id] = worker
        return worker

    def queue_audio_file(self, guild, voice_client, file_path: str) -> None:
        worker = self.get_worker(guild.id)
        if not worker:
            worker = self.create_worker(guild, voice_client)
        worker.queue(file_path)
        worker.play()
    
    def skip_now_playing(self, guild) -> None:
        worker = self.get_worker(guild.id)
        if not worker:
            raise NoWorkerExists
        worker.skip()
        return