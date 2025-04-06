import os
from dataclasses import dataclass

@dataclass
class Config:
    liqpay_pub_key: str
    liqpay_private_key: str
    mqtt_host: str
    mqtt_port: int
    mqtt_username: str
    mqtt_password: str
    base_url: str
    liqpay_sandbox: int = 0
    
    @staticmethod
    def from_env() -> "Config":
        from dotenv import load_dotenv
        load_dotenv()
        
        return Config(
            liqpay_pub_key=os.getenv("LIQPAY_PUBLIC_KEY"), # type: ignore
            liqpay_private_key=os.getenv("LIQPAY_PRIVATE_KEY"), # type: ignore
            mqtt_host=os.getenv("MQTT_HOST"), # type: ignore
            mqtt_port=int(os.getenv("MQTT_PORT")), # type: ignore
            mqtt_username=os.getenv("MQTT_USERNAME"), # type: ignore
            mqtt_password=os.getenv("MQTT_PASSWORD"), # type: ignore
            base_url=os.getenv("BASE_URL"), # type: ignore
        )
        
        
config = Config.from_env()