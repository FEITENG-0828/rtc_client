import pywintypes
import win32pipe
import win32file
import winerror
import struct

class VideoPipe:
    """
    Windows命名管道封装
    用于客户端与服务端之间传输视频数据
    """
    
    def __init__(self, pipe_name : str = "video_pipe", buffer_size : int = 65536):
        """
        初始化命名管道
        :param pipe_name: 管道名称（不要包含完整路径）
        :param buffer_size: 管道缓冲区大小（建议4096的倍数）
        """
        self.pipe_name : str = r"\\.\pipe\{}".format(pipe_name)
        self.buffer_size : int = buffer_size
        self.connected : bool = False
        self.__pipe_handle : pywintypes.HANDLE = None
        self.__initPipe()

    def __initPipe(self):
        """创建并配置命名管道"""
        try:
            # 设置管道参数
            self.__pipe_handle = win32pipe.CreateNamedPipe(
                self.pipe_name,
                win32pipe.PIPE_ACCESS_OUTBOUND,
                win32pipe.PIPE_TYPE_BYTE | win32pipe.PIPE_READMODE_BYTE | win32pipe.PIPE_WAIT,
                1, # 只允许1个实例
                self.buffer_size,
                self.buffer_size,
                0, # 默认超时
                None # 默认安全属性
            )
        except pywintypes.error as e:
            raise RuntimeError(f"创建管道失败: {e.strerror}") from e

    def waitForConnection(self):
        """等待客户端连接"""
        try:
            win32pipe.ConnectNamedPipe(self.__pipe_handle, None)
            self.connected = True
        except pywintypes.error as e:
            if e.winerror != winerror.ERROR_PIPE_CONNECTED:
                raise RuntimeError(f"连接失败: {e.strerror}") from e
            else:
                self.connected = True

    def writeFrame(self, data : bytes):
        """
        写入视频帧数据，自动添加4字节长度头（使用大端序）
        :param data: bytes格式的视频数据
        """
        if not self.connected:
            raise RuntimeError("写入前需要先建立连接")

        try:
            # 添加4字节大端序长度头
            header = struct.pack(">I", len(data))
            total_data = header + data
            
            # 写入完整数据（头部+内容）
            written = 0
            while written < len(total_data):
                _, n = win32file.WriteFile(self.__pipe_handle, total_data[written:])
                written += n
                
            return written
        except pywintypes.error as e:
            self.connected = False
            raise RuntimeError(f"写入失败: {e.strerror}") from e

    def close(self):
        """关闭管道连接"""
        if self.__pipe_handle:
            try:
                if self.connected:
                    win32file.FlushFileBuffers(self.__pipe_handle)
                    win32pipe.DisconnectNamedPipe(self.__pipe_handle)
                win32file.CloseHandle(self.__pipe_handle)
            except pywintypes.error:
                pass
        self.connected = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()
