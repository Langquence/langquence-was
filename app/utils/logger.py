import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'RESET': '\033[0m'        # Reset to default
    }
    
    def format(self, record):
        format_orig = self._style._fmt
        
        if record.levelname in self.COLORS:
            color = self.COLORS[record.levelname]
            record.levelname = f"{color}{record.levelname}{self.COLORS['RESET']}"
            
        result = super().format(record)
        
        self._style._fmt = format_orig
        
        return result

# 기본 설정 함수
def setup_logger():
    # 로그 디렉토리 생성
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    formatter = ColoredFormatter('%(asctime)s - [PID:%(process)d/TID:%(thread)d] - %(name)s - %(levelname)s - %(message)s')

    # 콘솔 출력용 핸들러
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)

    # 현재 날짜로 로그 파일 이름 생성
    current_date = datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(log_dir, f'app_{current_date}.log')

    # 날짜별 로그 파일 핸들러
    file_handler = TimedRotatingFileHandler(
        log_file,
        when='midnight',
        interval=1,
        backupCount=30,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    file_handler.suffix = '%Y-%m-%d'

    # 루트 로거 설정
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # 이미 핸들러가 있는 경우 제거
    if root_logger.handlers:
        root_logger.handlers = []
        
    root_logger.addHandler(stream_handler)
    root_logger.addHandler(file_handler)

# 초기 설정 실행
setup_logger()

# 모듈별 로거를 가져오는 함수
def get_logger(name):
    return logging.getLogger(name)