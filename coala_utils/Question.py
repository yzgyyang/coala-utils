from pyprint.Printer import Printer
from pyprint.ConsolePrinter import ConsolePrinter
from coala_utils.Constants import TRUE_STRINGS, FALSE_STRINGS
from coala_utils.string_processing.StringConverter import StringConverter


def ask_question(question,
                 default=None,
                 printer: Printer = None,
                 typecast=str,
                 **kwargs):
    """
    Asks the user a question and returns the answer.

    :param question:
        String to be used as question.
    :param default:
        The default answer to be returned if the user gives a void answer
        to the question.
    :param printer:
        The printer object used for console interactions. If this is not
        given, it defaults to a ``ConsolePrinter`` which prints outputs to
        the console.
    :param typecast:
        Type to cast the input to. Defaults to a ``str``.
    :param kwargs:
        The additional keyword arguments are held for backwards compatibility
        and for future use with the ``prompt_toolkit``.
    :return:
        The response from the user.
    """
    if printer is None:
        printer = ConsolePrinter()

    while True:
        printer.print(question, color="yellow", end=" ")
        if default:
            printer.print("[" + default + "]", end=" ")
        printer.print("")

        answer = input()
        if default and len(answer) == 0:
            answer = default

        try:
            answer = typecast(StringConverter(answer))
        except BaseException as e:
            printer.print(
                str(e) + "\nPlease enter a valid answer.",
                color="blue")
        else:
            return answer


def ask_yes_no(question,
               default=None,
               printer: Printer = None):
    """
    Asks the user a yes/no question until the user gives a clear answer,
    and returns a boolean value representing the answer.

    :param question:
        String to be used as question.
    :param default:
        The default answer to be returned if the user gives a void answer
        to the question. It must be one of ('yes', 'no', None).
    :param printer:
        The printer object used for console interactions. If this is not
        given, it defaults to a ``ConsolePrinter`` which prints outputs to
        the console.
    :return:
        True if the user input is one of coala-utils.Constants.TRUE_STRING,
        False if the user input is one of coala-utils.Constant.FALSE_STRING.
        The user input is case insensitive.
    """
    if printer is None:
        printer = ConsolePrinter()

    if default is None:
        prompt = ' [y/n] '
    elif default == 'yes':
        prompt = ' [Y/n] '
    elif default == 'no':
        prompt = ' [y/N] '
    else:
        raise ValueError('Invalid default answer: %s' % default)

    while True:
        printer.print(question + prompt, color='yellow', end=' ')
        answer = input().lower().strip()

        if default and len(answer) == 0:
            answer = default

        if answer in TRUE_STRINGS:
            return True
        elif answer in FALSE_STRINGS:
            return False
        else:
            printer.print('Invalid answer, please try again.', color='red')
