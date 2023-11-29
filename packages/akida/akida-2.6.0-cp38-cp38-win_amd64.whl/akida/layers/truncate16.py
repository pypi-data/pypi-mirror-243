from akida.core import (Layer, LayerParams, LayerType)


class Truncate16(Layer):
    """Akida Truncate16 layer corresponding to the quantizeml Truncate16 layer.

    This layer supports only 16-bits inputs and output their 8bit outputs.

    Args:
        input_shape (tuple): the 3D input shape.
        name (str, optional): name of the layer. Defaults to empty string.

    """

    def __init__(self,
                 input_shape,
                 name=""):
        try:
            params = LayerParams(
                LayerType.Truncate16, {
                    "input_x": input_shape[0],
                    "input_y": input_shape[1],
                    "input_c": input_shape[2]
                })
            # Call parent constructor to initialize C++ bindings
            # Note that we invoke directly __init__ instead of using super, as
            # specified in pybind documentation
            Layer.__init__(self, params, name)
        except BaseException:
            self = None
            raise
