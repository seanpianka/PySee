import distutils


class CaptureTool:
    valid_tools = {}
    valid_modes = ['region', 'full', 'window']
    valid_flags = ['filename', 'delay']

    def __init__(self, name, command, **kwargs):
        self.name = name
        self.command = command
        self.modes = {mode: kwargs.get(mode, '')
                      for mode in CaptureTool.valid_modes}
        self.flags = {flag: kwargs.get(flag, '')
                      for flag in CaptureTool.valid_flags}

        # CaptureTool is not valid if not installed.
        if distutils.spawn.find_executable(command):
            CaptureTool.valid_tools[name] = self
