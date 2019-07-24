![fmlybook](fmlybook.png)

create family book websites from gedcom file including personal family trees

the static sites are build by [sphinx](http://www.sphinx-doc.org/en/master/) documentation generator

the family tree images coming from the LaTeX [genealogytree](https://github.com/T-F-S/genealogytree) package

# how to

get all the python and LaTeX stuff from docker for a simple make

```
cd fmlybook
docker run -it --rm -v $PWD:/fmlybook -w /fmlybook typedivision/fmlybook
# make
```

for all the config there is a config.py

# example

the Potter & Weasley [gedcom](gedcom/family.ged) file as family site in
[english](https://typedivision.github.io/fmlybook/en) and [german](https://typedivision.github.io/fmlybook/de)
