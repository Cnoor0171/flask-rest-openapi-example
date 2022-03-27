from dataclasses import dataclass


@dataclass
class Site:
    id: str
    name: str


SITES = [
    Site(id="site-1", name="Site 1"),
    Site(id="site-2", name="Site 2"),
    Site(id="site-3", name="Site 3"),
]


def get_all_sites() -> list[Site]:
    return SITES


def get_site_by_id(id: str) -> Site | None:
    for site in SITES:
        if id == site.id:
            return site
    return None
