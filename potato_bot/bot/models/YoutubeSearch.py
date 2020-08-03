from aiohttp import ClientSession
from urllib import parse
from json import loads

BASE_URL = "https://youtube.com/results?search_query="
BASE_VIDEO_URL = "https://youtube.com/watch?v="


class YoutubeSearch:
    @staticmethod
    async def search(client: ClientSession, text: str):
        results = []
        parsed_text = parse.quote_plus(text)
        url = BASE_URL + parsed_text
        resp = await client.get(url)
        html = await resp.text()
        start = (
            html.index('window["ytInitialData"]') + len('window["ytInitialData"]') + 3
        )
        end = html.index("};", start) + 1
        json_str = html[start:end]
        data = loads(json_str)

        videos = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
            "sectionListRenderer"
        ]["contents"][0]["itemSectionRenderer"]["contents"]

        for video in videos:
            res = {}
            if "videoRenderer" in video.keys():
                video_data = video.get("videoRenderer", {})
                res["id"] = video_data.get("videoId", None)
                res["video_url"] = BASE_VIDEO_URL + res["id"]
                res["title"] = (
                    video_data.get("title", {}).get("runs", [[{}]])[0].get("text", None)
                )

                results.append(res)

                if len(results) >= 10:
                    break

        return results
