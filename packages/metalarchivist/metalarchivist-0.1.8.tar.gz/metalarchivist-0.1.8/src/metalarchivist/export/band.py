import time
import random
import concurrent.futures

import urllib3
from rich.console import Console

from ..interface import BandProfile
from .album import MetalArchivesDirectory


class BandError(Exception):
    def __init__(self, status_code):
        self.status_code = status_code

    def __repr__(self):
        return self.__name__ + f'<{self.status_code}>'


class Band:
    
    @staticmethod
    def get_profile(profile_url: str) -> BandProfile:
        while True:
            response = urllib3.request('GET', profile_url)
            status_code = response.status

            if status_code == 520:
                time.sleep(30)
                continue

            elif status_code != 200:
                raise BandError(status_code)
            
            break

        return BandProfile(profile_url, response.data)
    
    @staticmethod
    def _get_profile_thread(profile_url: str, wait_seconds=1, verbose=False) -> tuple[BandProfile | None, str]:
        console = Console()
        time.sleep(wait_seconds)
        
        response = urllib3.request('GET', profile_url)
        status_code = response.status

        if verbose:
            relative_url = profile_url.replace(MetalArchivesDirectory.METAL_ARCHIVES_ROOT, '')
            console.log((f'GET {relative_url}\n'
                         f'| status: {status_code}\n'
                         f'| wait:   {round(wait_seconds, 1)}'))

        if status_code == 520:
            return None, profile_url

        elif status_code != 200:
            raise BandError(status_code)

        return BandProfile(profile_url, response.data), profile_url

    @classmethod
    def get_profiles(cls, profile_urls: list[str], segment_size=16, 
                     depth=0, max_depth=3, verbose=False) -> list[BandProfile]:

        console = Console()
        profile_urls_swap = list()
        profiles = list()
        profile_urls_len = len(profile_urls)

        if verbose:
            console.log(f'Executing wave {depth} | {profile_urls_len} profiles')

        with concurrent.futures.ThreadPoolExecutor() as executor:
            
            processed_urls = set()

            # don't throw them all in at once
            for segment_start in range(0, profile_urls_len + segment_size, segment_size):
                segment_end = min(segment_start + segment_size, profile_urls_len)

                band_futures = list()
                for url in profile_urls[segment_start:segment_end]:
                    if url not in processed_urls:
                        future = executor.submit(cls._get_profile_thread, url, 
                                                 wait_seconds=random.randint(1, 30) / 10,
                                                 verbose=verbose)
                        band_futures.append(future)
                        processed_urls.add(url)

                # examine the remains
                for future in concurrent.futures.as_completed(band_futures):
                    profile, profile_url = future.result()
                    if profile is None:
                        profile_urls_swap.append(profile_url)
                    else:
                        profiles.append(profile)

        # if there's any left, throw them back into the pit
        if len(profile_urls_swap) > 0 and max_depth > depth:
            if verbose:
                console.log((f'Wave {depth} completed with errors'))

            profiles += cls.get_profiles(profile_urls_swap,
                                         segment_size=segment_size,
                                         depth=depth + 1, 
                                         max_depth=max_depth)
        
        return profiles
