"""
This module provides the :class:`Amplifier` class, which is the base class of
all low level amplifier drivers. If you want to write a driver for a specific
amplifier your driver must derive from the :class:`Amplifier` class and
implement its methods.

Users will not use your driver directly but a decorated version of it which
provides additional features like writing data to a file and receiving marker
via TCP.

"""

class Amplifier(object):
    """Amplifier base class.

    The base class is very generic on purpose. Amplifiers from different
    vendors vary in so many ways that it is difficult to find a common set of
    methods that all support.

    In the spirit of "encapsulating what varies", I decided to encapsulate the
    configuration. So the main configuration of the amplifier, like setting the
    mode (e.g. data, impedance, etc.), sampling frequency, etc. happens in
    :meth:`configure` and is very specific for the amplifier at hand.

    :meth:`start`, :meth:`stop`, and :meth:`get_data` is very generic and must
    be supported by all derived amplifier classes.

    How an amplifier should be used::

        amp = Amp()

        # measure impedance
        amp.configure(config)
        amp.start()
        while 1:
            data = amp.get_data()
            if enough:
                break
        amp.stop()

        # measure data
        amp.configure(config)
        channels = amp.get_channels()
        amp.start()
        while 1:
            data = amp.get_data()
            if enough:
                break
        amp.stop()

    """

    def configure(self, config):
        """Configure the amplifier.

        Use this method to set the mode (i.e. impedance, data, ...), sampling
        frequency, filter, etc.

        This depends strongly on the amplifier.

        Args:
            config: The configuration of the amplifier.

        """
        pass

    def configure_with_gui(self):
        """Configure the amplifier interactively.

        Use this method to spawn a GUI which allows for configuring the
        amplifier. After the configuring is done it should call
        :meth:`configure` to configure the amplifier.

        """
        pass

    def start(self):
        """Make the amplifier ready for delivering data."""
        pass

    def stop(self):
        """Stop the amplifier."""
        pass

    def get_data(self):
        """Get data from the amplifier.

        This method is called as fast as possible (e.g. hundreds of times per
        second) and returns the data and the marker (if supported).

        Returns:
            A numpy array (time, channels) and a list of markers.

        """
        pass

    def get_channels(self):
        """Return the list of channel names.

        The list has the same order as the data, i.e. the second name in the
        list represents the second colum of the data returned by
        :meth:`get_data`.

        Returns:
            A list of channel names.

        """
        raise NotImplementedError

    def get_sampling_frequency(self):
        """Return the sampling frequency.

        This method returns the sampling frequency which is currently enabled
        in the amplifier.

        Returns:
            A float.

        """
        raise NotImplementedError

    @staticmethod
    def is_available():
        """Is the amplifier connected to the computer?

        This method should be overwritten by derived classes and return True if
        the amplifier is connected to the computer or False if not.

        Returns:
            A boolean

        """
        raise NotImplementedError

