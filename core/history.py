class HistoryManager:
    def __init__(self, engine):
        self.engine = engine
        self.undo_stack = []
        self.redo_stack = []
        self.is_undoing = False

    def save_state(self):
        if self.is_undoing:
            return
        # Store clones of elements
        state = [el.clone() for el in self.engine.elements]
        self.undo_stack.append(state)
        self.redo_stack.clear()
        if len(self.undo_stack) > 50:
            self.undo_stack.pop(0)

    def undo(self):
        if not self.undo_stack:
            return
        
        self.is_undoing = True
        current_state = [el.clone() for el in self.engine.elements]
        self.redo_stack.append(current_state)
        
        state = self.undo_stack.pop()
        self.engine.elements = state
        self.engine.elements_changed.emit()
        self.is_undoing = False

    def redo(self):
        if not self.redo_stack:
            return
        
        self.is_undoing = True
        current_state = [el.clone() for el in self.engine.elements]
        self.undo_stack.append(current_state)
        
        state = self.redo_stack.pop()
        self.engine.elements = state
        self.engine.elements_changed.emit()
        self.is_undoing = False
