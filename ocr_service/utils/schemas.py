from enum import Enum


class OCRLanguage(str, Enum):
    SPA = "spa"
    ENG = "eng"
    SPAENG = "spa+eng"
