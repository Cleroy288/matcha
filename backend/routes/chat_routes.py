from flask import Blueprint

from controllers.chat_controller import conversation_messages, conversations, post_message, unread_messages

chat_routes = Blueprint("chat", __name__)

# Chat entre users "connectés" (match mutuel)
chat_routes.route("/chat/conversations",            methods=["GET"])(conversations)
chat_routes.route("/chat/messages/<int:user_id>",   methods=["GET"])(conversation_messages)
chat_routes.route("/chat/messages/<int:user_id>",   methods=["POST"])(post_message)
chat_routes.route("/chat/unread",                   methods=["GET"])(unread_messages)
