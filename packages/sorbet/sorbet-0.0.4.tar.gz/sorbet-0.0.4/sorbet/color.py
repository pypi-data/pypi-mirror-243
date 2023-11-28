class Color:
    def black(*args):
        """Returns the arguments in black.

        :param args: The arguments to return in black.

        :type args: str

        :return: The arguments in black.
        """
        return f"\033[30m{' '.join(args)}\033[0m"

    def red(*args):
        """Returns the arguments in red.

        :param args: The arguments to return in red.

        :type args: str

        :return: The arguments in red.
        """
        return f"\033[31m{' '.join(args)}\033[0m"

    def green(*args):
        """Returns the arguments in green.

        :param args: The arguments to return in green.

        :type args: str

        :return: The arguments in green.
        """
        return f"\033[32m{' '.join(args)}\033[0m"

    def yellow(*args):
        """Returns the arguments in yellow.

        :param args: The arguments to return in yellow.

        :type args: str

        :return: The arguments in yellow.
        """
        return f"\033[33m{' '.join(args)}\033[0m"

    def blue(*args):
        """Returns the arguments in blue.

        :param args: The arguments to return in blue.

        :type args: str

        :return: The arguments in blue.
        """
        return f"\033[34m{' '.join(args)}\033[0m"

    def magenta(*args):
        """Returns the arguments in magenta.

        :param args: The arguments to return in magenta.

        :type args: str

        :return: The arguments in magenta.
        """
        return f"\033[35m{' '.join(args)}\033[0m"

    def cyan(*args):
        """Returns the arguments in cyan.

        :param args: The arguments to return in cyan.

        :type args: str

        :return: The arguments in cyan.
        """
        return f"\033[36m{' '.join(args)}\033[0m"

    def white(*args):
        """Returns the arguments in white.

        :param args: The arguments to return in white.

        :type args: str

        :return: The arguments in white.
        """
        return f"\033[37m{' '.join(args)}\033[0m"

    def bright_black(*args):
        """Returns the arguments in bright black.

        :param args: The arguments to return in bright black.

        :type args: str

        :return: The arguments in bright black.
        """
        return f"\033[90m{' '.join(args)}\033[0m"

    def bright_red(*args):
        """Returns the arguments in bright red.

        :param args: The arguments to return in bright red.

        :type args: str

        :return: The arguments in bright red.
        """
        return f"\033[91m{' '.join(args)}\033[0m"

    def bright_green(*args):
        """Returns the arguments in bright green.

        :param args: The arguments to return in bright green.

        :type args: str

        :return: The arguments in bright green.
        """
        return f"\033[92m{' '.join(args)}\033[0m"

    def bright_yellow(*args):
        """Returns the arguments in bright yellow.

        :param args: The arguments to return in bright yellow.

        :type args: str

        :return: The arguments in bright yellow.
        """
        return f"\033[93m{' '.join(args)}\033[0m"

    def bright_blue(*args):
        """Returns the arguments in bright blue.

        :param args: The arguments to return in bright blue.

        :type args: str

        :return: The arguments in bright blue.
        """
        return f"\033[94m{' '.join(args)}\033[0m"

    def bright_magenta(*args):
        """Returns the arguments in bright magenta.

        :param args: The arguments to return in bright magenta.

        :type args: str

        :return: The arguments in bright magenta.
        """
        return f"\033[95m{' '.join(args)}\033[0m"

    def bright_cyan(*args):
        """Returns the arguments in bright cyan.

        :param args: The arguments to return in bright cyan.

        :type args: str

        :return: The arguments in bright cyan.
        """
        return f"\033[96m{' '.join(args)}\033[0m"

    def bright_white(*args):
        """Returns the arguments in bright white.

        :param args: The arguments to return in bright white.

        :type args: str

        :return: The arguments in bright white.
        """
        return f"\033[97m{' '.join(args)}\033[0m"


color = Color
