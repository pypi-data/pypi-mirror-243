from .color import *
from .format_strings import *
import inspect
import executing

DEFAULT_PREFIX = "🍨"


def get_arg_strings(call_frame):
    callNode = Source.executing(call_frame).node
    source = Source.for_frame(call_frame)
    return [source.get_text_with_indentation(arg) for arg in callNode.args]


class Source(executing.Source):
    def get_text_with_indentation(self, node):
        result = self.asttokens().get_text(node)
        if "\n" in result:
            result = " " * node.first_token.start[1] + result
            result = result
        result = result.strip()
        return result


class Sorbet:
    """The Sorbet class."""

    def __init__(self, prefix=DEFAULT_PREFIX, output=False, includeContext=False):
        """Initializes the Sorbet class.

        :param prefix: The prefix to use for the logger.
        :param output: Whether to output to the console.
        :param includeContext: Whether to include the context in the output.

        :type prefix: str
        :type output: bool
        :type includeContext: bool

        :return: None
        """
        self.enabled = True
        self.prefix = prefix
        self.output = output
        self.includeContext = includeContext

    def __call__(self, *args):
        """Called when the class is called.

        :param args: The arguments to pass to the class.

        :type args: Tuple[Any]

        :return: Any | None
        """
        if self.enabled:
            callFrame = inspect.currentframe().f_back
            try:
                out = self._out(callFrame, args)
            except Exception as e:
                out = f"{self.prefix} | {color.red('Error')}: {e}"
            print(out) if self.enabled else None

        if not args:  # sb()
            returns = None
        elif len(args) == 1:  # sb(1)
            returns = args[0]
        else:  # sb(1, 2, 3).
            returns = args
        return returns
    
    def enable(self):
        """Enables the logger.

        :return: None
        """
        self.enabled = True


    def disable(self):
        """Disables the logger.

        :return: None
        """
        self.enabled = False

    def _get_caller_info(self, caller_frame):
        """Gets the caller info.

        :param caller_frame: The caller frame.

        :type caller_frame: inspect.FrameInfo

        :return: Tuple[str, int, str]
        """
        function_name = caller_frame.f_code.co_name
        line_number = caller_frame.f_lineno
        file_name = caller_frame.f_code.co_filename
        return function_name, line_number, file_name.split("\\")[-1].split("/")[-1]

    def _format_context(self, caller_frame):
        """Formats the context.
        
        :param caller_frame: The caller frame.
        
        :type caller_frame: inspect.FrameInfo
        
        :return: str
        """
        caller_info = self._get_caller_info(caller_frame)
        return f"{color.cyan(caller_info[2])}:{color.cyan(str(caller_info[1]))} > {color.cyan(caller_info[0])}{'()' if caller_info[0] != '<module>' else ''} | {color.cyan(get_time())} ; {color.cyan(get_date())}"

    def _out(self, callFrame, args):
        """Formats the output.

        :param callFrame: The call frame.
        :param args: The arguments to pass to the class.

        :type callFrame: inspect.FrameInfo
        :type args: Tuple[Any]

        :return: str
        """
        if not args:
            return f"{self.prefix} | {self._format_context(callFrame)}"
        else:
            argPairs = list(zip(get_arg_strings(callFrame), args))
            return f"{self.prefix} | {self._format_args(argPairs)}{' | ' + self._format_context(callFrame) if self.includeContext else ''}"

    def _format_args(self, argPairs):
        """Formats the arguments.

        :param args: The arguments to format.

        :type args: Tuple[Any]

        :return: str
        """
        _args = []
        for i in range(len(argPairs)):
            argPair = argPairs[i]
            arg = argPair[1]
            argName = argPair[0]
            if type(arg) in [str, int, float]:
                check_arg = str(arg).replace("'", "").replace('"', '')
                check_arg_name = argName.replace("'", "").replace('"', '')
                _args.append(
                    f"{color.cyan(f'<{type(arg).__name__}>')}{':' + color.cyan(argName) if check_arg != check_arg_name else ''} - {self._color_type(arg)}"
                )
            elif type(arg) in [list, tuple]:
                _args.append(
                    f"{color.cyan(f'<{type(arg).__name__}>')}{':' + color.cyan(argName) if str(arg) != argName else ''} - {'[' if type(arg) == list else '('}{self._format_lists(arg)}{']' if type(arg) == list else ')'}"
                )
            elif type(arg) == dict:
                check_arg = str(arg).replace("'", "").replace('"', '')
                _args.append(
                    f"{color.cyan(f'<{type(arg).__name__}>')}{':' + color.cyan(argName) if check_arg != argName else ''} - "
                    + self._format_dict(arg)
                )
            elif type(arg) in [bool]:
                _args.append(
                    f"{color.cyan(f'<{type(arg).__name__}>')}{':' + color.cyan(argName) if str(arg) != argName else ''} - "
                    + (color.green(str(arg)) if arg else color.red(str(arg)))
                )
            else:
                _args.append(
                    f"{color.cyan(f'<{type(arg).__name__}>')}{':' + color.cyan(argName) if str(arg) != argName else ''} - "
                    + str(arg)
                )

        return ", ".join(_args)

    def _format_lists(self, _list):
        """Formats the list.

        :param list: The list to format.

        :type list: list

        :return: str
        """
        items = []
        for i in range(len(_list)):
            item = _list[i]
            if type(item) in [str, int, float]:
                items.append(f"{self._color_type(item)}")
            elif type(item) in [list, tuple]:
                items.append(
                    f"{'[' if type(item) == list else '('}{self._format_lists(item)}{']' if type(item) == list else ')'}"
                )
            elif type(item) == dict:
                items.append(self._format_dict(item))
            elif type(item) in [bool]:
                items.append(color.green(str(item)) if item else color.red(str(item)))
            else:
                items.append(str(item))

        return ", ".join(items)

    def _format_dict(self, dict):
        """Formats the dictionary.

        :param dict: The dictionary to format.

        :type dict: dict

        :return: str
        """
        _dict = []
        for key in dict.keys():
            _dict.append(
                f"{self._color_type(str(key))}: {self._color_type(str(dict[key]))}"
            )
        return "{" + ", ".join(_dict) + "}"

    def _color_type(self, object):
        """Colors the type.

        :param object: The object to color.

        :type object: Any

        :return: str
        """
        if type(object) == str:
            return color.cyan("'" + object + "'")
        else:
            return color.cyan(str(object))


sb = Sorbet()
