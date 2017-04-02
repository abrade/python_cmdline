#!/usr/bin/env python

import cmdline.script as _script

class Test(_script.Script):
    """ simple test client"""

    OPTIONS = [
        {
            'argument': '--test',
            'help': 'helping string',
        },
    ]

    CMDS = [
        {
            'command': 'do_greet',
            'options': [
                {
                    'argument': '--person',
                    'help': 'greets a person',
                },
            ],
        },
    ]

    def do_greet(self, person):
        """ greet [person]
        Greet the named person
        """
        if person:
            print "hi,", person
        else:
            print "hi"

    def run(self):
        if self.options.sub_parser:
            getattr(self, self.options.sub_parser)(self.options.person)


if __name__ == '__main__':
    Test.run_as_main()
