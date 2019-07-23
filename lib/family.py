
from datetime import date

class Family:
    def __init__(self, record):
        self.id = record.xref_id

        husb_rec = record.sub_tag("HUSB")
        self.husb_id = husb_rec.xref_id if husb_rec else None

        wife_rec = record.sub_tag("WIFE")
        self.wife_id = wife_rec.xref_id if wife_rec else None

        self.is_married = False
        self.mdate = ""
        self.marriage = ["", "", ""]
        marr_rec = record.sub_tag("MARR")
        date_val = marr_rec.sub_tag_value("DATE") if marr_rec else None
        if date_val:
            self.is_married=True
        if date_val and date_val.kw.get("date", None):
            year, month, day = date_val.kw["date"].as_tuple
            if year != 9999 and month != 99 and day != 99:
                self.mdate = date(year, month, day)
            year = year if year != 9999 else ""
            month = month if month != 99 else ""
            day = day if day != 99 else ""
            self.marriage = [year, month, day]

        place_val = marr_rec.sub_tag_value("PLAC") if marr_rec else None
        self.mplace = place_val.split(",")[0] if place_val else ""

        self.child_ids = []
        for child_rec in record.sub_tags("CHIL"):
            self.child_ids.append(child_rec.xref_id)
