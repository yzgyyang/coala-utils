import prompt_toolkit
from pygments.token import Token
from pygments.styles.tango import TangoStyle

from coala_utils.string_processing.StringConverter import StringConverter


def ask_question(question,
                 default="",
                 prefill=False,
                 typecast=str,
                 no_newline=False,
                 **kwargs):
    """
    Presents a question to the user with the question in yellow
    using ``prompt``.

    :param question:   String to be used as question.
    :param default:    The default answer to be returned if the user gives
                       a void answer to the question.
    :param prefill:    If True, the default answer is prefilled for the user.
    :param no_newline: If False, newline is appended to the question.
    :param typecast:   Type to cast the input to.
    :param kwargs:     Anything else to be passed on to ``prompt``.
    :return:           The answer from the user.
    """
    if "style" in kwargs:
        style = kwargs["style"]
        del kwargs["style"]
    else:
        style = prompt_toolkit.styles.style_from_pygments(
            TangoStyle,
            {Token.Prompt: "#ffff00"})

    if not prefill:
        question += " [{}]".format(default)

    if not no_newline:
        question += "\n"

    result = prompt_toolkit.prompt(
        question,
        default=default if prefill else "",
        style=style,
        **kwargs)

    if not prefill and result == "":
        return default
    else:
        return typecast(StringConverter(result))
