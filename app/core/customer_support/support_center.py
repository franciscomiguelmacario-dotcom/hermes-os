from datetime import datetime


class SupportCenter:

    def __init__(self, order_manager, notifications, memory, logger=None):
        self.order_manager = order_manager
        self.notifications = notifications
        self.memory = memory
        self.logger = logger

    def all(self):
        return self.memory.get("support_tickets", [])

    def pending(self):
        return [
            ticket for ticket in self.all()
            if ticket.get("status") == "open"
        ]

    def get_ticket(self, ticket_id):
        for ticket in self.all():
            if ticket["id"] == int(ticket_id):
                return ticket

        return None

    def create_ticket(
        self,
        customer_email=None,
        subject=None,
        message=None,
        order_id=None
    ):
        tickets = self.all()

        ticket = {
            "id": len(tickets) + 1,
            "created_at": datetime.now().isoformat(),
            "customer_email": customer_email,
            "subject": subject or "Pedido de suporte",
            "message": message,
            "order_id": int(order_id) if order_id else None,
            "status": "open",
            "replies": []
        }

        tickets.append(ticket)
        self.memory.set("support_tickets", tickets)

        return {
            "status": "support_ticket_created",
            "ticket": ticket
        }

    def reply_ticket(self, ticket_id, message):
        tickets = self.all()

        for ticket in tickets:
            if ticket["id"] == int(ticket_id):
                reply = {
                    "created_at": datetime.now().isoformat(),
                    "message": message,
                    "from": "Hermes"
                }

                ticket["replies"].append(reply)
                ticket["last_reply_at"] = reply["created_at"]
                self.memory.set("support_tickets", tickets)

                self.notifications.create(
                    "support_reply",
                    ticket.get("customer_email"),
                    f"Resposta ao teu pedido #{ticket['id']}",
                    message,
                    ticket["id"]
                )

                return {
                    "status": "support_ticket_replied",
                    "ticket": ticket
                }

        return {
            "status": "error",
            "message": "support ticket not found"
        }

    def close_ticket(self, ticket_id):
        tickets = self.all()

        for ticket in tickets:
            if ticket["id"] == int(ticket_id):
                ticket["status"] = "closed"
                ticket["closed_at"] = datetime.now().isoformat()
                self.memory.set("support_tickets", tickets)

                return {
                    "status": "support_ticket_closed",
                    "ticket": ticket
                }

        return {
            "status": "error",
            "message": "support ticket not found"
        }

    def auto_reply(self, ticket_id):
        ticket = self.get_ticket(ticket_id)

        if not ticket:
            return {
                "status": "error",
                "message": "support ticket not found"
            }

        order_id = ticket.get("order_id")
        order = None

        if order_id:
            order = self.order_manager.get_order(order_id)

        if order:
            reply = self.build_order_reply(ticket, order)
        else:
            reply = self.build_general_reply(ticket)

        return self.reply_ticket(ticket_id, reply)

    def auto_reply_all(self):
        results = []

        for ticket in self.pending():
            results.append(
                self.auto_reply(ticket["id"])
            )

        batch = {
            "created_at": datetime.now().isoformat(),
            "tickets_processed": len(results),
            "results": results
        }

        history = self.memory.get("support_auto_reply_batches", [])
        history.append(batch)
        self.memory.set("support_auto_reply_batches", history)

        return {
            "status": "support_auto_reply_finished",
            "tickets_processed": len(results),
            "batch": batch
        }

    def build_order_reply(self, ticket, order):
        fulfillment_status = order.get("fulfillment_status")
        tracking = order.get("tracking_number")

        if fulfillment_status == "fulfilled":
            return (
                f"Olá,\n\n"
                f"A tua encomenda #{order.get('id')} já foi enviada.\n"
                f"Produto: {order.get('product_title')}\n"
                f"Tracking: {tracking or 'em processamento'}\n\n"
                f"Obrigado pela tua compra."
            )

        return (
            f"Olá,\n\n"
            f"A tua encomenda #{order.get('id')} foi recebida e está em preparação.\n"
            f"Produto: {order.get('product_title')}\n"
            f"Estado: {fulfillment_status}\n\n"
            f"Vamos avisar assim que for enviada."
        )

    def build_general_reply(self, ticket):
        return (
            f"Olá,\n\n"
            f"Recebemos o teu pedido de suporte: {ticket.get('subject')}.\n"
            f"A nossa equipa vai analisar e responder o mais rápido possível.\n\n"
            f"Obrigado pelo contacto."
        )

    def batches(self):
        return self.memory.get("support_auto_reply_batches", [])
