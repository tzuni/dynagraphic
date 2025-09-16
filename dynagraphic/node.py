import dynagraphic
from dynagraphic.exceptions import GdcBioInvalidDataKeyException
from typing import List
# from dynagraphic.graph import GdcBioGraph


class GdcBioNode():
    DISPLAY_STATES = set(['standard', 'fringe', 'hidden'])
    SELECTED_STATES = set(['selected', 'not-selected'])
    def __init__(self, node_id: str, label: str, data: dict) -> None:
        if 'id' in data:
            raise GdcBioInvalidDataKeyException('id')
        if 'label' in data:
            raise GdcBioInvalidDataKeyException('label')
        
        self.id = node_id
        self.data = data
        self.data['id'] = node_id
        self.data['label'] = label
        self.graph = None
        # Display properties
        self.visible = True
        self.display_classes = set()

    # def set_graph(self, graph: type[dynagraphic.GdcBioGraph]) -> None:
    #     self.graph = graph

    def _set_classes(self, classes: List[str]) -> None:
        # Deprecated
        self.display_classes = classes

    def set_standard(self) -> None:
        classes = self.display_classes - GdcBioNode.DISPLAY_STATES
        classes.add('standard')
        self._set_classes(classes)

    def set_fringe(self) -> None:
        classes = self.display_classes - GdcBioNode.DISPLAY_STATES
        classes.add('fringe')
        self._set_classes(classes)

    def set_hidden(self) -> None:
        classes = self.display_classes - GdcBioNode.DISPLAY_STATES
        classes.add('hidden')
        self._set_classes(classes)

    def set_selected(self) -> None:
        classes = self.display_classes - GdcBioNode.SELECTED_STATES
        classes.add('selected')
        self._set_classes(classes)

    def set_not_selected(self) -> None:
        classes = self.display_classes - GdcBioNode.SELECTED_STATES
        classes.add('not-selected')
        self._set_classes(classes)

    def add_class(self, class_id: str) -> None:
        # Deprecated
        self.display_classes.add(class_id)

    def remove_class(self, class_id: str) -> None:
        # Deprecated
        self.display_classes.remove(class_id)

    def cyto_repr(self) -> None:
        cyto_dict = {
            'data': self.data,
            'classes': ' '.join(self.display_classes)
        }
        return cyto_dict

    def is_standard(self):
        return 'standard' in self.display_classes
    
    def is_visible(self):
        return 'hidden' not in self.display_classes
    
    def is_fringe(self):
        return 'fringe' in self.display_classes