class GdcBioEdge():
    DISPLAY_STATES = set(['standard', 'fringe', 'hidden'])
    SELECTED_STATES = set(['selected', 'not-selected'])
    def __init__(self, source: str, target: str) -> None:
        self.source = source
        self.target = target
        self.id = (source, target)
        # display properties
        self.display_classes = set()

    def _set_classes(self, classes: list[str]) -> None:
        # Deprecated
        self.display_classes = classes

    def set_standard(self) -> None:
        classes = self.display_classes - GdcBioEdge.DISPLAY_STATES
        classes.add('standard')
        self._set_classes(classes)

    def set_fringe(self) -> None:
        classes = self.display_classes - GdcBioEdge.DISPLAY_STATES
        classes.add('fringe')
        self._set_classes(classes)

    def set_hidden(self) -> None:
        classes = self.display_classes - GdcBioEdge.DISPLAY_STATES
        classes.add('hidden')
        self._set_classes(classes)

    def set_selected(self) -> None:
        classes = self.display_classes - GdcBioEdge.SELECTED_STATES
        classes.add('selected')
        self._set_classes(classes)

    def set_not_selected(self) -> None:
        classes = self.display_classes - GdcBioEdge.SELECTED_STATES
        classes.add('not-selected')
        self._set_classes(classes)

    def cyto_repr(self):
        cyto_dict = {
            'data': {
                'source': self.source,
                'target': self.target
            },
            'classes': ' '.join(self.display_classes)
        }
        return cyto_dict
