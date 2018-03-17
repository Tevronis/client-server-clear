
from server import Server

FUNCTIONAL = {"REGISTRATION": Server.user_registration,
              "VERIFICATION": Server.verification,
              "GETSENT": Server.get_mails_sent_id,
              "GETINBOX": Server.get_mails_inbox_id,
              "GETMESSAGE": Server.mail_to_send,
              "DELMESSAGE": Server.delete_message,
              "SETMESSAGE": Server.dump_jsons
              }