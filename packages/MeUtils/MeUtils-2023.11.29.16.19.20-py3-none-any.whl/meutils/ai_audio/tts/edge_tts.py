#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : tts
# @Time         : 2023/11/3 15:21
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 增加固定时长的生成

from meutils.pipe import *

import edge_tts


class EdgeTTS(object):

    def __init__(self):
        pass

    def create(
            self,
            text: Union[str, List[str]],
            role: str = '云希',
            rate: float = 0,
            volume: float = 0,
            filename: Optional[None] = None
    ):
        """ todo：增加字幕合成，增加 多进程，多线程
            for i, srtitem in enumerate(tqdm(pysrt.open('subtitle.srt'))):
                create(srtitem.text, filename=f"wav/{i:0>6}.wav")
        """
        if isinstance(text, str):
            text = [text]

        acreate = partial(self.acreate, role=role, rate=rate, volume=volume, filename=filename)

        return text | xmap(acreate) | xAsyncio

    @alru_cache
    async def acreate(
            self,
            text: str,
            role: str = '云希',
            rate: float = 0,
            volume: float = 0,
            filename: Optional[None] = None,
            **kwargs
    ):
        voices = (await edge_tts.VoicesManager.create()).find(**{'ShortName': role}) or [{}]
        voice = voices[0].get('ShortName', 'zh-CN-YunxiNeural')

        rate = f"{'+' if rate >= 0 else ''}{rate}%"
        volume = f"{'+' if volume >= 0 else ''}{volume}%"

        communicate = edge_tts.Communicate(text, voice=voice, rate=rate, volume=volume)  # todo: 文件流

        filename = filename or f"{time.time()}.mp3"  # f"{str(datetime.datetime.now())[:19]}.mp3"
        await communicate.save(filename)
        return filename

    @staticmethod
    @lru_cache
    def find_voices(**kwargs: Any):  # @alru_cache
        """https://speech.platform.bing.com/consumer/speech/synthesize/readaloud/voices/list?trustedclienttoken=6A5AA1D4EAFF4E9FB37E23D68491D6F4
            find_voices(**{"Locale": "en-US"})
            find_voices(**{'ShortName': 'zh-CN-XiaoxiaoNeural'})
        """
        return asyncio.run(edge_tts.VoicesManager.create()).find(**kwargs or {"Locale": "zh-CN"})


if __name__ == '__main__':
    print(EdgeTTS().create(['不知道'] * 10))

    # cls = EdgeTTS()
    # cls.create('不知道')
    # cls.create('不知道')
