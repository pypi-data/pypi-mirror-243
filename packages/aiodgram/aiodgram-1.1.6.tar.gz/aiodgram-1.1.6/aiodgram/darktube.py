from pytube import streams, YouTube

class DownloadVideo:
    """
    This library using for download video from YouTube.

    This work only YouTube short, if you want send user in Telegram!
    """
     
    def __init__(self) -> None:
        pass


    def download_This_Video(self,
                          link_on_video: str,
                          video_name: str,
                          resolution: int = 720
                          ):
        """
        Download video from YouTube.

        :param link_on_video: str, link on video from YouTube
        :param resolution: int, the desired resolution for the video, default 720p
        :param video_name: str, name of your video

        :return Video in folder where project


        The download speed depends on your ethernet speed.
        Sending is only available for files less than 30 MB, therefore, no half-hour videos, maximum YouTube Shorts!
        """
        yt = YouTube(link_on_video)
        
        yt.streams.filter(resolution=f"{resolution}p").first().download(filename=f'{video_name}.mp4')