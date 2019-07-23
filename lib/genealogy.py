
from os import path, makedirs, remove
from shutil import copyfile
from datetime import date
from babel.dates import format_date

from pylatex import Document, Command
from pylatex.base_classes import Environment
from pylatex.package import Package
from pylatex.utils import NoEscape

from pdf2image import convert_from_path

tex_lib = NoEscape(r"""
\makeatletter
\def\yshiftdim#1{
  \newdimen\pnorth
  \newdimen\psouth
  \pgfextracty{\pnorth}{\pgfpointanchor{p@#1}{north}}
  \pgfextracty{\psouth}{\pgfpointanchor{p@#1}{south}}
  \dimdef\height{\pnorth-\psouth}
  \ifdim\yshift=0pt
    \dimdef\yshift{\height}
  \else
    \dimdef\yshift{(\yshift-\height)/4}
  \fi
}
\def\labelyshift{
  \dimdef\yshift{0pt}
  \letcs\parlist{gtr@fam@\gtr@currentfamily @par}
  \forlistloop{\yshiftdim}{\parlist}
}
\tikzset{
  labelyshift/.code={\labelyshift\pgfkeys{/tikz/yshift=-\yshift}}
}
\makeatother
""")

person_tree_down_ = NoEscape(r"""
  template=database pole,
  database format=short marriage below,
  node size=24mm,
  level size=25mm,
  parent distance=2mm,
  child distance=3mm,
  date format=mon d yyyy,
  pref code={#1},
  box={
    top=2.5mm,left=1mm,right=1mm,bottom=2mm,
    before upper=\parskip4pt,
    if image defined={
      add to width=18mm,right=20mm,
      segmentation style={solid,shorten >=20mm,shorten <=1mm},
      underlay={\begin{tcbclipinterior}
        \path[fill overzoom DBimage]
        ([xshift=-19mm]interior.south east) rectangle (interior.north east);
      \end{tcbclipinterior}},
    }{segmentation style={solid,shorten >=1mm,shorten <=1mm}},
  },
""")

person_tree_down_ = NoEscape(r"""
  template=database traditional,
  edges={perpendicular},
  node size=20mm,
  level size=40mm,
  pref code={#1},
  date format=mon d yyyy,
  box={
    valign=center,
    before upper=\parskip2pt,
    if image defined={
      top=26mm,
      underlay={\begin{tcbclipinterior}\path[fill overzoom DBimage]
        ([yshift=-25mm,xshift=2mm]interior.north west) rectangle ([yshift=-1mm,xshift=-2mm]interior.north east);
      \end{tcbclipinterior}},
    }{add to height=-25mm},
  },
""")

def person_tree_down(lang):
    tree_options = NoEscape(r"""
  template=database pole,
  database format=short no marriage,
  node size=20mm,
  level size=40mm,
  parent distance=3mm,
  child distance=2mm,
  pref code={#1},
  event format=prefix date,
  image shift/.style={tikz={yshift=-25mm}},
  box={
    valign=center,
    before upper=\parskip2pt,
    if image defined={
      top=26mm,
      underlay={\begin{tcbclipinterior}\path[fill overzoom DBimage]
        ([yshift=-26mm,xshift=0mm]interior.north west) rectangle ([yshift=-0mm,xshift=-0mm]interior.north east);
      \end{tcbclipinterior}},
    }{add to height=-25mm},
  },
""")
    if lang == "de":
        tree_options += NoEscape("date format=d.m.yyyy,")
    else:
        tree_options += NoEscape("date format=mon d yyyy")
    return tree_options

def person_tree_right(lang):
    tree_options = NoEscape(r"""
  template=database sideways,
  database format=short no marriage,
  timeflow=right,
  node size=15mm,
  level size=40mm,
  parent distance=3mm,
  child distance=2mm,
  place text={in~}{},
  list separators hang,
  event format=prefix date,
  image shift/.style={},
  box={
    top=3mm,left=1.5mm,right=1.5mm,bottom=2mm,
    before upper=\parskip4pt,
    if image defined={
      height=26mm,right=20mm,
      segmentation style={solid,shorten >=20mm,shorten <=1mm},
      underlay={\begin{tcbclipinterior}
        \path[preaction={fill=tcbcolframe!10!tcbcolback},fill overzoom DBimage]
        ([xshift=-19mm]interior.south east) rectangle (interior.north east);
      \end{tcbclipinterior}},%
    }{segmentation style={solid,shorten >=1mm,shorten <=1mm}},
  },
""")
    if lang == "de":
        tree_options += NoEscape("date format=d.m.yyyy,")
    else:
        tree_options += NoEscape("date format=mon d yyyy,")
    return tree_options

def family_tree(lang):
    tree_options = NoEscape(r"""
  template=database sideways,
  database format=short no marriage,
  timeflow=right,
  node size=15mm,
  level size=46mm,
  further distance=8mm,
  parent distance=8mm,
  child distance=3mm,
  level distance=10mm,
  place text={in~}{},
  label options={node font=\footnotesize,anchor=east,xshift=-8mm},%,labelyshift},
  label database options={list separators={}{}{}{}},
  list separators hang,
  box={
    top=3mm,left=1.5mm,right=1.5mm,bottom=2mm,
    before upper=\parskip4pt,
    if image defined={
      height=26mm,right=20mm,
      segmentation style={solid,shorten >=20mm,shorten <=1mm},
      underlay={\begin{tcbclipinterior}
        \path[preaction={fill=tcbcolframe!10!tcbcolback},fill overzoom DBimage]
        ([xshift=-19mm]interior.south east) rectangle (interior.north east);
      \end{tcbclipinterior}},%
    }{segmentation style={solid,shorten >=1mm,shorten <=1mm}},
  },
""")
    if lang == "de":
        tree_options += NoEscape("label database options={date format=d.m.yyyy},")
    else:
        tree_options += NoEscape("label database options={date format=mon d yyyy},")
    return tree_options

def event_date(event_date, date_items):
    if not event_date and date_items[0]:
        event_date = date_items[0]

    return event_date

def tree_node(tree, node, person, family=None, media=None, media_dir=None, node_opt=""):
    if not person:
        return

    images_dir = path.abspath("_build/images")
    if media and not path.exists(images_dir):
        makedirs(images_dir)

    image = ""
    if media and person.img_id:
        img_file = media[person.img_id].file
        image = path.join(images_dir, img_file)
        copyfile(path.join(media_dir, img_file), image)

    bdate = event_date(person.bdate, person.birth)
    ddate = event_date(person.ddate, person.death)

    tree +=     [" %s[id=%s,%s]{"                % (node, person.id, node_opt)]
    tree +=     ["  %s,"                         % person.gender]
    tree +=     ["  name={\pref{%s} \surn{%s}}," % (person.gname, person.sname)]
    tree +=     ["  birth={%s}{%s},"             % (bdate, person.bplace)]
    tree +=     ["  death={%s}{%s},"             % (ddate, person.dplace)]
    if image:
        tree += ["  image={%s},"                 % image]
    if family:
        tree += ["  marriage={%s}{%s},"          % (family.mdate, family.mplace)]
    tree +=     [" }"]

def family_label(family):
    if not family:
        return ""

    mdate = event_date(family.mdate, family.marriage)
    return "family database={marriage={%s}{%s}}" % (mdate, family.mplace)

def tree_doc(tree, tree_opt, doc_name, save_dir, lang):
    doc = Document(
        document_options='border=10pt',
        documentclass='standalone',
        textcomp=False,
        page_numbers=False
    )

    if lang == "de":
        doc.preamble.append(Command("gtrset", arguments=NoEscape("language=german-german")))

    doc.append(tex_lib)

    with doc.create(GenealogyPicture(options=tree_opt)):
        doc.append(NoEscape("\n".join(tree)))

    doc_dir = path.join("_build", "tex")
    doc_path = path.join(doc_dir, doc_name)
    if not path.exists(doc_dir):
        makedirs(doc_dir)
    doc.generate_pdf(doc_path, clean_tex=False)

    img = convert_from_path(doc_path + ".pdf", dpi=150)
    img[0].save(path.join(save_dir, doc_name + ".png"), "PNG")

class GenealogyPicture(Environment):
    _latex_name = "genealogypicture"
    packages = [Package("genealogytree", options="all")]

class Genealogy:
    def __init__(self, persons, families, media, lang):
        self.__persons = persons
        self.__families = families
        self.__media = media
        self.__media_dir = path.join("gedcom", "media")
        self.__lang = lang

    def get_person_tree(self, person_id, save_dir):
        person = self.__persons[person_id]

        parents = self.__families[person.parents_id] if person.parents_id else None
        father = self.__persons[person.father_id] if person.father_id else None
        mother = self.__persons[person.mother_id] if person.mother_id else None

        db =  ["sandclock{"]
        tree_node(db, "p", father, node_opt="image shift")
        tree_node(db, "p", mother, node_opt="image shift")

        family = None
        partner = None
        for family_id in person.family_ids:
            family = self.__families[family_id]
            if family.husb_id == person_id:
                partner = self.__persons[family.wife_id]
            else:
                partner = self.__persons[family.husb_id]

        family_db = ["child{"]
        tree_node(family_db, "g", person, None, self.__media, self.__media_dir)
        tree_node(family_db, "p", partner, family, self.__media, self.__media_dir)
        if family:
            for child_id in family.child_ids:
                tree_node(family_db, "c", self.__persons[child_id])
        family_db += ["}"]

        if not parents:
            db += family_db
        else:
            for child_id in parents.child_ids:
                if child_id != person_id:
                    sibling = self.__persons[child_id]
                    tree_node(db, "c", sibling)
                else:
                    db += family_db

        db += ["}"]

        doc_name = person.id + "tree"
        nodes = len(parents.child_ids) if parents else 0
        nodes += len(family.child_ids) if family else 0
        if  (nodes > 10):
            tree_doc(db, person_tree_right(self.__lang), doc_name, save_dir, self.__lang)
        else:
            tree_doc(db, person_tree_down(self.__lang), doc_name, save_dir, self.__lang)

    def get_family_tree(self, family_id, save_dir):
        family = self.__families[family_id]

        person = self.__persons[family.husb_id]
        parents = self.__families[person.parents_id] if person.parents_id else None
        father = self.__persons[person.father_id] if person.father_id else None
        mother = self.__persons[person.mother_id] if person.mother_id else None

        partner = self.__persons[family.wife_id]
        parents_p = self.__families[partner.parents_id] if partner.parents_id else None
        father_p = self.__persons[partner.father_id] if partner.father_id else None
        mother_p = self.__persons[partner.mother_id] if partner.mother_id else None

        db = ["parent[" + family_label(family) + "]{"]

        if len(family.child_ids) > 0:
            for child_id in family.child_ids:
                tree_node(db, "g", self.__persons[child_id], None, self.__media, self.__media_dir)
        else:
            db += ["g[phantom=0pt,box={width=0pt}]{}"]

        db += ["parent[" + family_label(parents) + ",pivot shift=8mm]{"]

        node_opt = (
            "tikz={yshift=-4mm}" if not event_date(parents.mdate, parents.marriage) else ""
        )
        tree_node(db, "g", person, None, self.__media, self.__media_dir)
        tree_node(db, "p", father, None, self.__media, self.__media_dir, node_opt)
        tree_node(db, "p", mother, None, self.__media, self.__media_dir)

        db += ["}"]
        db += ["parent[" + family_label(parents_p) + ",pivot shift=-8mm]{"]

        node_opt = (
            "tikz={yshift=4mm}" if not event_date(parents_p.mdate, parents_p.marriage) else ""
        )
        tree_node(db, "g", partner, None, self.__media, self.__media_dir)
        tree_node(db, "p", father_p, None, self.__media, self.__media_dir)
        tree_node(db, "p", mother_p, None, self.__media, self.__media_dir, node_opt)

        db += ["}"]
        db += ["}"]

        doc_name = family_id + "tree"
        tree_doc(db, family_tree(self.__lang), doc_name, save_dir, self.__lang)
