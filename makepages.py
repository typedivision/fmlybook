#!/usr/bin/env python3

import os

from ged4py import GedcomReader
from lib.person import Person
from lib.family import Family
from lib.media import Media
from lib.genealogy import Genealogy
from lib.narrator import Narrator

from sphinx.config import Config

import gettext
_ = gettext.gettext

def family_page(family_id, generation, descendant_id=None):

    genealogy.get_family_tree(family_id, pages_dir)

    with open(os.path.join(pages_dir, family_id + ".rst"), "w") as text_file:
        family = families[family_id]
        husb = persons[family.husb_id]
        wife = persons[family.wife_id]

        family_name = husb.name + " & " + wife.name
        print(family_name, file=text_file)
        for i in range(len(family_name)):
            text_file.write("=")
        print("", file=text_file)

        husb_id = family.husb_id
        husb_born_text = narrator.get_born_text(
            husb_id, use_name=True, short=True, docref=[husb_id]
        )
        father_id = None
        mother_id = None
        if husb.parents_id:
            parents = families[husb.parents_id]
            if parents:
                father_id = parents.husb_id
                mother_id = parents.wife_id

        if father_id and persons[father_id].name or mother_id and persons[mother_id].name:
            husb_parents_text = narrator.get_parents_text(
                husb_id, docref=[father_id, mother_id] if generation > 0 else []
            )
        else:
            husb_parents_text = ""

        print(husb_born_text, file=text_file)
        if husb_parents_text: print(husb_parents_text, file=text_file)
        print(narrator.get_died_text(husb_id, short=True), file=text_file)
        print("", file=text_file)

        wife_id = family.wife_id
        wife_born_text = narrator.get_born_text(
            wife_id, use_name=True, short=True, docref=[wife_id]
        )
        father_id = None
        mother_id = None
        if wife.parents_id:
            parents = families[wife.parents_id]
            if parents:
                father_id = parents.husb_id
                mother_id = parents.wife_id

        if father_id and persons[father_id].name or mother_id and persons[mother_id].name:
            wife_parents_text = narrator.get_parents_text(
                wife_id, docref=[father_id, mother_id] if generation > 0 else []
            )
        else:
             wife_parents_text = ""

        print(wife_born_text, file=text_file)
        if wife_parents_text: print(wife_parents_text, file=text_file)
        print(narrator.get_died_text(wife_id, short=True), file=text_file)
        print("", file=text_file)

        family_partner_text = narrator.get_family_partner_text(family_id)
        family_children_text = narrator.get_family_children_text(family_id, docref=[descendant_id])
        print(family_partner_text, file=text_file)
        print(family_children_text, file=text_file)
        print("", file=text_file)

        image = family_id + "tree.png"
        print(".. image:: " + image, file=text_file)
        print("", file=text_file)

        children = []
        for child_id in family.child_ids:
            print(narrator.get_born_text(child_id, use_name=True), file=text_file)
            print("", file=text_file)

def person_page(person_id, generation, descendant_id=None):

    genealogy.get_person_tree(person_id, pages_dir)

    with open(os.path.join(pages_dir, person_id + ".rst"), "w") as text_file:
        person = persons[person_id]

        name = person.name
        print(name, file=text_file)
        for i in range(len(name)):
            text_file.write("=")
        print("", file=text_file)

        father_id = None
        mother_id = None
        if person.parents_id:
            parents = families[person.parents_id]
            if parents:
                father_id = parents.husb_id
                mother_id = parents.wife_id

        if father_id and persons[father_id].name or mother_id and persons[mother_id].name:
            parents_text = narrator.get_parents_text(
                person_id, child_of=True, use_name=True,
                docref=[person.parents_id] if generation > 0 else []
            )
        else:
            parents_text = person.fname + "."

        print(parents_text, file=text_file)
        print(narrator.get_born_text(person_id), file=text_file)
        print(narrator.get_siblings_text(person_id), file=text_file)
        print("", file=text_file)

        family_text = narrator.get_partner_text(
            person_id, docref=person.family_ids
        )
        print(family_text, file=text_file)
        print("", file=text_file)

        print(narrator.get_died_text(person_id), file=text_file)
        print("", file=text_file)

        image = person_id + "tree.png"
        print(".. image:: " + image, file=text_file)

def index_page(family_ids, person_ids):

    with open("index.rst", "w") as text_file:
        family = families[family_ids[0]]
        husb = persons[family.husb_id]
        wife = persons[family.wife_id]

        title = _("Familybook")
        print(title, file=text_file)
        for i in range(len(title)):
            text_file.write("=")
        print("", file=text_file)

        family_name = narrator.get_list_text([husb.sname, wife.sname])
        family_link = ":doc:`%s<pages/%s>`" % (family_name, family.id)
        print(
            _("A report on the generations of the families %s.") % family_link, file=text_file
        )
        print("", file=text_file)

        print("*" + _("Families") + "*", file=text_file)
        print("", file=text_file)
        print(".. toctree::", file=text_file)
        for family_id in family_ids:
            print("   pages/" + family_id, file=text_file)
        print("", file=text_file)

        print("*" + _("Persons") + "*", file=text_file)
        print("", file=text_file)
        print(".. toctree::", file=text_file)
        for person_id in person_ids:
            print("   pages/" + person_id, file=text_file)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

gedcom_path = os.path.abspath("gedcom/family.ged")

pages_dir = os.path.abspath("pages")
if not os.path.exists(pages_dir):
    os.makedirs(pages_dir)

config = Config.read(".")
config.add('generations', 0, 'env', None)
config.add('family_id', "", 'env', None)
config.init_values()

lang = config.language
family_id_start = config.family_id
generations = config.generations

if lang == "de":
    de = gettext.translation('messages', localedir='locales', languages=['de'])
    de.install()
    _ = de.gettext

persons = {}
families = {}
media = {}

with GedcomReader(gedcom_path) as parser:
    for record in parser.records0("INDI"):
        persons[record.xref_id] = Person(record)
    for record in parser.records0("FAM"):
        families[record.xref_id] = Family(record)
    for record in parser.records0("OBJE"):
        media[record.xref_id] = Media(record)

narrator = Narrator(persons, families, lang)
genealogy = Genealogy(persons, families, media, lang)

family_ids = []
person_ids = []

def create_pages(family_id, descendant_id, family_ids, person_ids, generation):
    family_ids += [family_id]
    family_page(family_id, generation, descendant_id)

    family = families[family_id]
    person_ids += [family.husb_id, family.wife_id]
    person_page(family.husb_id, generation, descendant_id)
    person_page(family.wife_id, generation, descendant_id)

    if generation <= 0:
        return

    husb = persons[family.husb_id]
    create_pages(husb.parents_id, husb.id, family_ids, person_ids, generation - 1)

    wife = persons[family.wife_id]
    create_pages(wife.parents_id, wife.id, family_ids, person_ids, generation - 1)

create_pages(family_id_start, None, family_ids, person_ids, generations)
index_page(family_ids, person_ids)

