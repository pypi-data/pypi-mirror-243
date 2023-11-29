import os
from datetime import datetime
from urllib.parse import urlencode


class MetalArchivesDirectory:

    METAL_ARCHIVES_ROOT = 'https://www.metal-archives.com'
    METAL_ARCHIVES_SEARCH = 'https://www.metal-archives.com/search/advanced/searching/bands'

    @classmethod
    def upcoming_releases(cls, echo=0, display_start=0, display_length=100,
                          from_date=datetime.now().strftime('%Y-%m-%d'), 
                          to_date='0000-00-00'):

        return (f'{os.path.join(cls.METAL_ARCHIVES_ROOT, "release/ajax-upcoming/json/1")}'
                f'?sEcho={echo}&iDisplayStart={display_start}&iDisplayLength={display_length}'
                f'&fromDate={from_date}&toDate={to_date}')

    @classmethod
    def search_query(cls, band_name=None, genre=None, country=None, location=None, 
                     themes=None, label_name=None, notes=None, status=None, 
                     year_from=None, year_to=None):
        """
        ?bandNotes=&status=&themes=&location=&bandLabelName=#bands
        """
        query_params = {'exactBandMatch': 1, 'bandName': band_name, 'genre': genre,
                        'country': country, 'status': status, 'location': location,
                        'bandNotes': notes, 'themes': themes, 'bandLabelName': label_name,
                        'yearCreationFrom': year_from, 'yearCreationTo': year_to}
        
        query_str = urlencode({k: v for k, v in query_params.items() if v is not None})

        return query_str