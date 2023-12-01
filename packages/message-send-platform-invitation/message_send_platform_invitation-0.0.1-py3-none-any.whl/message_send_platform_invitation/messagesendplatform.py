from dotenv import load_dotenv

from circles_local_database_python.connector import Connector
from circles_local_database_python.generic_crud import GenericCRUD
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from queue_local.database_queue import DatabaseQueue

load_dotenv()

MESSAGE_SEND_PLATFORM_INVITATION_LOCAL_PYTHON_COMPONENT_ID = 243
MESSAGE_SEND_PLATFORM_INVITATION_LOCAL_PYTHON_COMPONENT_COMPONENT_NAME = "message-send-platform-invitation-local-python"
DEVELOPER_EMAIL = 'jenya.b@circ.zone'
object1 = {
    'component_id': MESSAGE_SEND_PLATFORM_INVITATION_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': MESSAGE_SEND_PLATFORM_INVITATION_LOCAL_PYTHON_COMPONENT_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
logger=Logger.create_logger(object=object1)

class MessageSendPlatform(GenericCRUD):
    def __init__(self,schema_name, connection: Connector = None,) -> None:
        pass

    def get_potential_person_list_by_campaign_id(self, campaign_id) -> list:
        logger.start()
        query = (
            f"SELECT * FROM criteria_table"
            f"JOIN campaign_table ON campaign_table.{campaign_id} = criteria_table.criteria_id"
            f"JOIN person.person_table ON TIMESTAMPDIFF(YEAR, person.person_table.birthday_date, CURDATE()) BETWEEN"
            f"(criteria.criteria_table.min_age AND criteria.criteria_table.max_age)"
        )
        self.schema_name = "criteria"
        self.cursor.execute(query)
        self.connection.commit()
        potential_person =  self.cursor.fetchall()
        logger.end()
        return potential_person


    def get_number_of_invitations_sent_in_the_last_24_hours(self,message_id) -> int:
        logger.start()
        query = (
            f"SELECT COUNT(*) FROM message_sent_view"
            f"WHERE message_id = {message_id} AND actual_send_timestamp >= NOW() - INTERVAL 24 HOUR"
        )
        self.schema_name = "message"
        self.cursor.execute(query)
        self.connection.commit()
        number_of_invitations =  self.cursor.fetchall()
        logger.end()
        return number_of_invitations


    def get_number_of_invitations_to_send(self,message_id) -> int:
        logger.start()
        multiplier = 0.1
        invitations_sent_in_the_last_24_hours = self.get_number_of_invitations_sent_in_the_last_24_hours(message_id)
        logger.end()
        return invitations_sent_in_the_last_24_hours * multiplier


    def send_invitations( potential_person_list, number_of_invitations_to_send, message_template_id ):
        logger.start()
        for person in potential_person_list:
            DatabaseQueue().push({
                "person_id": person,
                "message_template_id": message_template_id
            })

