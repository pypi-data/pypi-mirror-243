#
# Automatically generated file, do not edit!
#

"""
    ArducamEvkSDK
"""
from __future__ import annotations
import ArducamEvkSDK
import typing

__all__ = [
    "Camera",
    "CameraConfig",
    "CaptureMethodConflict",
    "CaptureTimeout",
    "ConfigFileEmpty",
    "ConfigFormatError",
    "Control",
    "ControlFormatError",
    "Critical",
    "DMA",
    "Debug",
    "Device",
    "DeviceConnect",
    "DeviceDisconnect",
    "DeviceToHost",
    "Empty",
    "Err",
    "ErrorCode",
    "EventCode",
    "Exit",
    "Format",
    "FormatMode",
    "Frame",
    "FrameEnd",
    "FrameStart",
    "FreeEmptyBuffer",
    "FreeUnknowBuffer",
    "Full",
    "High",
    "HostToDevice",
    "I2CMode",
    "I2C_MODE_16_16",
    "I2C_MODE_16_32",
    "I2C_MODE_16_8",
    "I2C_MODE_8_16",
    "I2C_MODE_8_8",
    "Info",
    "InitCameraFailed",
    "JPG",
    "LoggerLevel",
    "Low",
    "MON",
    "MON_D",
    "MemType",
    "MemoryAllocateFailed",
    "NotSupport",
    "Off",
    "OpenCameraFailed",
    "Param",
    "RAM",
    "RAW",
    "RAW_D",
    "RGB",
    "ReadConfigFileFailed",
    "RegisterMultipleCallback",
    "STATS",
    "StateError",
    "Success",
    "Super",
    "SuperPlus",
    "Trace",
    "TransferError",
    "TransferTimeout",
    "USBSpeed",
    "USBTypeMismatch",
    "Unknown",
    "UnknownDeviceType",
    "UnknownError",
    "UnknownUSBType",
    "UserdataAddrError",
    "UserdataLenError",
    "VRCommandDirection",
    "VRCommandError",
    "Warn",
    "YUV",
    "free_device_list",
    "get_error_name",
    "list_devices"
]


class Camera():
    def __init__(self) -> None: ...
    def add_log_file(self, filename: str) -> bool: 
        """
        add a log file
        """
    def capture(self, timeout: int = 2000) -> typing.Optional[Frame]: 
        """
        capture a image, return a object of Frame, or None if failed
        """
    def check_usb_type(self) -> bool: 
        """
        check the connection usb type is expected or not
        """
    def close(self) -> bool: 
        """
        close the camera
        """
    def enable_console_log(self, enable: bool = True) -> None: 
        """
        enable/disable console log
        """
    def has_capture_callback(self) -> bool: 
        """
        check if the callback function for reading a frame is set
        """
    def has_event_callback(self) -> bool: 
        """
        check if the callback function for event is set
        """
    def has_message_callback(self) -> bool: 
        """
        check if the callback function for message is set
        """
    def init(self) -> bool: 
        """
        init the camera
        """
    def open(self, param: Param) -> bool: 
        """
        open the camera
        """
    def read_board_config(self, command: int, value: int, index: int, buf_size: int) -> typing.Optional[typing.List[int]]: 
        """
        read sensor register
        """
    def read_reg(self, mode: I2CMode, i2c_addr: int, regAddr: int) -> typing.Optional[int]: 
        """
        read sensor register
        """
    def read_reg_16_16(self, ship_addr: int, reg_addr: int) -> typing.Optional[int]: 
        """
        Reads a register value with 16 bit address and 16-bit value.
        """
    def read_reg_16_8(self, ship_addr: int, reg_addr: int) -> typing.Optional[int]: 
        """
        Reads a register value with 16 bit address and 8-bit value.
        """
    def read_reg_8_16(self, ship_addr: int, reg_addr: int) -> typing.Optional[int]: 
        """
        Reads a register value with 8 bit address and 16-bit value.
        """
    def read_reg_8_8(self, ship_addr: int, reg_addr: int) -> typing.Optional[int]: 
        """
        Reads a register value with 8 bit address and 8-bit value.
        """
    def read_sensor_reg(self, reg_addr: int) -> typing.Optional[int]: 
        """
        read sensor register
        """
    def read_user_data(self, addr: int, len: int) -> typing.Optional[typing.List[int]]: 
        """
        read sensor register
        """
    def register_control(self, controls: typing.List[Control]) -> bool: 
        """
        register controls
        """
    def send_vr(self, command: int, direction: int, value: int, index: int, buffer: typing.List[int]) -> bool: 
        """
        send vendor request
        """
    def set_auto_transfer(self, auto_transfer: bool) -> bool: 
        """
        enable or disable the automatic transfer configuration setting before starting the camera
        """
    def set_capture_callback(self, callback: typing.Callable[[Frame], None]) -> None: 
        """
        set the callback function for reading a frame, or None to disable it
        """
    def set_control(self, controlId: str, value: int) -> bool: 
        """
        set control value
        """
    def set_event_callback(self, callback: typing.Callable[[EventCode], None]) -> None: 
        """
        set the callback function for event, or None to disable it
        """
    def set_message_callback(self, callback: typing.Callable[[LoggerLevel, str], None]) -> None: 
        """
        set the callback function for messages, or None to disable it
        """
    def set_transfer(self, transfer_size: int, transfer_buffer_size: int) -> bool: 
        """
        set transfer size and buffer size
        """
    def start(self) -> bool: 
        """
        start the camera
        """
    def stop(self) -> None: 
        """
        stop the camera
        """
    def switch_mode(self, mode_id: int) -> bool: 
        """
        switch the camera mode
        """
    def write_board_config(self, command: int, value: int, index: int, buf: typing.List[int]) -> bool: 
        """
        write sensor register
        """
    def write_reg(self, mode: I2CMode, i2c_addr: int, regAddr: int, value: int) -> bool: 
        """
        write sensor register
        """
    def write_reg_16_16(self, ship_addr: int, reg_addr: int, value: int) -> bool: 
        """
        Writes a register value with 16 bit address and 16-bit value.
        """
    def write_reg_16_8(self, ship_addr: int, reg_addr: int, value: int) -> bool: 
        """
        Writes a register value with 16 bit address and 8-bit value.
        """
    def write_reg_8_16(self, ship_addr: int, reg_addr: int, value: int) -> bool: 
        """
        Writes a register value with 8 bit address and 16-bit value.
        """
    def write_reg_8_8(self, ship_addr: int, reg_addr: int, value: int) -> bool: 
        """
        Writes a register value with 8 bit address and 8-bit value.
        """
    def write_sensor_reg(self, reg_addr: int, value: int) -> bool: 
        """
        write sensor register
        """
    def write_user_data(self, addr: int, data: typing.List[int]) -> bool: 
        """
        write sensor register
        """
    @property
    def bandwidth(self) -> int:
        """
        A property of bandwidth (read-only).

        :type: int
        """
    @bandwidth.setter
    def bandwidth(self) -> None:
        """
        A property of bandwidth (read-only).
        """
    @property
    def bin_config(self) -> dict:
        """
        A property of bin_config (read-only).

        :type: dict
        """
    @bin_config.setter
    def bin_config(self) -> None:
        """
        A property of bin_config (read-only).
        """
    @property
    def capture_fps(self) -> int:
        """
        A property of capture_fps (read-only).

        :type: int
        """
    @capture_fps.setter
    def capture_fps(self) -> None:
        """
        A property of capture_fps (read-only).
        """
    @property
    def config(self) -> CameraConfig:
        """
        A property of config.

        :type: CameraConfig
        """
    @config.setter
    def config(self, arg1: CameraConfig) -> None:
        """
        A property of config.
        """
    @property
    def config_type(self) -> str:
        """
        A property of config_type (read-only). (NONE | TEXT | BINARY)

        :type: str
        """
    @config_type.setter
    def config_type(self) -> None:
        """
        A property of config_type (read-only). (NONE | TEXT | BINARY)
        """
    @property
    def controls(self) -> typing.List[Control]:
        """
        A property of controls (read-only).

        :type: typing.List[Control]
        """
    @controls.setter
    def controls(self) -> None:
        """
        A property of controls (read-only).
        """
    @property
    def force_capture(self) -> bool:
        """
        A property of force_capture.

        :type: bool
        """
    @force_capture.setter
    def force_capture(self, arg1: bool) -> None:
        """
        A property of force_capture.
        """
    @property
    def last_error(self) -> int:
        """
        A property of last_error (read-only).

        :type: int
        """
    @last_error.setter
    def last_error(self) -> None:
        """
        A property of last_error (read-only).
        """
    @property
    def last_error_message(self) -> str:
        """
        A property of last_error_message (read-only).

        :type: str
        """
    @last_error_message.setter
    def last_error_message(self) -> None:
        """
        A property of last_error_message (read-only).
        """
    @property
    def log_level(self) -> LoggerLevel:
        """
        A property of log_level.

        :type: LoggerLevel
        """
    @log_level.setter
    def log_level(self, arg1: LoggerLevel) -> None:
        """
        A property of log_level.
        """
    @property
    def mem_type(self) -> MemType:
        """
        A property of mem_type.

        :type: MemType
        """
    @mem_type.setter
    def mem_type(self, arg1: MemType) -> None:
        """
        A property of mem_type.
        """
    @property
    def usb_type(self) -> str:
        """
        A property of usb_type (read-only).

        :type: str
        """
    @usb_type.setter
    def usb_type(self) -> None:
        """
        A property of usb_type (read-only).
        """
    pass
class CameraConfig():
    def __init__(self) -> None: ...
    @property
    def bit_width(self) -> int:
        """
        A property of bit_width.

        :type: int
        """
    @bit_width.setter
    def bit_width(self, arg0: int) -> None:
        """
        A property of bit_width.
        """
    @property
    def format(self) -> int:
        """
        A property of format.

        :type: int
        """
    @format.setter
    def format(self, arg0: int) -> None:
        """
        A property of format.
        """
    @property
    def height(self) -> int:
        """
        A property of height.

        :type: int
        """
    @height.setter
    def height(self, arg0: int) -> None:
        """
        A property of height.
        """
    @property
    def i2c_addr(self) -> int:
        """
        A property of i2c_addr.

        :type: int
        """
    @i2c_addr.setter
    def i2c_addr(self, arg0: int) -> None:
        """
        A property of i2c_addr.
        """
    @property
    def i2c_mode(self) -> int:
        """
        A property of i2c_mode.

        :type: int
        """
    @i2c_mode.setter
    def i2c_mode(self, arg0: int) -> None:
        """
        A property of i2c_mode.
        """
    @property
    def width(self) -> int:
        """
        A property of width.

        :type: int
        """
    @width.setter
    def width(self, arg0: int) -> None:
        """
        A property of width.
        """
    pass
class Control():
    def __init__(self) -> None: 
        """
        Creates a new control.
        """
    def __repr__(self) -> str: 
        """
        Returns a string representation of the control.
        """
    def __str__(self) -> str: 
        """
        Returns a string representation of the control.
        """
    @property
    def code(self) -> str:
        """
        A property of code.

        :type: str
        """
    @code.setter
    def code(self, arg0: str) -> None:
        """
        A property of code.
        """
    @property
    def default(self) -> int:
        """
        A property of default.

        :type: int
        """
    @default.setter
    def default(self, arg0: int) -> None:
        """
        A property of default.
        """
    @property
    def flags(self) -> int:
        """
        A property of flags.

        :type: int
        """
    @flags.setter
    def flags(self, arg0: int) -> None:
        """
        A property of flags.
        """
    @property
    def func(self) -> str:
        """
        A property of func (read-only).

        :type: str
        """
    @func.setter
    def func(self) -> None:
        """
        A property of func (read-only).
        """
    @property
    def max(self) -> int:
        """
        A property of max.

        :type: int
        """
    @max.setter
    def max(self, arg0: int) -> None:
        """
        A property of max.
        """
    @property
    def min(self) -> int:
        """
        A property of min.

        :type: int
        """
    @min.setter
    def min(self, arg0: int) -> None:
        """
        A property of min.
        """
    @property
    def name(self) -> str:
        """
        A property of name (read-only).

        :type: str
        """
    @name.setter
    def name(self) -> None:
        """
        A property of name (read-only).
        """
    @property
    def step(self) -> int:
        """
        A property of step.

        :type: int
        """
    @step.setter
    def step(self, arg0: int) -> None:
        """
        A property of step.
        """
    pass
class Device():
    def __repr__(self) -> str: 
        """
        Returns a string representation of the device.
        """
    @property
    def id_product(self) -> int:
        """
        A property of id_product (const).

        :type: int
        """
    @property
    def id_vendor(self) -> int:
        """
        A property of id_vendor (const).

        :type: int
        """
    @property
    def in_used(self) -> bool:
        """
        A property of in_used (const).

        :type: bool
        """
    @property
    def serial_number(self) -> typing.List[int]:
        """
        A property of serial_number (const).This is a list with 12 elements.

        :type: typing.List[int]
        """
    @property
    def speed(self) -> USBSpeed:
        """
        A property of speed (const).

        :type: USBSpeed
        """
    @property
    def usb_type(self) -> int:
        """
        A property of usb_type (const).

        :type: int
        """
    pass
class ErrorCode():
    """
    Members:

      Success : Success.

      Empty : Empty.

      ReadConfigFileFailed : Failed to read configuration file.

      ConfigFileEmpty : Configuration file is empty.

      ConfigFormatError : Camera configuration format error.

      ControlFormatError : Camera control format error.

      OpenCameraFailed : Failed to open camera.

      UnknownUSBType : Unknown USB type.

      UnknownDeviceType : Unknown Device type.

      InitCameraFailed : Failed to initialize camera.

      MemoryAllocateFailed : Failed to allocate memory.

      USBTypeMismatch : USB type mismatch.

      CaptureTimeout : Capture timeout.

      CaptureMethodConflict : Capture method conflict.

      FreeEmptyBuffer : Free empty buffer.

      FreeUnknowBuffer : Free unknown buffer.

      RegisterMultipleCallback : Register multiple callback.

      StateError : Camera state error.

      NotSupport : Not support.

      VRCommandError : Vendor command error.

      UserdataAddrError : Userdata address error.

      UserdataLenError : Userdata length error.

      UnknownError : Unknown error.
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    CaptureMethodConflict: ArducamEvkSDK.ErrorCode # value = <ErrorCode.CaptureMethodConflict: 1538>
    CaptureTimeout: ArducamEvkSDK.ErrorCode # value = <ErrorCode.CaptureTimeout: 1537>
    ConfigFileEmpty: ArducamEvkSDK.ErrorCode # value = <ErrorCode.ConfigFileEmpty: 258>
    ConfigFormatError: ArducamEvkSDK.ErrorCode # value = <ErrorCode.ConfigFormatError: 259>
    ControlFormatError: ArducamEvkSDK.ErrorCode # value = <ErrorCode.ControlFormatError: 260>
    Empty: ArducamEvkSDK.ErrorCode # value = <ErrorCode.Empty: 16>
    FreeEmptyBuffer: ArducamEvkSDK.ErrorCode # value = <ErrorCode.FreeEmptyBuffer: 1793>
    FreeUnknowBuffer: ArducamEvkSDK.ErrorCode # value = <ErrorCode.FreeUnknowBuffer: 1794>
    InitCameraFailed: ArducamEvkSDK.ErrorCode # value = <ErrorCode.InitCameraFailed: 769>
    MemoryAllocateFailed: ArducamEvkSDK.ErrorCode # value = <ErrorCode.MemoryAllocateFailed: 770>
    NotSupport: ArducamEvkSDK.ErrorCode # value = <ErrorCode.NotSupport: 61441>
    OpenCameraFailed: ArducamEvkSDK.ErrorCode # value = <ErrorCode.OpenCameraFailed: 513>
    ReadConfigFileFailed: ArducamEvkSDK.ErrorCode # value = <ErrorCode.ReadConfigFileFailed: 257>
    RegisterMultipleCallback: ArducamEvkSDK.ErrorCode # value = <ErrorCode.RegisterMultipleCallback: 2049>
    StateError: ArducamEvkSDK.ErrorCode # value = <ErrorCode.StateError: 32769>
    Success: ArducamEvkSDK.ErrorCode # value = <ErrorCode.Success: 0>
    USBTypeMismatch: ArducamEvkSDK.ErrorCode # value = <ErrorCode.USBTypeMismatch: 1025>
    UnknownDeviceType: ArducamEvkSDK.ErrorCode # value = <ErrorCode.UnknownDeviceType: 515>
    UnknownError: ArducamEvkSDK.ErrorCode # value = <ErrorCode.UnknownError: 65535>
    UnknownUSBType: ArducamEvkSDK.ErrorCode # value = <ErrorCode.UnknownUSBType: 514>
    UserdataAddrError: ArducamEvkSDK.ErrorCode # value = <ErrorCode.UserdataAddrError: 65377>
    UserdataLenError: ArducamEvkSDK.ErrorCode # value = <ErrorCode.UserdataLenError: 65378>
    VRCommandError: ArducamEvkSDK.ErrorCode # value = <ErrorCode.VRCommandError: 65283>
    __members__: dict # value = {'Success': <ErrorCode.Success: 0>, 'Empty': <ErrorCode.Empty: 16>, 'ReadConfigFileFailed': <ErrorCode.ReadConfigFileFailed: 257>, 'ConfigFileEmpty': <ErrorCode.ConfigFileEmpty: 258>, 'ConfigFormatError': <ErrorCode.ConfigFormatError: 259>, 'ControlFormatError': <ErrorCode.ControlFormatError: 260>, 'OpenCameraFailed': <ErrorCode.OpenCameraFailed: 513>, 'UnknownUSBType': <ErrorCode.UnknownUSBType: 514>, 'UnknownDeviceType': <ErrorCode.UnknownDeviceType: 515>, 'InitCameraFailed': <ErrorCode.InitCameraFailed: 769>, 'MemoryAllocateFailed': <ErrorCode.MemoryAllocateFailed: 770>, 'USBTypeMismatch': <ErrorCode.USBTypeMismatch: 1025>, 'CaptureTimeout': <ErrorCode.CaptureTimeout: 1537>, 'CaptureMethodConflict': <ErrorCode.CaptureMethodConflict: 1538>, 'FreeEmptyBuffer': <ErrorCode.FreeEmptyBuffer: 1793>, 'FreeUnknowBuffer': <ErrorCode.FreeUnknowBuffer: 1794>, 'RegisterMultipleCallback': <ErrorCode.RegisterMultipleCallback: 2049>, 'StateError': <ErrorCode.StateError: 32769>, 'NotSupport': <ErrorCode.NotSupport: 61441>, 'VRCommandError': <ErrorCode.VRCommandError: 65283>, 'UserdataAddrError': <ErrorCode.UserdataAddrError: 65377>, 'UserdataLenError': <ErrorCode.UserdataLenError: 65378>, 'UnknownError': <ErrorCode.UnknownError: 65535>}
    pass
class EventCode():
    """
    Members:

      FrameStart : Frame start

      FrameEnd : Frame end

      Exit : Exit

      TransferError : Transfer error

      TransferTimeout : Transfer timeout

      DeviceConnect : Device connect

      DeviceDisconnect : Device disconnect
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    DeviceConnect: ArducamEvkSDK.EventCode # value = <EventCode.DeviceConnect: 512>
    DeviceDisconnect: ArducamEvkSDK.EventCode # value = <EventCode.DeviceDisconnect: 513>
    Exit: ArducamEvkSDK.EventCode # value = <EventCode.Exit: 3>
    FrameEnd: ArducamEvkSDK.EventCode # value = <EventCode.FrameEnd: 2>
    FrameStart: ArducamEvkSDK.EventCode # value = <EventCode.FrameStart: 1>
    TransferError: ArducamEvkSDK.EventCode # value = <EventCode.TransferError: 256>
    TransferTimeout: ArducamEvkSDK.EventCode # value = <EventCode.TransferTimeout: 257>
    __members__: dict # value = {'FrameStart': <EventCode.FrameStart: 1>, 'FrameEnd': <EventCode.FrameEnd: 2>, 'Exit': <EventCode.Exit: 3>, 'TransferError': <EventCode.TransferError: 256>, 'TransferTimeout': <EventCode.TransferTimeout: 257>, 'DeviceConnect': <EventCode.DeviceConnect: 512>, 'DeviceDisconnect': <EventCode.DeviceDisconnect: 513>}
    pass
class Format():
    def __init__(self) -> None: ...
    @property
    def bit_depth(self) -> int:
        """
        A property of bit_depth.

        :type: int
        """
    @bit_depth.setter
    def bit_depth(self, arg0: int) -> None:
        """
        A property of bit_depth.
        """
    @property
    def format_code(self) -> int:
        """
        A property of format_code.

        :type: int
        """
    @format_code.setter
    def format_code(self, arg0: int) -> None:
        """
        A property of format_code.
        """
    @property
    def height(self) -> int:
        """
        A property of height.

        :type: int
        """
    @height.setter
    def height(self, arg0: int) -> None:
        """
        A property of height.
        """
    @property
    def width(self) -> int:
        """
        A property of width.

        :type: int
        """
    @width.setter
    def width(self, arg0: int) -> None:
        """
        A property of width.
        """
    pass
class FormatMode():
    """
    Members:

      RAW : RAW

      RGB : RGB

      YUV : YUV

      JPG : JPG

      MON : MON

      RAW_D : RAW_D

      MON_D : MON_D

      STATS : STATS
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    JPG: ArducamEvkSDK.FormatMode # value = <FormatMode.JPG: 3>
    MON: ArducamEvkSDK.FormatMode # value = <FormatMode.MON: 4>
    MON_D: ArducamEvkSDK.FormatMode # value = <FormatMode.MON_D: 6>
    RAW: ArducamEvkSDK.FormatMode # value = <FormatMode.RAW: 0>
    RAW_D: ArducamEvkSDK.FormatMode # value = <FormatMode.RAW_D: 5>
    RGB: ArducamEvkSDK.FormatMode # value = <FormatMode.RGB: 1>
    STATS: ArducamEvkSDK.FormatMode # value = <FormatMode.STATS: 8>
    YUV: ArducamEvkSDK.FormatMode # value = <FormatMode.YUV: 2>
    __members__: dict # value = {'RAW': <FormatMode.RAW: 0>, 'RGB': <FormatMode.RGB: 1>, 'YUV': <FormatMode.YUV: 2>, 'JPG': <FormatMode.JPG: 3>, 'MON': <FormatMode.MON: 4>, 'RAW_D': <FormatMode.RAW_D: 5>, 'MON_D': <FormatMode.MON_D: 6>, 'STATS': <FormatMode.STATS: 8>}
    pass
class Frame():
    def __init__(self) -> None: ...
    @property
    def bad(self) -> bool:
        """
        A property of bad.

        :type: bool
        """
    @bad.setter
    def bad(self, arg0: bool) -> None:
        """
        A property of bad.
        """
    @property
    def data(self) -> numpy.ndarray[numpy.uint8]:
        """
        A property of data.

        :type: numpy.ndarray[numpy.uint8]
        """
    @data.setter
    def data(self, arg0: numpy.ndarray[numpy.uint8]) -> None:
        """
        A property of data.
        """
    @property
    def format(self) -> Format:
        """
        A property of format.

        :type: Format
        """
    @format.setter
    def format(self, arg0: Format) -> None:
        """
        A property of format.
        """
    @property
    def seq(self) -> int:
        """
        A property of seq.

        :type: int
        """
    @seq.setter
    def seq(self, arg0: int) -> None:
        """
        A property of seq.
        """
    pass
class I2CMode():
    """
    Members:

      I2C_MODE_8_8 : 8-bit register address and 8-bit data

      I2C_MODE_8_16 : 8-bit register address and 16-bit data

      I2C_MODE_16_8 : 16-bit register address and 8-bit data

      I2C_MODE_16_16 : 16-bit register address and 16-bit data

      I2C_MODE_16_32 : 16-bit register address and 32-bit data
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    I2C_MODE_16_16: ArducamEvkSDK.I2CMode # value = <I2CMode.I2C_MODE_16_16: 3>
    I2C_MODE_16_32: ArducamEvkSDK.I2CMode # value = <I2CMode.I2C_MODE_16_32: 4>
    I2C_MODE_16_8: ArducamEvkSDK.I2CMode # value = <I2CMode.I2C_MODE_16_8: 2>
    I2C_MODE_8_16: ArducamEvkSDK.I2CMode # value = <I2CMode.I2C_MODE_8_16: 1>
    I2C_MODE_8_8: ArducamEvkSDK.I2CMode # value = <I2CMode.I2C_MODE_8_8: 0>
    __members__: dict # value = {'I2C_MODE_8_8': <I2CMode.I2C_MODE_8_8: 0>, 'I2C_MODE_8_16': <I2CMode.I2C_MODE_8_16: 1>, 'I2C_MODE_16_8': <I2CMode.I2C_MODE_16_8: 2>, 'I2C_MODE_16_16': <I2CMode.I2C_MODE_16_16: 3>, 'I2C_MODE_16_32': <I2CMode.I2C_MODE_16_32: 4>}
    pass
class LoggerLevel():
    """
    Members:

      Trace : trace log level

      Debug : debug log level

      Info : info log level

      Warn : warn log level

      Err : err log level

      Critical : critical log level

      Off : off log level
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    Critical: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.Critical: 5>
    Debug: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.Debug: 1>
    Err: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.Err: 4>
    Info: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.Info: 2>
    Off: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.Off: 6>
    Trace: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.Trace: 0>
    Warn: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.Warn: 3>
    __members__: dict # value = {'Trace': <LoggerLevel.Trace: 0>, 'Debug': <LoggerLevel.Debug: 1>, 'Info': <LoggerLevel.Info: 2>, 'Warn': <LoggerLevel.Warn: 3>, 'Err': <LoggerLevel.Err: 4>, 'Critical': <LoggerLevel.Critical: 5>, 'Off': <LoggerLevel.Off: 6>}
    pass
class MemType():
    """
    Members:

      DMA : DMA

      RAM : RAM
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    DMA: ArducamEvkSDK.MemType # value = <MemType.DMA: 1>
    RAM: ArducamEvkSDK.MemType # value = <MemType.RAM: 2>
    __members__: dict # value = {'DMA': <MemType.DMA: 1>, 'RAM': <MemType.RAM: 2>}
    pass
class Param():
    def __init__(self) -> None: 
        """
        construct a default param
        """
    @property
    def bin_config(self) -> bool:
        """
        A property of bin_config.

        :type: bool
        """
    @bin_config.setter
    def bin_config(self, arg0: bool) -> None:
        """
        A property of bin_config.
        """
    @property
    def config_file_name(self) -> str:
        """
        A property of config_file_name.

        :type: str
        """
    @config_file_name.setter
    def config_file_name(self, arg0: str) -> None:
        """
        A property of config_file_name.
        """
    @property
    def device(self) -> Device:
        """
        A property of device.

        :type: Device
        """
    @device.setter
    def device(self, arg0: Device) -> None:
        """
        A property of device.
        """
    @property
    def mem_type(self) -> MemType:
        """
        A property of mem_type.

        :type: MemType
        """
    @mem_type.setter
    def mem_type(self, arg0: MemType) -> None:
        """
        A property of mem_type.
        """
    pass
class USBSpeed():
    """
    Members:

      Unknown : The OS doesn't report or know the device speed.

      Low : The device is operating at low speed (1.5MBit/s).

      Full : The device is operating at full speed (12MBit/s).

      High : The device is operating at high speed (480MBit/s).

      Super : The device is operating at super speed (5000MBit/s).

      SuperPlus : The device is operating at super speed plus (10000MBit/s).
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    Full: ArducamEvkSDK.USBSpeed # value = <USBSpeed.Full: 2>
    High: ArducamEvkSDK.USBSpeed # value = <USBSpeed.High: 3>
    Low: ArducamEvkSDK.USBSpeed # value = <USBSpeed.Low: 1>
    Super: ArducamEvkSDK.USBSpeed # value = <USBSpeed.Super: 4>
    SuperPlus: ArducamEvkSDK.USBSpeed # value = <USBSpeed.SuperPlus: 5>
    Unknown: ArducamEvkSDK.USBSpeed # value = <USBSpeed.Unknown: 0>
    __members__: dict # value = {'Unknown': <USBSpeed.Unknown: 0>, 'Low': <USBSpeed.Low: 1>, 'Full': <USBSpeed.Full: 2>, 'High': <USBSpeed.High: 3>, 'Super': <USBSpeed.Super: 4>, 'SuperPlus': <USBSpeed.SuperPlus: 5>}
    pass
class VRCommandDirection():
    """
    Members:

      HostToDevice : Host to device

      DeviceToHost : Device to host
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    DeviceToHost: ArducamEvkSDK.VRCommandDirection # value = <VRCommandDirection.DeviceToHost: 128>
    HostToDevice: ArducamEvkSDK.VRCommandDirection # value = <VRCommandDirection.HostToDevice: 0>
    __members__: dict # value = {'HostToDevice': <VRCommandDirection.HostToDevice: 0>, 'DeviceToHost': <VRCommandDirection.DeviceToHost: 128>}
    pass
def free_device_list() -> None:
    """
    free the device list
    """
def get_error_name(ec: int) -> str:
    """
    get the error name
    """
def list_devices() -> typing.List[Device]:
    """
    list all supported devices
    """
CaptureMethodConflict: ArducamEvkSDK.ErrorCode # value = <ErrorCode.CaptureMethodConflict: 1538>
CaptureTimeout: ArducamEvkSDK.ErrorCode # value = <ErrorCode.CaptureTimeout: 1537>
ConfigFileEmpty: ArducamEvkSDK.ErrorCode # value = <ErrorCode.ConfigFileEmpty: 258>
ConfigFormatError: ArducamEvkSDK.ErrorCode # value = <ErrorCode.ConfigFormatError: 259>
ControlFormatError: ArducamEvkSDK.ErrorCode # value = <ErrorCode.ControlFormatError: 260>
Critical: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.Critical: 5>
DMA: ArducamEvkSDK.MemType # value = <MemType.DMA: 1>
Debug: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.Debug: 1>
DeviceConnect: ArducamEvkSDK.EventCode # value = <EventCode.DeviceConnect: 512>
DeviceDisconnect: ArducamEvkSDK.EventCode # value = <EventCode.DeviceDisconnect: 513>
DeviceToHost: ArducamEvkSDK.VRCommandDirection # value = <VRCommandDirection.DeviceToHost: 128>
Empty: ArducamEvkSDK.ErrorCode # value = <ErrorCode.Empty: 16>
Err: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.Err: 4>
Exit: ArducamEvkSDK.EventCode # value = <EventCode.Exit: 3>
FrameEnd: ArducamEvkSDK.EventCode # value = <EventCode.FrameEnd: 2>
FrameStart: ArducamEvkSDK.EventCode # value = <EventCode.FrameStart: 1>
FreeEmptyBuffer: ArducamEvkSDK.ErrorCode # value = <ErrorCode.FreeEmptyBuffer: 1793>
FreeUnknowBuffer: ArducamEvkSDK.ErrorCode # value = <ErrorCode.FreeUnknowBuffer: 1794>
Full: ArducamEvkSDK.USBSpeed # value = <USBSpeed.Full: 2>
High: ArducamEvkSDK.USBSpeed # value = <USBSpeed.High: 3>
HostToDevice: ArducamEvkSDK.VRCommandDirection # value = <VRCommandDirection.HostToDevice: 0>
I2C_MODE_16_16: ArducamEvkSDK.I2CMode # value = <I2CMode.I2C_MODE_16_16: 3>
I2C_MODE_16_32: ArducamEvkSDK.I2CMode # value = <I2CMode.I2C_MODE_16_32: 4>
I2C_MODE_16_8: ArducamEvkSDK.I2CMode # value = <I2CMode.I2C_MODE_16_8: 2>
I2C_MODE_8_16: ArducamEvkSDK.I2CMode # value = <I2CMode.I2C_MODE_8_16: 1>
I2C_MODE_8_8: ArducamEvkSDK.I2CMode # value = <I2CMode.I2C_MODE_8_8: 0>
Info: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.Info: 2>
InitCameraFailed: ArducamEvkSDK.ErrorCode # value = <ErrorCode.InitCameraFailed: 769>
JPG: ArducamEvkSDK.FormatMode # value = <FormatMode.JPG: 3>
Low: ArducamEvkSDK.USBSpeed # value = <USBSpeed.Low: 1>
MON: ArducamEvkSDK.FormatMode # value = <FormatMode.MON: 4>
MON_D: ArducamEvkSDK.FormatMode # value = <FormatMode.MON_D: 6>
MemoryAllocateFailed: ArducamEvkSDK.ErrorCode # value = <ErrorCode.MemoryAllocateFailed: 770>
NotSupport: ArducamEvkSDK.ErrorCode # value = <ErrorCode.NotSupport: 61441>
Off: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.Off: 6>
OpenCameraFailed: ArducamEvkSDK.ErrorCode # value = <ErrorCode.OpenCameraFailed: 513>
RAM: ArducamEvkSDK.MemType # value = <MemType.RAM: 2>
RAW: ArducamEvkSDK.FormatMode # value = <FormatMode.RAW: 0>
RAW_D: ArducamEvkSDK.FormatMode # value = <FormatMode.RAW_D: 5>
RGB: ArducamEvkSDK.FormatMode # value = <FormatMode.RGB: 1>
ReadConfigFileFailed: ArducamEvkSDK.ErrorCode # value = <ErrorCode.ReadConfigFileFailed: 257>
RegisterMultipleCallback: ArducamEvkSDK.ErrorCode # value = <ErrorCode.RegisterMultipleCallback: 2049>
STATS: ArducamEvkSDK.FormatMode # value = <FormatMode.STATS: 8>
StateError: ArducamEvkSDK.ErrorCode # value = <ErrorCode.StateError: 32769>
Success: ArducamEvkSDK.ErrorCode # value = <ErrorCode.Success: 0>
Super: ArducamEvkSDK.USBSpeed # value = <USBSpeed.Super: 4>
SuperPlus: ArducamEvkSDK.USBSpeed # value = <USBSpeed.SuperPlus: 5>
Trace: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.Trace: 0>
TransferError: ArducamEvkSDK.EventCode # value = <EventCode.TransferError: 256>
TransferTimeout: ArducamEvkSDK.EventCode # value = <EventCode.TransferTimeout: 257>
USBTypeMismatch: ArducamEvkSDK.ErrorCode # value = <ErrorCode.USBTypeMismatch: 1025>
Unknown: ArducamEvkSDK.USBSpeed # value = <USBSpeed.Unknown: 0>
UnknownDeviceType: ArducamEvkSDK.ErrorCode # value = <ErrorCode.UnknownDeviceType: 515>
UnknownError: ArducamEvkSDK.ErrorCode # value = <ErrorCode.UnknownError: 65535>
UnknownUSBType: ArducamEvkSDK.ErrorCode # value = <ErrorCode.UnknownUSBType: 514>
UserdataAddrError: ArducamEvkSDK.ErrorCode # value = <ErrorCode.UserdataAddrError: 65377>
UserdataLenError: ArducamEvkSDK.ErrorCode # value = <ErrorCode.UserdataLenError: 65378>
VRCommandError: ArducamEvkSDK.ErrorCode # value = <ErrorCode.VRCommandError: 65283>
Warn: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.Warn: 3>
YUV: ArducamEvkSDK.FormatMode # value = <FormatMode.YUV: 2>
__version__ = 'dev'
