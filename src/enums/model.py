from shared.model import Model


class Profile(Model):
    def __init__(self):
        super().__init__()
        self.table = "profiles"
