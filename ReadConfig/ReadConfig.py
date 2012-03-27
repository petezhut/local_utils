#!/usr/bin/env python

class Section:
    def has_item(self, item):
        return self.__dict__.has_key(item)

class ReadConfig(object):
    """
    ReadConfig - An improved config parser.
    """
    sections = []
    def __load(self, lines):
        for line in filter(None, lines):
            if line.startswith("["):
                cursec = line.split("[")[-1].split("]")[0]
                self.sections.append(cursec)
                section = Section()
                setattr(self, cursec, section)
            else:
                k,v = line.split("=")
                setattr(section, k.strip(), v.strip())

    def read(self, cfg):
        """
        read(configfile) -> This loads a configfile into the object
        """
        try:
            f = open(cfg, 'rb')
            self.__load(map(lambda x: x.strip(), f.readlines()))
            f.close()
        except IOError, e:
            raise StandardError("Couldn't find config file: %s" % (cfg))

    def get_sections(self):
        """
        get_sections() -> Returns a list of the sections from the loaded config file.
        """
        return self.sections

    def has_section(self, section='DEFAULT'):
        """
        has_section(section_name) -> Returns a boolean for the presence of a section.
        If no section name is passed, it defaults to 'DEFAULT' as the section name.
        """
        return section.strip() in self.sections

    def get_items(self, section='DEFAULT'):
        """
        get_items(section_name) -> Returns the dictionary of items found with in the 
        specified section.  If no section name is passed, it defaults to 'DEFAULT' as 
        the section name.
        """
        return self.__dict__[section].__dict__

if __name__ == '__main__':
    R = ReadConfig()
#    R.read()
#    R.read("nope.cfg")
    R.read("test.cfg")

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
