from pydantic import BaseModel

class data_platform(common):
    name: str
    url: str
    logo_url: str
    is_oauth_supported: bool
    is_uname_pwd_supported: bool
