
class Media:
    def __init__(self, record):
        self.file = record.sub_tag_value("FILE")
        self.title = record.sub_tag_value("TITL")
