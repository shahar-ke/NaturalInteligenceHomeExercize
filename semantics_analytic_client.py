import datetime
from typing import List, Tuple, Dict


class SemanticAnalyticClient:
    def __init__(self,
                 server_url: str = 'http://localhost:8008',
                 ads_end_point: str = 'campaigns/ads',
                 ds_end_point: str = 'ds/words/quality'):
        self.quality_words: List[Tuple[str, float]] = list()
        # need to change to
        now = datetime.datetime.now()
        self.last_update_time = now.replace(day=now.day - 1, hour=5, minute=0, second=0, microsecond=0)
        self.server_url = server_url
        self.ads_end_point = ads_end_point
        self.ds_end_point = ds_end_point

    def analyse_ad_words(self):
        now = datetime.datetime.now()
        if (now - self.last_update_time).days < 1:
            print('current analysis still relevant')
            return
        ads_count = self.get_ads_count()
        word_score: Dict[str, float] = dict()
        for ad_num in range(1, ads_count + 1):
            ad = self.get_ad(ad_num)
            ad = ad.strip()
            if not ad:
                print(f'no ad for {ad_num}')
                continue
            for ad_word in ad.split():
                ad_word = ad_word.strip()
                if not ad_word:
                    continue
                ad_word = ad_word.lower()
                if ad_word in word_score:
                    continue
                ad_word_semantic = self.get_word_semantics(ad_word)
                word_score[ad_word] = ad_word_semantic
        self.quality_words = [(word, score) for word, score in word_score.items() if score > 0]
        self.quality_words.sort(key=lambda word_score_item: word_score_item[1], reverse=True)

    def get_words_score(self) -> List[Tuple[str, float]]:
        self.analyse_ad_words()
        return self.quality_words

    def get_ads_count(self) -> int:
        req_url = f'{self.server_url}/{self.ads_end_point}/count'
        resp = self._send_request(req_url)
        assert resp, 'could not get response from server'
        ads_count = 0
        try:
            ads_count = int(resp.text)
        except Exception as e:
            print(f'invalid count response: {resp.text}')
            print(f'caught: {str(e)}')
        return ads_count

    def get_ad(self, ad_num) -> str:
        req_url = f'{self.server_url}/{self.ads_end_point}/{ad_num}'
        resp = self._send_request(req_url)
        assert resp, 'could not get response from server'
        return str(resp.text)

    def get_word_semantics(self, ad_word: str) -> float:
        req_url = f'{self.server_url}/{self.ds_end_point}'
        resp = self._send_request(req_url, url_params={'word': ad_word})
        assert resp, 'could not get response from server'
        word_score = float('-inf')
        try:
            word_score = float(resp.text)
        except Exception as e:
            print(f'invalid word score: {resp.text}')
            print(f'caught: {str(e)}')
        return word_score
