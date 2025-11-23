import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.config import config
from app.common.filter import db_session_middleware, tracing_middleware
# 日志初始化要放在路由加载之前，否则会导致系统日志查询功能无法正常显示
from kxy.framework.kxy_logger import KxyLogger
KxyLogger.init_logger(config.LOG_LEVEL,config.AppName,config.ENV_NAME,filename='log/app',file_type='log',backupCount=5,maxBytes=10485760)
from app.system.api import router as system_router
from app.infra.api import router as infra_router
from app.pay.api import router as pay_router
from app.product.api import router as product_router
from app.trade.api import router as trade_router
from app.publish.api import router as publish_router
from app.kxy.api import router as kxy_router
from app.system.services.back_ground_service import BackGroundService
from fastapi.middleware.cors import CORSMiddleware

from app.tools.wx_util import WxUtil

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时执行
    # asyncio.create_task(WxUtil().refresh_token_task())
    asyncio.create_task(BackGroundService.init_system())
    yield
app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)
# 因为默认的fastapi的swagger-ui和redoc接口无法访问，所以需要自定义
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origin_regex=None,
    expose_headers=[],
    max_age=600,
)
app.middleware("http")(tracing_middleware)
app.middleware("http")(db_session_middleware)
app.include_router(system_router)
app.include_router(infra_router)
app.include_router(pay_router)
app.include_router(product_router)
app.include_router(trade_router)
app.include_router(publish_router)
app.include_router(kxy_router)

templates = Jinja2Templates(directory="templates")

@app.get("/websocket-test", response_class=HTMLResponse)
async def websocket_test_page(request: Request):
    return templates.TemplateResponse("websocket_test.html", {"request": request})

if config.ENV_NAME!='production':
    # swagger路由，通过接口端口访问
    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html(request: Request):
        return templates.TemplateResponse(
            "swagger-ui.html",
            {
                "request": request,
                "openapi_url": app.openapi_url,
                "title": app.title + " - Swagger UI",
            },
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)