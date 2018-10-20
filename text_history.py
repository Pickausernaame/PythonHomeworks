class TextHistory:
    def __init__(self, text=""):
        self._text = text
        self._version = 0
        self.actions = []

    @property
    def text(self):
        return self._text

    @property
    def version(self):
        return self._version

    def index_validation(self, pos):
        if pos not in range(0, len(self.text)) or pos < 0:
            raise ValueError()

    def version_validation(self, before, after):
        if before < 0 or after < 0 or before >= after:
            raise ValueError()

    def insert(self, text, pos=None):
        self.action(InsertAction(pos, text, from_version=self.version, to_version=self.version+1))
        return self.version

    def replace(self, text, pos=None):
        self.action(ReplaceAction(pos, text, from_version=self.version, to_version=self.version + 1))
        return self.version

    def delete(self, pos, length):
        self.action(DeleteAction(pos, self.text, from_version=self.version, to_version=self.version + 1, length=length))
        return self.version

    def action(self, action):
        self._text = action.apply(self.text)
        if action.pos is not None:
            self.index_validation(action.pos)
        self.version_validation(action.from_version, action.to_version)
        self.actions.append(action)
        self._version = action.to_version
        return action.to_version

    def get_actions(self, from_version=None, to_version=None):
        if to_version is None:
            to_version = self.version
        if from_version is None:
            from_version = self.version
        if from_version not in range(0, self.version + 1) or to_version not in range(0, self.version + 1):
            raise ValueError()
        if from_version > to_version:
            raise ValueError()
        return self.actions[from_version:to_version]


class Action:
    def __init__(self, pos, text, from_version, to_version, length=None):
        self.pos = pos
        self.text = text
        self.length = length
        self.from_version = from_version
        self.to_version = to_version


class InsertAction(Action):
    def apply(self, text):
        stored_value = text
        input_value = self.text
        if self.pos is None:
            self.pos = len(input_value)-1
            mdf_text = stored_value + input_value
        else:
            if self.pos == 0:
                mdf_text = input_value + stored_value
            else:
                mdf_text = stored_value[:self.pos] + input_value + stored_value[self.pos:]
        return mdf_text


class ReplaceAction(Action):
    def apply(self, text):
        stored_value = text
        input_value = self.text
        if self.pos is None:
            insert = InsertAction(self.pos, input_value, from_version=self.from_version, to_version=self.to_version)
            mdf_text = insert.apply(stored_value)
        else:
            mdf_text = stored_value[:self.pos] + input_value + stored_value[self.pos + len(input_value):]
        return mdf_text


class DeleteAction(Action):
    def apply(self, text):
        return text[:self.pos] + text[self.pos + self.length:]

