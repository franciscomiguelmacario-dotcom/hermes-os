from datetime import datetime


class NotificationCenter:

    def __init__(self, memory, logger=None):
        self.memory = memory
        self.logger = logger

    def all(self):
        return self.memory.get("notifications", [])

    def create(
        self,
        notification_type,
        recipient=None,
        subject=None,
        message=None,
        related_id=None
    ):
        notifications = self.all()

        notification = {
            "id": len(notifications) + 1,
            "created_at": datetime.now().isoformat(),
            "type": notification_type,
            "recipient": recipient,
            "subject": subject,
            "message": message,
            "related_id": related_id,
            "status": "created"
        }

        notifications.append(notification)
        self.memory.set("notifications", notifications)

        return {
            "status": "notification_created",
            "notification": notification
        }

    def order_confirmation(self, order):
        subject = f"Confirmação da encomenda #{order.get('id')}"

        message = (
            f"Olá {order.get('customer_name') or 'cliente'},\n\n"
            f"A tua encomenda foi recebida com sucesso.\n\n"
            f"Produto: {order.get('product_title')}\n"
            f"Quantidade: {order.get('quantity')}\n"
            f"Total: {order.get('total')}€\n\n"
            f"Vamos preparar o envio e avisamos assim que houver tracking.\n\n"
            f"Obrigado pela compra."
        )

        return self.create(
            "order_confirmation",
            order.get("customer_email"),
            subject,
            message,
            order.get("id")
        )

    def shipping_confirmation(self, order):
        subject = f"A tua encomenda #{order.get('id')} foi enviada"

        tracking = order.get("tracking_number") or "tracking em processamento"

        message = (
            f"Olá {order.get('customer_name') or 'cliente'},\n\n"
            f"A tua encomenda já foi enviada.\n\n"
            f"Produto: {order.get('product_title')}\n"
            f"Tracking: {tracking}\n\n"
            f"Podes acompanhar o envio com este código.\n\n"
            f"Obrigado pela compra."
        )

        return self.create(
            "shipping_confirmation",
            order.get("customer_email"),
            subject,
            message,
            order.get("id")
        )

    def campaign_alert(self, campaign, action, reason):
        subject = f"Campanha {campaign.get('id')} - {action}"

        message = (
            f"Campanha: {campaign.get('product_title')}\n"
            f"Ação: {action}\n"
            f"Motivo: {reason}\n"
            f"Estado: {campaign.get('status')}\n"
            f"Budget: {campaign.get('budget')}\n"
        )

        return self.create(
            "campaign_alert",
            "admin",
            subject,
            message,
            campaign.get("id")
        )

    def mark_sent(self, notification_id):
        notifications = self.all()

        for notification in notifications:
            if notification["id"] == int(notification_id):
                notification["status"] = "sent"
                notification["sent_at"] = datetime.now().isoformat()

                self.memory.set("notifications", notifications)

                return {
                    "status": "notification_sent",
                    "notification": notification
                }

        return {
            "status": "error",
            "message": "notification not found"
        }

    def pending(self):
        return [
            notification for notification in self.all()
            if notification.get("status") == "created"
        ]

    def send_pending(self):
        results = []

        for notification in self.pending():
            results.append(
                self.mark_sent(notification["id"])
            )

        batch = {
            "created_at": datetime.now().isoformat(),
            "sent": len(results),
            "results": results
        }

        history = self.memory.get("notification_batches", [])
        history.append(batch)
        self.memory.set("notification_batches", history)

        return {
            "status": "notifications_processed",
            "sent": len(results),
            "batch": batch
        }

    def batches(self):
        return self.memory.get("notification_batches", [])
