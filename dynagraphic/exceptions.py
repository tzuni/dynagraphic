class GdcBioInvalidDataKeyException(Exception):
    def __init__(self, key: str) -> None:
        self.message = f'Data key {key} is not allowed to occur in the data dictionary'
