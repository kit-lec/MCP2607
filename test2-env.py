import os
import time

from dotenv import load_dotenv
# load_dotenv(환경변수파일경로)
# 매개변수 없이 호출하면 기본적으로 .env 설정파일 읽어옴. 
# 성공적으로 읽어오면 True 리턴.
print(load_dotenv())

print(f'✅ {os.path.basename(__file__)} 실행됨 {time.strftime('%Y-%m-%d %H:%M:%S')}')
print(f'\tOPENAI_API_KEY={os.getenv("OPENAI_API_KEY")[:20]}...')
