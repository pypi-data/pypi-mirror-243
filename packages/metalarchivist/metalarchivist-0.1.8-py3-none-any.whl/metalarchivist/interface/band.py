
import re
import json

from enum import StrEnum, auto
from dataclasses import dataclass, field, asdict, InitVar

import lxml.html



class InvalidAttributeError(Exception):
    ...



class Period(StrEnum):
    EARLY = auto()
    MID = auto()
    LATER = auto()
    ALL = auto()
    ERROR = auto()

    @classmethod
    def has_value(cls, value) -> set:
        return value in cls._value2member_map_



@dataclass(frozen=True)
class GenrePhase:
    name: str
    period: Period = field(default=Period.ALL)



class GenreJunk(StrEnum):
    METAL = auto()
    ELEMENTS = auto()
    INFLUENCES = auto()
    MUSIC = auto()
    AND = auto()
    WITH = auto()

    @classmethod
    def has_value(cls, value) -> bool:
        return value.lower() in cls._value2member_map_


@dataclass
class Genres:
    """ Handle genres specified in text assuming 
        the conventions applied by metal-archives.com
        
        Phases: separated by semicolons (;), denotes a change
            in a bands sound over a series of periods wrapped in
            parentheses, *early*, *mid*, and *later*. See `GenrePhase`.

            *e.g* Doom Metal (early); Post-Rock (later)

        Multiples: A slash (/) indicates that a band fits within
            multiple genres. Phases are subdivided into multiples,
            where applicable. Bands without phases will likewise
            contain multiples.

            *e.g* Drone/Doom Metal (early); Psychedelic/Post-Rock (later),
                Progressive Death/Black Metal

        Modifiers: A genre can be modified into a variant with descriptive
            text, delimited by a space ( ).

            *e.g* Progressive Death Metal

        Junk: Words that are largely uninformative can be removed, the most
            common being "Metal". See `GenreJunk`.

            *e.g* Symphonic Gothic Metal with Folk influences
    """

    full_genre: str
    clean_genre: str = field(init=False)
    phases: list[GenrePhase] = field(init=False)

    def __post_init__(self):
        # scrub anomalies
        clean_genre = re.sub(' Metal', '', self.full_genre)
        clean_genre = re.sub(r'\u200b', '', clean_genre)
        clean_genre = re.sub(chr(1089), chr(99), clean_genre)
        clean_genre = re.sub(r'(\w)\(', r'\g<1> (', clean_genre)
        clean_genre = re.sub(r'\)\/? ', r'); ', clean_genre)
        clean_genre = re.sub(r' \- ', ' ', clean_genre)

        phases = clean_genre.split(';')

        # strip and use regex to parse genre phase components
        phases = list(map(self._parse_phase, map(str.lstrip, phases)))

        # explode strings into multiple records by character
        phases = self._explode_phases_on_delimiter(phases, '/')
        phases = self._explode_phases_on_delimiter(phases, ',')

        # remove meaningless text
        phases = self._scrub_phases_of_junk(phases)

        # convert genres that appear in all phases to a single ALL record
        phases = self._collapse_recurrent_phases(phases)

        self.phases = phases = list(set(phases))
        sorted_genres = sorted(phases, key=self._phase_sort_key)
        self.clean_genre = ', '.join(map(lambda n: n.name, sorted_genres))

    @staticmethod
    def _phase_sort_key(phase: GenrePhase):
        return (Period._member_names_.index(phase.period.name), phase.name)

    @staticmethod
    def _collapse_recurrent_phases(phases: list[GenrePhase]) -> list[GenrePhase]:
        total_phases = len(set(map(lambda n: n.period, phases)))

        phase_counts = dict()
        for phase in phases:
            try:
                phase_counts[phase.name] += 1
            except KeyError:
                phase_counts[phase.name] = 1

        consistent_genres = set(g for g, c in phase_counts.items() if c == total_phases)
        collapsed_phases = list(map(GenrePhase, consistent_genres)) 
        collapsed_phases += list(filter(lambda p: p.name not in consistent_genres, phases))

        return collapsed_phases

    @staticmethod
    def _scrub_phases_of_junk(phases: list[GenrePhase]) -> list[GenrePhase]:
        def scrub(phase):
            return [GenrePhase(p, phase.period)
                    for p in phase.name.split(' ')
                    if not GenreJunk.has_value(p)]
        
        return sum(list(map(scrub, phases)), [])

    @staticmethod
    def _explode_phases_on_delimiter(phases: list[GenrePhase], delimiter: str) -> list[GenrePhase]:
        def explode(phase):
            return [GenrePhase(n.strip(), phase.period) for n in phase.name.split(delimiter)]
            
        return sum(list(map(explode, phases)), [])

    @staticmethod
    def _parse_phase(phase: str) -> GenrePhase:
        phase_match = re.compile(r'^(?P<name>.*?)(\((?P<period>[\w\/\, ]+)\))?$').match(phase)
        
        phase_record = phase_match.groupdict() if phase_match else dict(name=phase, period='all')
        try:
            period = phase_record['period']
            phase_record['period'] = Period[period.upper()] if period else Period.ALL
        except KeyError:
            phase_record['period'] = Period.ERROR

        return GenrePhase(**phase_record)
    
    def to_dict(self) -> dict:
        phases = [dict(name=p.name.lower(), period=p.period.value) for p in self.phases]
        return dict(genre=self.clean_genre.lower(), genre_phases=phases)

@dataclass
class ThemePhase:
    name: str
    period: Period


@dataclass
class Themes:
    full_theme: str
    clean_theme: str = field(init=False)
    phases: list[ThemePhase] = field(init=False)

    def __post_init__(self):
        clean_theme = re.sub(r'\)[\/\b\w]', '), ', self.full_theme)
        clean_theme = re.sub(r'\(earlier\)', '(early)', clean_theme)
        clean_theme = re.sub(r'\(early, later\)', '(early/later)', clean_theme)
        clean_theme = re.sub(r'\(early\), \b', '(early); ', clean_theme)
        clean_theme = re.sub(r'\(later\), \b', '(later); ', clean_theme)
        clean_theme = re.sub(r'\);$', ')', clean_theme)
        clean_theme = re.sub(r'\(deb.\)', '', clean_theme)

        clean_theme = re.sub(r'themes from ', '', clean_theme)
        clean_theme = re.sub(r' themes', '', clean_theme)
        clean_theme = re.sub(r'based on ', '', clean_theme)
        clean_theme = re.sub(r' \(thematic\)', '', clean_theme)
        
        self.clean_theme = clean_theme

        phases = clean_theme.split(';')
        phases = list(map(self._parse_phase, map(str.lstrip, phases)))
        
        phases = self._explode_phases_on_delimiter(phases, '/')
        phases = self._explode_phases_on_delimiter(phases, ',')

        self.phases = phases

    @staticmethod
    def _parse_phase(phase: str) -> GenrePhase:
        phase_match = re.compile(r'^(?P<name>.*?)(\((?P<period>[\w\/\, ]+)\))?$').match(phase)
        
        phase_record = phase_match.groupdict() if phase_match else dict(name=phase, period='all')
        try:
            period = phase_record['period']
            phase_record['period'] = Period[period.upper()] if period else Period.ALL
        except KeyError:
            phase_record['period'] = Period.ERROR

        return ThemePhase(**phase_record)

    @staticmethod
    def _explode_phases_on_delimiter(phases: list[ThemePhase], delimiter: str) -> list[ThemePhase]:
        def explode(phase):
            return [ThemePhase(n.strip(), phase.period) for n in phase.name.split(delimiter)]
            
        return sum(list(map(explode, phases)), [])
    
    def to_dict(self) -> dict:
        phases = [dict(name=p.name.lower(), period=p.period.value) for p in self.phases]
        return dict(theme=self.clean_theme.lower(), theme_phases=phases)


@dataclass
class BandLink:
    name: str = field(init=False)
    link: str = field(init=False)

    def __init__(self, html: str):
        html_anchor = lxml.html.fragment_fromstring(html)
        self.name = html_anchor.text
        self.link = html_anchor.attrib['href']


@dataclass(frozen=True)
class BandMember:
    alias: str
    role: str
    profile: str = field(hash=True)


@dataclass(frozen=True)
class BandDescription:
    country_of_origin: str = field(kw_only=True)
    location: str = field(kw_only=True)
    status: str = field(kw_only=True)
    formed_in: str = field(kw_only=True)
    genre: str = field(kw_only=True)
    themes: str = field(kw_only=True, default=None)
    lyrical_themes: str = field(kw_only=True, default=None)
    years_active: str = field(kw_only=True)
    last_label: str = field(kw_only=True, default=None)
    current_label: str = field(kw_only=True, default=None)


@dataclass
class BandProfile:
    url: str
    html: InitVar[bytes]
    
    name: str = field(init=False)
    metallum_id: str = field(init=False)
    lineup: dict[str, list[BandMember]] = field(init=False)
    description: BandDescription = field(init=False)
    genres: Genres = field(init=False)
    themes: Themes = field(init=False)

    def __post_init__(self, profile_html: bytes):
        self.metallum_id = int(self.url.split('/')[-1])

        try:
            profile_document = lxml.html.document_fromstring(profile_html)

            profile_band_name_xpath = '//h1[@class="band_name"]/a/text()'
            band_name: list = profile_document.xpath(profile_band_name_xpath)
            if len(band_name) == 0:
                profile_band_name_xpath = '//h1[@class="band_name noCaps"]/a/text()'
                band_name: list = profile_document.xpath(profile_band_name_xpath)

            self.name = band_name.pop()
        except IndexError:
            raise Exception(f'unable to parse band name from {self.url}')

        lineup = self._parse_lineup(profile_document)
        if len(lineup) == 0:
            lineup = self._parse_lineup(profile_document, all_members=False)
        
        self.lineup = lineup

        desc_titles = profile_document.xpath('//div[@id="band_stats"]/dl/dt//text()')
        desc_detail_xpath = '//div[@id="band_stats"]/dl/dt/following-sibling::dd//text()'
        desc_detail = profile_document.xpath(desc_detail_xpath)
        
        self.description = self._parse_description(desc_titles, desc_detail)
        if self.description.themes:
            self.themes = Themes(self.description.themes)
        elif self.description.lyrical_themes:
            self.themes = Themes(self.description.lyrical_themes)
        else:
            self.themes = Themes('Unknown')

        self.genres = Genres(self.description.genre)

    @staticmethod
    def _parse_lineup(profile_document, all_members=True) -> dict[str, list[BandMember]]:
        member_selection = 'band_tab_members_all' if all_members else 'band_tab_members_current'
        lineup_tablerows_xpath = (f'//div[@id="{member_selection}"]'
                                  f'//table[contains(@class, "lineupTable")]'
                                  f'//tr[@class="lineupHeaders" or @class="lineupRow"]')
        
        lineup_tablerows = profile_document.xpath(lineup_tablerows_xpath)

        lineup = dict()
        current_section = None if all_members else 'Current'

        for tablerow in lineup_tablerows:
            
            if tablerow.attrib['class'] == 'lineupHeaders':
                current_section = tablerow.xpath('td/text()').pop().strip().lower()
            
            elif tablerow.attrib['class'] == 'lineupRow':
                member_profile_anchor = tablerow.xpath('td[1]/a').pop()
                member_alias = member_profile_anchor.text.strip()
                member_profile = member_profile_anchor.attrib['href']

                member_role = tablerow.xpath('td[2]/text()').pop() \
                                      .strip().replace('\xa0', ' ')

                member = BandMember(member_alias, member_role, member_profile)

                try:
                    lineup[current_section].append(member)
                except KeyError:
                    lineup[current_section] = [member]
            
            else:
                raise InvalidAttributeError
            
        return lineup

    @staticmethod
    def _parse_description(description_titles, description_details) -> BandDescription:
        description = {str(dt).lower(): str(dd).strip() 
                       for dt, dd in zip(description_titles, description_details)}
        
        # scrub non alpha and whitespace
        description = {re.sub(r'[^\w\s]+', '', dt): None if dd == 'N/A' else dd 
                       for dt, dd in description.items()}
        
        # underscores
        description = {re.sub(r'\s+', '_', dt): dd
                       for dt, dd in description.items()}

        return BandDescription(**description)
    
    def to_dict(self):
        dictionary = asdict(self)
        dictionary['genres'] = self.genres.to_dict()
        dictionary['themes'] = self.themes.to_dict()
        return dictionary
    