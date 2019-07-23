
from datetime import date
from babel.dates import format_date
from dateutil.relativedelta import relativedelta

#from datetime import timedelta
#from babel.dates import format_timedelta

import gettext
_ = gettext.gettext

def name_list(names):
    count = len(names)
    text = names[0]

    if count == 1:
        return text
    if count == 2:
        return text + " " + _("and") + " " + names[1]
    for i in range(1, count - 1):
        text += ", " + names[i]

    return text + " " + _("and") + " " + names[count - 1]

def born_date_place(gender, date_type):
    return {
        None     : {
            "date"  : _("%(name)s was born on %(date)s in %(place)s."),
            "year"  : _("%(name)s was born in %(date)s in %(place)s."),
        },
        "male"   : {
            "date"  : _("He was born on %(date)s in %(place)s."),
            "year"  : _("He was born in %(date)s in %(place)s."),
        },
        "female" : {
            "date"  : _("She was born on %(date)s in %(place)s."),
            "year"  : _("She was born in %(date)s in %(place)s."),
        }
    }[gender][date_type]

def born_date(gender, date_type):
    return {
        None     : {
            "date"  : _("%(name)s was born on %(date)s."),
            "year"  : _("%(name)s was born in %(date)s."),
        },
        "male"   : {
            "date"  : _("He was born on %(date)s."),
            "year"  : _("He was born in %(date)s."),
        },
        "female" : {
            "date"  : _("She was born on %(date)s."),
            "year"  : _("She was born in %(date)s."),
        }
    }[gender][date_type]

def death_date_age_place(date_type):
    return {
        "date"  : _("%(name)s died on %(date)s at the age of %(age)s in %(place)s."),
        "year"  : _("%(name)s died in %(date)s at the age of %(age)s in %(place)s."),
    }[date_type]

def death_date_place(date_type):
    return {
        "date"  : _("%(name)s died on %(date)s in %(place)s."),
        "year"  : _("%(name)s died in %(date)s in %(place)s."),
    }[date_type]

def death_date_age(date_type):
    return {
        "date"  : _("%(name)s died on %(date)s at the age of %(age)s ."),
        "year"  : _("%(name)s died in %(date)s at the age of %(age)s ."),
    }[date_type]

def death_date(date_type):
    return {
        "date"  : _("%(name)s died on %(date)s."),
        "year"  : _("%(name)s died in %(date)s."),
    }[date_type]

def parents_child_of(gender):
    return {
        "male"   : _("%(name)s is the son of %(parents)s."),
        "female" : _("%(name)s is the daughter of %(parents)s."),
    }[gender]

def parents_father_mother(gender):
    return {
        "male"   : _("His parents are %(father)s and %(mother)s."),
        "female" : _("Her parents are %(father)s and %(mother)s."),
    }[gender]

def name_sibling(gender, gender_sibling):
    return {
        "male" : {
            "male"   : _("The name of his brother is %(siblings)s."),
            "female" : _("The name of his sister is %(siblings)s."),
        },
        "female" : {
            "male"   : _("The name of her brother is %(siblings)s."),
            "female" : _("The name of her sister is %(siblings)s."),
        }
    }[gender][gender_sibling]

def name_siblings(gender):
    return {
        "male"   : _("His siblings are %(siblings)s."),
        "female" : _("Her siblings are %(siblings)s."),
    }[gender]

def name_partner(married):
    return {
        True  : _("%(name)s married %(partner)s."),
        False : _("%(name)s is the partner of %(partner)s.")
    }[married]

def marriage_partner_date_place():
    return _("%(name)s married %(partner)s on %(date)s in %(place)s.")

def marriage_names_date_place():
    return _("%(names)s married on %(date)s in %(place)s.")

def marriage_names():
    return _("%(names)s are married.")

def person_age():
    return _("%(name)s was %(age)s\xa0years old.")

def person_partner_age():
    return _("%(name)s was %(age)s\xa0years old and %(partner)s %(partner_age)s\xa0years.")

def name_children():
    return _("%(name_and_partner)s have %(count)s\xa0children together. They are called %(children)s.")

def name_child(gender):
    return {
        None     : _("%(name_and_partner)s have a child called %(children)s."),
        "male"   : _("%(name_and_partner)s have a son. He is called %(children)s."),
        "female" : _("%(name_and_partner)s have a daughter. She is called %(children)s."),
    }[gender]

def event_date(event_date, date_items, lang):
    date_text = ""
    date_type = None
    if event_date:
        if lang == "de":
            date_text = format_date(event_date, "d.\xa0MMMM yyyy", locale='de_DE')
        else:
            date_text = format_date(event_date, "MMMM\xa0d, yyyy", locale='en')
        date_type = "date"
    elif date_items[0]:
        date_text = date_items[0]
        date_type = "year"

    return date_text, date_type

class Narrator:
    def __init__(self, persons, families, lang):
        self.__persons = persons
        self.__families = families
        self.__lang = lang

        global _
        if lang == "de":
            de = gettext.translation('messages', localedir='locales', languages=['de'])
            de.install()
            _ = de.gettext

    def get_list_text(self, names):
        return name_list(names)

    def get_born_text(self, person_id, **options):
        person = self.__persons[person_id]

        person_name = person.fname
        if options.get("docref") and person_id in options.get("docref"):
            person_name = person.fname.replace(
                person.gname, ":doc:`" + person.gname + "<" + person_id + ">`"
            )

        text = ""
        bdate, bdate_type = event_date(person.bdate, person.birth, self.__lang)
        value_map = {
            "name"  : person_name,
            "date"  : bdate,
            "place" : person.bplace,
        }
        if bdate:
            if person.bplace and not options.get("short"):
                if options.get("use_name"):
                    text = born_date_place(None, bdate_type) % value_map
                else:
                    text = born_date_place(person.gender, bdate_type) % value_map
            else:
                if options.get("use_name"):
                    text = born_date(None, bdate_type) % value_map
                else:
                    text = born_date(person.gender, bdate_type) % value_map

        return text

    def get_died_text(self, person_id, **options):
        person = self.__persons[person_id]

        text = ""
        bdate, bdate_type = event_date(person.bdate, person.birth, self.__lang)
        ddate, ddate_type = event_date(person.ddate, person.death, self.__lang)

        bdate_date = person.bdate
        ddate_date = person.ddate
        if bdate_type == "year":
            bdate_date = date(bdate, 12, 31)
        if ddate_type == "year":
            ddate_date = date(ddate, 1, 1)
        age = relativedelta(ddate_date, bdate_date).years if bdate_date and ddate_date else None

        value_map = {
            "name"  : person.gname,
            "date"  : ddate,
            "place" : person.dplace,
            "age"   : age,
        }
        if ddate:
            if person.dplace and age and not options.get("short"):
                text = death_date_age_place(ddate_type) % value_map
            elif person.dplace and not options.get("short"):
                text = death_date_place(ddate_type) % value_map
            elif age and not options.get("short"):
                text = death_date_age(ddate_type) % value_map
            else:
                text = death_date(ddate_type) % value_map

        return text

    def get_parents_text(self, person_id, **options):
        person = self.__persons[person_id]
        father_name = None
        mother_name = None

        if person.parents_id:
            parents = self.__families[person.parents_id]

            if parents and parents.husb_id and parents.wife_id:
                father = self.__persons[parents.husb_id]
                father_name = father.name
                if options.get("docref") and father.id in options.get("docref"):
                    father_name = father_name.replace(
                        father.gname, ":doc:`" + father.gname + "<" + father.id + ">`"
                    )
                mother = self.__persons[parents.wife_id]
                mother_name = mother.name
                if options.get("docref") and mother.id in options.get("docref"):
                    mother_name = mother_name.replace(
                        mother.gname, ":doc:`" + mother.gname + "<" + mother.id + ">`"
                    )
                parents_names = name_list([father_name, mother_name])
                if options.get("docref") and parents.id in options.get("docref"):
                    parents_names = ":doc:`" + parents_names + "<" + parents.id + ">`"

        value_map = {
            "name"    : person.fname,
            "parents" : parents_names,
            "father"  : father_name,
            "mother"  : mother_name,
        }
        if options.get("child_of"):
            text = parents_child_of(person.gender) % value_map
        else:
            text = parents_father_mother(person.gender) % value_map
        return text;

    def get_siblings_text(self, person_id):
        person = self.__persons[person_id]

        siblings = []
        if person.parents_id:
            parents = self.__families[person.parents_id]
            if parents:
                for child_id in parents.child_ids:
                    if child_id != person_id:
                        siblings.append(self.__persons[child_id])

        if len(siblings) == 0:
            return ""

        value_map = {
            "siblings" : name_list(list(map(lambda s: s.gname, siblings))),
        }
        if len(siblings) == 1:
            gender_sibling = siblings[0].gender
            text = name_sibling(person.gender, gender_sibling) % value_map
        else:
            text = name_siblings(person.gender) % value_map

        return text

    def get_partner_text(self, person_id, **options):
        person = self.__persons[person_id]

        text = ""
        for family_id in person.family_ids:
            family = self.__families[family_id]
            if family.husb_id == person_id:
                partner = self.__persons[family.wife_id]
            else:
                partner = self.__persons[family.husb_id]

            mdate, mdate_type = event_date(family.mdate, family.marriage, self.__lang)
            value_map = {
                "name"    : person.name,
                "partner" : partner.name,
                "date"    : mdate,
                "place"   : family.mplace,
            }
            if mdate:
                text += marriage_partner_date_place() % value_map
            else:
                text += name_partner(family.is_married) % value_map

            text += " " + self.get_family_children_text(
                family_id, no_gender=True, docref=options.get("docref")
            )

        return text

    def get_family_partner_text(self, family_id):
        family = self.__families[family_id]
        husb = self.__persons[family.husb_id]
        wife = self.__persons[family.wife_id]

        text = ""
        mdate, mdate_type = event_date(family.mdate, family.marriage, self.__lang)
        value_map = {
            "names" : name_list([husb.name, wife.name]),
            "date"  : mdate,
            "place" : family.mplace,
        }
        if mdate:
            text = marriage_names_date_place() % value_map
        elif family.is_married:
            text += marriage_names() % value_map

        value_map = {
            "name"        : husb.gname,
            "partner"     : wife.gname,
            "age"         : relativedelta(family.mdate, husb.bdate).years,
            "partner_age" : relativedelta(family.mdate, wife.bdate).years,
        }
        if mdate_type == "date":
            text += " " + person_partner_age() % value_map

        return text

    def get_family_children_text(self, family_id, **options):
        family = self.__families[family_id]
        children = []
        for child_id in family.child_ids:
            child = self.__persons[child_id]
            child_name = child.gname
            if options.get("docref") and child_id in options.get("docref"):
                child_name = ":doc:`" + child_name + "<" + child_id + ">`"
            children.append(child_name)

        if len(children) == 0:
            return ""

        husb = self.__persons[family.husb_id]
        wife = self.__persons[family.wife_id]
        name_and_partner = name_list([husb.gname, wife.gname])
        if options.get("docref") and family_id in options.get("docref"):
            name_and_partner = ":doc:`" + name_and_partner + "<" + family_id + ">`"

        value_map = {
            "name_and_partner" : name_and_partner,
            "count"    : len(children),
            "children" : name_list(children),
        }
        if (len(children) == 1):
            text = name_child(None if options.get("no_gender") else child.gender) % value_map
        else:
            text = name_children() % value_map

        return text
