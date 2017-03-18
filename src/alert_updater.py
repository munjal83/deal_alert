
from src.common.database import Database
from src.models.alerts.alert import Alert


Database.initialize()

finding_need_alert = Alert.find_update_alert()

for alert in finding_need_alert:
    alert.load_item_price()
    alert.send_email_if_price_reached()