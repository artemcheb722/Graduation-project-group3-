from fastapi import FastAPI

from applications.users.router import router_users
from applications.Restaurants.router import router_restaurants



def get_application() -> FastAPI:
    app = FastAPI(root_path="/api", root_path_in_servers=True)
    app.include_router(router_users, prefix="/users", tags=["Users"])
    app.include_router(router_restaurants, prefix="/restaurants", tags=["Restaurants"])  # ✅
    return app