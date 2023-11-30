
import re
from datetime import datetime
from dataclasses import dataclass, field, InitVar

from .band import BandLink, Genres

import lxml.html



def _parse_release_date(release_date):
    def _try_parse_release_date(release_date: str, date_format: str):
        try:
            return datetime.strptime(release_date, date_format) \
                           .date().strftime('%Y-%m-%d')
        except ValueError:
            return None

    release_date = re.sub(r',', '', release_date)
    release_date = re.sub(r'(\d)st', r'\g<1>', release_date)
    release_date = re.sub(r'(\d)nd', r'\g<1>', release_date)
    release_date = re.sub(r'(\d)rd', r'\g<1>', release_date)
    release_date = re.sub(r'(\d)th', r'\g<1>', release_date)
    release_date = re.sub(r'\s(\d)\s', r' 0\g<1> ', release_date)

    release_date_parsed = _try_parse_release_date(release_date, '%B %d %Y')
    if not release_date_parsed:
        release_date_parsed = _try_parse_release_date(release_date, '%B %Y')
    if not release_date_parsed:
        release_date_parsed = _try_parse_release_date(release_date, '%Y-%m-%d %H:%M:%S')

    return release_date_parsed


@dataclass
class AlbumLink:
    name: str = field(init=False)
    link: str = field(init=False)

    def __init__(self, html: str):
        html_anchor = lxml.html.fragment_fromstring(html)
        self.name = html_anchor.text
        self.link = html_anchor.attrib['href']



@dataclass
class AlbumRelease:    
    band: BandLink
    album: AlbumLink

    release_type: str
    genres: Genres
    release_date_display: InitVar[str]
    added_date_display: InitVar[str | None] = field(default=None)

    release_date: str = field(init=False)
    added_date: str | None = field(init=False)

    def __post_init__(self, release_date_display, added_date_display):
        self.release_date = _parse_release_date(release_date_display)

        if added_date_display == 'N/A' or added_date_display is None:
            self.added_date = None
        else:
            added_date = re.sub(r'\/(\d)\/', '/0\1/', added_date_display)
            self.added_date = datetime.strptime(added_date, '%Y-%m-%d %H:%M:%S') \
                                      .strftime('%Y-%m-%dT%H:%M:%SZ')


@dataclass
class AlbumTrackLength:
    length_text: InitVar[str]
    hours: int = field(init=False)
    minutes: int = field(init=False)
    seconds: int = field(init=False)

    def __post_init__(self, length_text: str):
        ...


@dataclass
class AlbumTrack:
    tablerow: InitVar[lxml.html.Element]

    metallum_id: int = field(init=False)
    number: str = field(init=False)
    title: str = field(init=False)
    length: AlbumTrackLength = field(init=False)
    lyrics: str = field(init=False)

    def __post_init__(self, tablerow: lxml.html.Element):
        number, title, length, lyrics = tablerow.xpath('./td')
        metallum_id = number.xpath('./a').pop().attrib['name']

        self.metallum_id = int(metallum_id)
        self.title = title.text


@dataclass
class AlbumDescription:
    release_type: str
    release_date: str
    catalog_id: str
    label: str
    media_format: str
    version_desc: str | None = field(default=None)
    limitation: str | None = field(default=None)
    reviews: str | None = field(default=None)


@dataclass
class AlbumProfile:
    url: str
    html: InitVar[bytes]

    name: str = field(init=False)
    metallum_id: int = field(init=False)
    tracklist: list[AlbumTrack] = field(init=False)
    description: AlbumDescription = field(init=False)

    def __post_init__(self, profile_html):
        self.metallum_id = int(self.url.split('/')[-1])

        profile_document = lxml.html.document_fromstring(profile_html)
        album_desc_titles_xpath = '//div[@id="album_info"]/dl/dt/text()'
        album_desc_titles = profile_document.xpath(album_desc_titles_xpath)

        album_desc_detail_xpath = '//div[@id="album_info"]/dl/dd/text()'
        album_desc_detail = profile_document.xpath(album_desc_detail_xpath)

        self.description = self._parse_description(album_desc_titles, album_desc_detail)
        
        album_tracklist_xpath = ('//div[@id="album_tabs_tracklist"]'
                                 '//tr[@class="even" or @class="odd"]')
        album_tracklist = profile_document.xpath(album_tracklist_xpath)
        self.tracklist = list(map(AlbumTrack, album_tracklist))

    @classmethod
    def _parse_description(cls, description_titles, description_details) -> AlbumDescription:
        description = {str(dt).lower(): str(dd).strip() 
                       for dt, dd in zip(description_titles, description_details)}
        
        # scrub non alpha and whitespace
        description = {re.sub(r'[^\w\s]+', '', dt): None if dd == 'N/A' else dd 
                       for dt, dd in description.items()}
        
        # underscores
        description = {re.sub(r'\s+', '_', dt): dd
                       for dt, dd in description.items()}
        
        # scrub invalid key names
        description = {cls._scrub_key_names(dt): dd
                       for dt, dd in description.items()}

        return AlbumDescription(**description)
    
    @staticmethod
    def _scrub_key_names(key: str) -> str:
        if key == 'type':
            return 'release_type'

        if key == 'format':
            return 'media_format'

        return key
    
    @property
    def release_date(self):
        return _parse_release_date(self.description.release_date)


@dataclass
class ReleasePage:
    total_records: int = field(init=False)
    total_display_records: int = field(init=False)
    echo: int = field(init=False)
    data: list[AlbumRelease] = field(init=False)

    def __init__(self, i_total_records: int, i_total_display_records: int,
                 s_echo: int, aa_data: list):

        self.total_records = i_total_records
        self.total_display_records = i_total_display_records
        self.echo = s_echo
        self.data = sum(list(map(self._process_album_release, aa_data)), [])

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError('ReleasePage objects can only be summed '
                            'with other ReleasePage objects')

        self.data += other.data
        return self
    
    @staticmethod
    def _process_album_release(record: list[str]) -> list[AlbumRelease]:
        """ returns a list to handle the potential for splits """

        band_link, album_link, release_type, genres, *dates = record

        if re.search(r'>\s?\/\s?<', band_link):
            band_links = band_link.split(' / ')
            genre_list = genres.split(' | ')

            return [AlbumRelease(BandLink(link), AlbumLink(album_link), 
                                 release_type, Genres(genre), *dates)
                    for link, genre in zip(band_links, genre_list)]

        return [AlbumRelease(BandLink(band_link), AlbumLink(album_link), 
                             release_type, Genres(genres), *dates)]


class ReleasePages(list):
    def combine(self) -> ReleasePage:
        first_page, *remaining = self
        return sum(remaining, start=first_page)

