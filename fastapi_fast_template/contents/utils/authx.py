from authx import AuthX, AuthXConfig

authx_config = AuthXConfig(
    JWT_ALGORITHM="HS256",
    JWT_SECRET_KEY="SECRET_KEY",
    JWT_TOKEN_LOCATION=["headers"],
)
auth = AuthX(config=authx_config)
