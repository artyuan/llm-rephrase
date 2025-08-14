from typing_extensions import TypedDict


class ModeratorParser(TypedDict):
    input: str
    output: bool


class RephraseParser(TypedDict):
    user_input: str
    professional_output: str
    casual_output: str
    polite_output: str
    social_media_output: str
