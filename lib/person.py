
from datetime import date

class Person:
    def __init__(self, record):
        self.id = record.xref_id
        self.fname = record.name.format()

        if "'" in self.fname:
            self.gname = self.fname.split("'")[1]
            self.fname = self.fname.replace("'", "")
        if "\"" in self.fname:
            self.gname = self.fname.split("\"")[1]
        else:
            self.gname = record.name.first

        if self.gname == "?":
            self.gname = ""

        mname = ""
        names = record.sub_tags("NAME")
        for name in names:
            mname = name.value[1] if name.type == "married" else ""

        self.sname = record.name.surname
        if not self.sname and mname:
            self.sname = "(" + mname + ")"

        if self.gname and self.sname:
            self.name = self.gname + " " + self.sname
        else:
            self.name = self.gname

        self.gender = None
        if record.sex == "M":
            self.gender = "male"
        elif record.sex == "F":
            self.gender = "female"

        self.bdate = ""
        self.birth = ["", "", ""]
        birth_rec = record.sub_tag("BIRT")
        date_val = birth_rec.sub_tag_value("DATE") if birth_rec else None
        if date_val and date_val.kw.get("date", None):
            year, month, day = date_val.kw["date"].as_tuple
            if year != 9999 and month != 99 and day != 99:
                self.bdate = date(year, month, day)
            year = year if year != 9999 else ""
            month = month if month != 99 else ""
            day = day if day != 99 else ""
            self.birth = [year, month, day]

        place_val = birth_rec.sub_tag_value("PLAC") if birth_rec else None
        self.bplace = place_val.split(",")[0] if place_val else ""

        self.ddate = ""
        self.death = ["", "", ""]
        death_rec = record.sub_tag("DEAT")
        date_val = death_rec.sub_tag_value("DATE") if death_rec else None
        if date_val and date_val.kw.get("date", None):
            year, month, day = date_val.kw["date"].as_tuple
            if year != 9999 and month != 99 and day != 99:
                self.ddate = date(year, month, day)
            year = year if year != 9999 else ""
            month = month if month != 99 else ""
            day = day if day != 99 else ""
            self.death = [year, month, day]

        place_val = death_rec.sub_tag_value("PLAC") if death_rec else None
        self.dplace = place_val.split(",")[0] if place_val else ""

        self.mother_id = record.mother.xref_id if record.mother else None
        self.father_id = record.father.xref_id if record.father else None

        parents_rec = record.sub_tag("FAMC")
        self.parents_id = parents_rec.xref_id if parents_rec else None

        family_recs = record.sub_tags("FAMS")
        self.family_ids = []
        for rec in family_recs:
            self.family_ids.append(rec.xref_id)

        img_rec = record.sub_tag("OBJE")
        self.img_id = img_rec.xref_id if img_rec else None
