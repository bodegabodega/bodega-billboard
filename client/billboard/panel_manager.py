class PanelManager:
    def __init__(self):
        self.panels = []
        self.current_panel = 0

    def add_panel(self, panel):
        self.panels.append(panel)

    def get_current_panel(self):
        return self.panels[self.current_panel]
    
    def increment_panel(self):
        self.current_panel += 1
        if self.current_panel >= len(self.panels):
            self.current_panel = 0

    def decrement_panel(self):
        self.current_panel -= 1
        if self.current_panel < 0:
            self.current_panel = len(self.panels) - 1