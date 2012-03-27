#!/usr/bin/env python

class Section:
    def has_item(self, item):
        return self.__dict__.has_key(item)

class ReadConfig(object):
    sections = []

    def __init__(self, cfg):
        f = open(cfg, 'rb')
        for line in filter(None, map(lambda x: x.strip(), f.readlines())):
            if line.startswith("["):
                cursec = line.split("[")[-1].split("]")[0]
                self.sections.append(cursec)
                section = Section()
                setattr(self, cursec, section)
            else:
                k,v = line.split("=")
                setattr(section, k.strip(), v.strip())

    def get_sections(self):
        return self.sections

    def has_section(self, section='DEFAULT'):
        return section.strip() in self.sections

    def get_items(self, section='DEFAULT'):
        return self.__dict__[section].__dict__

    def __get_attribute__(self, item):
        print("CALLED")

if __name__ == '__main__':
    R = ReadConfig("test.cfg")
    print("%s, %s" % (R.DEFAULT.lname, R.DEFAULT.fname))
    print(R.get_sections())
    if R.testnames.has_item('t1'):
        print("-")
        print(R.testnames.t1)
        print("-")
    if R.testnames.has_item('tx'):
        print(R.testnames.tx)
    print(R.get_items('testnames'))
    print(R.get_items('test'))
    print(R.get_items())
