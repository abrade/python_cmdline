
import logging as _logging
import argparse as _argparse

import prompt_toolkit as _pt
import prompt_toolkit.history as _pt_history
import prompt_toolkit.contrib.completers as _completers

import pygments.style as _style
import pygments.styles.default as _default_style
import pygments.token as _token


class DocumentStyle(_style.Style):
    styles = {
        _token.Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        _token.Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
        _token.Token.Menu.Completions.ProgressButton: 'bg:#003333',
        _token.Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',
    }
    styles.update(_default_style.DefaultStyle.styles)

class Script(object):
    OPTIONS = []
    CMDS = []

    def __init__(self, options):
        self.options = options

    def run(self):
        pass

    def interactive(self):
        history = _pt_history.InMemoryHistory()
        cmd_list = [
            cmd['command'] for cmd in self.CMDS
        ]
        completion = _completers.WordCompleter(
            cmd_list,
            ignore_case=True,
        )
        while True:
            try:
                text = _pt.prompt(u'> ', style=DocumentStyle, history=history, completer=completion)
                if text:
                    splitted = text.strip().split()
                    cmd = splitted.pop(0)
                    if cmd in cmd_list:
                        command = getattr(self, cmd)
                        command(*splitted)
                if text == 'exit':
                    break
            except TypeError:
                print command.__doc__
            except KeyboardInterrupt:
                pass
            except EOFError:
                break

        print "Bye!"

    @classmethod
    def run_as_main(cls):
        arg_parse = _argparse.ArgumentParser()
        arg_parse.add_argument(
            '--verbose',
            dest='log_verbose',
            action='store_true',
            help='Set logger to loglevel INFO'
        )
        arg_parse.add_argument(
            '--debug',
            dest='log_debug',
            action='store_true',
            help='Set logger to loglevel DEBUG'
        )
        for opt in cls.OPTIONS:
            arg_parse.add_argument(
                opt['argument'],
                action=opt.get('action', 'store'),
                type=opt.get('type', str),
                help=opt.get('help', '')
            )

        cmd_parsers = arg_parse.add_subparsers(
            title='subcommands',
            help='sub-command help',
            dest='sub_parser',
        )
        cmd_parsers.add_parser(
            'interactive',
            help='Start script as prompt'
        )

        for cmd in cls.CMDS:
            cmd_name = cmd.get('command')
            cmd_parser = cmd_parsers.add_parser(
                cmd_name,
                help=cmd_name + ' help'
            )
            for cmd_opt in cmd.get('options'):
                cmd_parser.add_argument(
                    cmd_opt['argument'],
                    action=cmd_opt.get('action', 'store'),
                    type=cmd_opt.get('type', str),
                    help=cmd_opt.get('help', ''),
                )

        args = arg_parse.parse_args()
        loglevel = _logging.WARNING
        logformat= '[%(asctime)s] [ %(levelname)s ] %(name)s: %(message)s | %(filename)s %(funcName)s'
        if args.log_verbose:
            loglevel = _logging.INFO

        if args.log_debug:
            loglevel = _logging.DEBUG

        _logging.basicConfig(
            level=loglevel,
            format=logformat,
        )
        _log = _logging.getLogger(__name__)
        _log.info('Running Script!')
        runner = cls(args)
        if args.sub_parser == 'interactive':
            runner.interactive()
        else:
            runner.run()
