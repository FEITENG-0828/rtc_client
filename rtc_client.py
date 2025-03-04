import numpy as np
import cv2
import asyncio
from uuv_webrtc import RtcClient
from video_pipe import VideoPipe

import os, sys
import logging

import argparse

import threading

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--local_port", type=int, default=20001,
                    metavar='', help="本地端口")
parser.add_argument("-s", "--server_host", type=str, default="127.0.0.1",
                    metavar='', help="服务器IP地址")
parser.add_argument("-p", "--server_port", type=int, default=20000,
                    metavar='', help="服务器端口")
parser.add_argument("-n", "--pipe_name", type=str, default="video_pipe",
                    metavar='', help="管道名称")
parser.add_argument("-q", "--jpg_quality", type=int, default=80,
                    metavar='', help="管道传输的JPG质量")
parser.add_argument("-o", "--log_path", type=str, default="./rtc_client.log",
                    metavar='', help="日志文件路径")
args = parser.parse_args()

os.makedirs(os.path.dirname(args.log_path), exist_ok=True)

rtc_client_logger = logging.getLogger("RtcClient")
rtc_client_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(
    filename=os.path.abspath(args.log_path), mode='a', encoding="utf-8")
file_handler.setFormatter(
    logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s] %(message)s"))
rtc_client_logger.addHandler(file_handler)

def pollingCloseSignal(client : RtcClient, pipe : VideoPipe):
    while True:
        input_str = sys.stdin.readline()
        if "close" in input_str.lower():
            rtc_client_logger.info("收到close信号")
            asyncio.run(client.close())
            pipe.close()
            break

if __name__ == "__main__":
    rtc_client_logger.info("客户端将启动")
    with RtcClient(
        local_port=args.local_port,
        server_address=(args.server_host, args.server_port),
        logger=rtc_client_logger
    ) as client:
        try:
            with VideoPipe(pipe_name=args.pipe_name) as pipe:
                monitor_thread = threading.Thread(target=pollingCloseSignal,
                                                args=(client, pipe),
                                                daemon=True)
                monitor_thread.start()

                rtc_client_logger.info("等待管道连接...")
                sys.stdout.write("pipe_ready\n")
                sys.stdout.flush()
                pipe.waitForConnection()
                rtc_client_logger.info("管道连接成功")

                success : bool = False
                frame : np.ndarray = None
                jpeg_data : bytes = None
                while pipe.connected:
                    success, frame = client.getLatestFrame()
                    if not success:
                        frame = np.zeros((720, 1080, 3), dtype=np.uint8)
                    _, jpeg_data = cv2.imencode(".jpg", frame,
                        [cv2.IMWRITE_JPEG_QUALITY, args.jpg_quality])
                    pipe.writeFrame(jpeg_data.tobytes())

        except Exception as e:
            rtc_client_logger.exception(f"发生错误: {e}")
        finally:
            rtc_client_logger.info("客户端将退出")
