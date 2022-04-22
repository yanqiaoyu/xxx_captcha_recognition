from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v2.captchaRecog import captchaRecogRouter
import sys
import os
import uvicorn

# 把根目录添加进系统目录
sys.path.append(os.pardir)

app = FastAPI()

# 处理跨域请求
app.add_middleware(
    CORSMiddleware,
    # 允许所有的源进行请求
    allow_origins=["*"],
    allow_credentials=True,
    # 允许所有的请求方法
    allow_methods=["*"],
    # 允许所有的请求头
    allow_headers=["*"],
)

# 处理路由
app.include_router(captchaRecogRouter)


def main():

    uvicorn.run(app="run:app",
                host='0.0.0.0',
                port=3579,
                reload=True,
                debug=True)


if __name__ == '__main__':
    main()
