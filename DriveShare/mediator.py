class UIMediator:

    def __init__(self):
        self.components = {}

    def register(self, name, component):
        self.components[name] = component

    def notify(self, sender, event):

        if event == "logout":
            if "login_screen" in self.components:
                self.components["login_screen"]()

        elif event == "refresh":
            pass