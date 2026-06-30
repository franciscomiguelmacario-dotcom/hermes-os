import json
import threading
import time

from flask import Flask, jsonify, redirect, render_template_string, request, url_for

from app.core.startup import Hermes


PAGE = """
<!doctype html>
<html lang="pt">
<head>
    <meta charset="utf-8">
    <title>Hermes OS // Command Center</title>

    <style>
        :root {
            --bg: #030712;
            --panel: rgba(15, 23, 42, 0.72);
            --panel-strong: rgba(15, 23, 42, 0.95);
            --border: rgba(56, 189, 248, 0.28);
            --border-soft: rgba(148, 163, 184, 0.18);
            --cyan: #22d3ee;
            --blue: #3b82f6;
            --purple: #8b5cf6;
            --green: #22c55e;
            --yellow: #eab308;
            --red: #ef4444;
            --text: #e5e7eb;
            --muted: #94a3b8;
            --dark: #020617;
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            font-family: Arial, Helvetica, sans-serif;
            color: var(--text);
            background:
                radial-gradient(circle at 20% 20%, rgba(34, 211, 238, 0.20), transparent 28%),
                radial-gradient(circle at 80% 10%, rgba(139, 92, 246, 0.18), transparent 30%),
                radial-gradient(circle at 50% 90%, rgba(59, 130, 246, 0.12), transparent 35%),
                linear-gradient(135deg, #020617 0%, #030712 45%, #0f172a 100%);
            overflow-x: hidden;
        }

        body::before {
            content: "";
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(rgba(34, 211, 238, 0.04) 1px, transparent 1px),
                linear-gradient(90deg, rgba(34, 211, 238, 0.04) 1px, transparent 1px);
            background-size: 42px 42px;
            mask-image: linear-gradient(to bottom, black, transparent 85%);
            pointer-events: none;
        }

        body::after {
            content: "";
            position: fixed;
            inset: 0;
            background: linear-gradient(
                115deg,
                transparent 0%,
                rgba(34, 211, 238, 0.04) 45%,
                transparent 55%
            );
            animation: scan 8s linear infinite;
            pointer-events: none;
        }

        @keyframes scan {
            0% { transform: translateX(-80%); }
            100% { transform: translateX(80%); }
        }

        .shell {
            width: min(1500px, calc(100% - 32px));
            margin: 0 auto;
            padding: 22px 0 40px;
            position: relative;
            z-index: 1;
        }

        .topbar {
            display: flex;
            justify-content: space-between;
            gap: 18px;
            align-items: center;
            padding: 18px;
            border: 1px solid var(--border);
            border-radius: 24px;
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.82), rgba(2, 6, 23, 0.82));
            box-shadow:
                0 0 40px rgba(34, 211, 238, 0.10),
                inset 0 0 30px rgba(59, 130, 246, 0.05);
            backdrop-filter: blur(18px);
        }

        .brand {
            display: flex;
            gap: 14px;
            align-items: center;
        }

        .orb {
            width: 54px;
            height: 54px;
            border-radius: 50%;
            background:
                radial-gradient(circle at 35% 30%, white, var(--cyan) 16%, var(--blue) 42%, transparent 66%),
                radial-gradient(circle, rgba(34, 211, 238, 0.2), transparent);
            box-shadow:
                0 0 18px rgba(34, 211, 238, 0.95),
                0 0 42px rgba(59, 130, 246, 0.45);
            animation: pulse 2.4s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); filter: brightness(1); }
            50% { transform: scale(1.06); filter: brightness(1.25); }
        }

        h1 {
            margin: 0;
            font-size: 30px;
            letter-spacing: 2px;
            text-transform: uppercase;
        }

        .subtitle {
            color: var(--muted);
            margin-top: 5px;
            font-size: 14px;
            letter-spacing: 0.8px;
        }

        .system-status {
            text-align: right;
            min-width: 260px;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 9px 12px;
            border: 1px solid rgba(34, 197, 94, 0.5);
            border-radius: 999px;
            color: #bbf7d0;
            background: rgba(22, 163, 74, 0.12);
            box-shadow: 0 0 18px rgba(34, 197, 94, 0.18);
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .dot {
            width: 9px;
            height: 9px;
            border-radius: 50%;
            background: var(--green);
            box-shadow: 0 0 12px var(--green);
        }

        .timestamp {
            margin-top: 8px;
            color: var(--muted);
            font-size: 12px;
        }

        .hero {
            display: grid;
            grid-template-columns: 1.2fr 0.8fr;
            gap: 18px;
            margin-top: 18px;
        }

        .panel {
            border: 1px solid var(--border-soft);
            border-radius: 24px;
            background: var(--panel);
            backdrop-filter: blur(16px);
            box-shadow:
                0 0 30px rgba(2, 6, 23, 0.40),
                inset 0 0 24px rgba(34, 211, 238, 0.03);
            overflow: hidden;
        }

        .panel-header {
            padding: 16px 18px;
            border-bottom: 1px solid var(--border-soft);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: linear-gradient(90deg, rgba(34, 211, 238, 0.08), transparent);
        }

        .panel-title {
            margin: 0;
            font-size: 16px;
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        .panel-body {
            padding: 18px;
        }

        .money-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
        }

        .money-card {
            padding: 18px;
            border: 1px solid rgba(34, 211, 238, 0.20);
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(2, 6, 23, 0.78), rgba(15, 23, 42, 0.70));
        }

        .money-label {
            color: var(--muted);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1.2px;
        }

        .money-value {
            margin-top: 10px;
            font-size: 30px;
            font-weight: 800;
        }

        .green { color: var(--green); }
        .cyan { color: var(--cyan); }
        .yellow { color: var(--yellow); }
        .red { color: var(--red); }
        .purple { color: #c4b5fd; }

        .grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
            margin-top: 18px;
        }

        .metric-card {
            padding: 18px;
            border-radius: 20px;
            border: 1px solid var(--border-soft);
            background:
                linear-gradient(135deg, rgba(15, 23, 42, 0.78), rgba(2, 6, 23, 0.88)),
                radial-gradient(circle at top right, rgba(34, 211, 238, 0.12), transparent 36%);
            position: relative;
            overflow: hidden;
        }

        .metric-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 12px;
            right: 12px;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--cyan), transparent);
        }

        .metric-title {
            color: var(--muted);
            font-size: 12px;
            letter-spacing: 1.2px;
            text-transform: uppercase;
        }

        .metric-value {
            font-size: 34px;
            font-weight: 800;
            margin-top: 8px;
        }

        .metric-sub {
            color: var(--muted);
            font-size: 13px;
            margin-top: 6px;
        }

        .layout {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 18px;
            margin-top: 18px;
        }

        .actions-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 14px;
        }

        form {
            border: 1px solid var(--border-soft);
            border-radius: 18px;
            padding: 14px;
            background: rgba(2, 6, 23, 0.45);
        }

        form h3 {
            margin: 0 0 10px;
            font-size: 13px;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: var(--cyan);
        }

        input {
            width: 100%;
            margin-bottom: 8px;
            padding: 11px 12px;
            color: var(--text);
            border: 1px solid rgba(148, 163, 184, 0.26);
            border-radius: 12px;
            background: rgba(2, 6, 23, 0.74);
            outline: none;
        }

        input:focus {
            border-color: rgba(34, 211, 238, 0.70);
            box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.10);
        }

        button {
            width: 100%;
            border: 0;
            border-radius: 12px;
            padding: 11px 14px;
            color: white;
            cursor: pointer;
            font-weight: 700;
            letter-spacing: 0.5px;
            background: linear-gradient(135deg, var(--blue), var(--purple));
            box-shadow: 0 0 18px rgba(59, 130, 246, 0.24);
        }

        button:hover {
            filter: brightness(1.15);
            transform: translateY(-1px);
        }

        .mini-list {
            display: grid;
            gap: 10px;
        }

        .list-item {
            padding: 12px;
            border: 1px solid var(--border-soft);
            border-radius: 14px;
            background: rgba(2, 6, 23, 0.48);
        }

        .list-item strong {
            color: white;
        }

        .list-item span {
            display: block;
            color: var(--muted);
            font-size: 13px;
            margin-top: 4px;
        }

        .alert {
            padding: 12px;
            border-radius: 14px;
            border: 1px solid var(--border-soft);
            background: rgba(2, 6, 23, 0.48);
            margin-bottom: 10px;
        }

        .alert.ok {
            border-color: rgba(34, 197, 94, 0.35);
            color: #bbf7d0;
        }

        .alert.warning {
            border-color: rgba(234, 179, 8, 0.38);
            color: #fef08a;
        }

        .alert.danger {
            border-color: rgba(239, 68, 68, 0.38);
            color: #fecaca;
        }

        .alert.info {
            border-color: rgba(34, 211, 238, 0.35);
            color: #a5f3fc;
        }

        .terminal {
            border-radius: 18px;
            border: 1px solid rgba(34, 211, 238, 0.22);
            background: rgba(2, 6, 23, 0.80);
            overflow: hidden;
        }

        .terminal-top {
            padding: 10px 12px;
            border-bottom: 1px solid var(--border-soft);
            color: var(--muted);
            font-size: 12px;
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        pre {
            margin: 0;
            padding: 16px;
            max-height: 520px;
            overflow: auto;
            color: #bfdbfe;
            font-size: 12px;
            line-height: 1.5;
        }

        .links {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        .link-chip {
            display: inline-flex;
            padding: 9px 12px;
            border-radius: 999px;
            border: 1px solid rgba(34, 211, 238, 0.28);
            color: #a5f3fc;
            text-decoration: none;
            background: rgba(2, 6, 23, 0.44);
            font-size: 13px;
        }

        .link-chip:hover {
            background: rgba(34, 211, 238, 0.12);
        }

        .wide {
            grid-column: 1 / -1;
        }

        @media (max-width: 1100px) {
            .hero,
            .layout {
                grid-template-columns: 1fr;
            }

            .money-grid,
            .grid {
                grid-template-columns: repeat(2, 1fr);
            }

            .actions-grid {
                grid-template-columns: 1fr;
            }

            .topbar {
                flex-direction: column;
                align-items: flex-start;
            }

            .system-status {
                text-align: left;
            }
        }

        @media (max-width: 640px) {
            .money-grid,
            .grid {
                grid-template-columns: 1fr;
            }

            h1 {
                font-size: 22px;
            }
        }
    </style>
</head>

<body>
    <div class="shell">
        <section class="topbar">
            <div class="brand">
                <div class="orb"></div>
                <div>
                    <h1>Hermes OS</h1>
                    <div class="subtitle">Autonomous Dropshipping Command Center</div>
                </div>
            </div>

            <div class="system-status">
                <div class="status-pill">
                    <span class="dot"></span>
                    Sistema operacional
                </div>
                <div class="timestamp">{{ data.get("generated_at") }}</div>
            </div>
        </section>

        <section class="hero">
            <div class="panel">
                <div class="panel-header">
                    <h2 class="panel-title">Finance Core</h2>
                    <span class="small">Receita / Custos / Lucro</span>
                </div>

                <div class="panel-body">
                    <div class="money-grid">
                        <div class="money-card">
                            <div class="money-label">Receita</div>
                            <div class="money-value cyan">{{ money.get("revenue", 0) }}€</div>
                        </div>

                        <div class="money-card">
                            <div class="money-label">Custos</div>
                            <div class="money-value yellow">{{ money.get("costs", 0) }}€</div>
                        </div>

                        <div class="money-card">
                            <div class="money-label">Lucro</div>
                            <div class="money-value {% if money.get('profit', 0) < 0 %}red{% else %}green{% endif %}">
                                {{ money.get("profit", 0) }}€
                            </div>
                        </div>

                        <div class="money-card">
                            <div class="money-label">Ticket médio</div>
                            <div class="money-value purple">{{ money.get("average_order_value", 0) }}€</div>
                        </div>
                    </div>

                    <div class="grid">
                        <div class="metric-card">
                            <div class="metric-title">Produtos</div>
                            <div class="metric-value">{{ summary.get("products", 0) }}</div>
                            <div class="metric-sub">Ativos: {{ summary.get("active_products", 0) }}</div>
                        </div>

                        <div class="metric-card">
                            <div class="metric-title">Encomendas</div>
                            <div class="metric-value">{{ summary.get("orders", 0) }}</div>
                            <div class="metric-sub">Pendentes: {{ summary.get("pending_orders", 0) }}</div>
                        </div>

                        <div class="metric-card">
                            <div class="metric-title">Campanhas</div>
                            <div class="metric-value">{{ summary.get("campaigns", 0) }}</div>
                            <div class="metric-sub">Ativas: {{ summary.get("active_campaigns", 0) }}</div>
                        </div>

                        <div class="metric-card">
                            <div class="metric-title">Autopilot</div>
                            <div class="metric-value">{{ autopilot.get("cycles_count", 0) }}</div>
                            <div class="metric-sub">Ciclos executados</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="panel">
                <div class="panel-header">
                    <h2 class="panel-title">Mission Alerts</h2>
                    <span class="small">Estado atual</span>
                </div>

                <div class="panel-body">
                    {% for alert in alerts %}
                        <div class="alert {{ alert.get('level') }}">
                            {{ alert.get("message") }}
                        </div>
                    {% endfor %}

                    <div style="height: 12px;"></div>

                    <div class="mini-list">
                        {% for action in actions %}
                            <div class="list-item">
                                <strong>Próxima ação</strong>
                                <span>{{ action }}</span>
                            </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </section>

        <section class="grid">
            <div class="metric-card">
                <div class="metric-title">Fornecedor</div>
                <div class="metric-value">{{ summary.get("supplier_products", 0) }}</div>
                <div class="metric-sub">Produtos disponíveis</div>
            </div>

            <div class="metric-card">
                <div class="metric-title">Notificações</div>
                <div class="metric-value">{{ summary.get("notifications", 0) }}</div>
                <div class="metric-sub">Pendentes: {{ summary.get("pending_notifications", 0) }}</div>
            </div>

            <div class="metric-card">
                <div class="metric-title">Suporte</div>
                <div class="metric-value">{{ summary.get("support_tickets", 0) }}</div>
                <div class="metric-sub">Abertos: {{ summary.get("pending_support", 0) }}</div>
            </div>

            <div class="metric-card">
                <div class="metric-title">Fulfillment</div>
                <div class="metric-value">{{ summary.get("fulfilled_orders", 0) }}</div>
                <div class="metric-sub">Encomendas enviadas</div>
            </div>
        </section>

        <section class="layout">
            <div class="panel">
                <div class="panel-header">
                    <h2 class="panel-title">Quick Actions</h2>
                    <span class="small">Controlos operacionais</span>
                </div>

                <div class="panel-body">
                    <div class="actions-grid">
                        <form method="post" action="/action/store-autopilot">
                            <h3>Executar Store Autopilot</h3>
                            <input name="margin" placeholder="Margem %" value="40">
                            <input name="budget" placeholder="Budget" value="10">
                            <input name="channel" placeholder="Canal" value="facebook_ads">
                            <input name="tracking_prefix" placeholder="Tracking prefix" value="HER">
                            <button type="submit">Iniciar ciclo autónomo</button>
                        </form>

                        <form method="post" action="/action/add-supplier-product">
                            <h3>Adicionar produto fornecedor</h3>
                            <input name="title" placeholder="Produto fornecedor" value="Relógio inteligente">
                            <input name="cost" placeholder="Custo" value="12.50">
                            <input name="shipping_days" placeholder="Dias envio" value="8">
                            <input name="supplier_url" placeholder="URL fornecedor" value="https://fornecedor.local/produto">
                            <input name="category" placeholder="Categoria" value="gadgets">
                            <button type="submit">Adicionar produto</button>
                        </form>

                        <form method="post" action="/action/create-order">
                            <h3>Criar encomenda teste</h3>
                            <input name="product_id" placeholder="ID produto" value="1">
                            <input name="customer_name" placeholder="Nome cliente" value="Francisco">
                            <input name="customer_email" placeholder="Email cliente" value="teste@email.com">
                            <input name="quantity" placeholder="Quantidade" value="1">
                            <button type="submit">Criar encomenda</button>
                        </form>

                        <form method="post" action="/action/create-support-ticket">
                            <h3>Criar ticket suporte</h3>
                            <input name="email" placeholder="Email cliente" value="teste@email.com">
                            <input name="subject" placeholder="Assunto" value="Onde está a encomenda?">
                            <input name="message" placeholder="Mensagem" value="Quero saber o tracking">
                            <input name="order_id" placeholder="ID encomenda" value="1">
                            <button type="submit">Criar ticket</button>
                        </form>

                        <form method="post" action="/action/send-notifications">
                            <h3>Comunicações</h3>
                            <button type="submit">Enviar notificações pendentes</button>
                        </form>

                        <form method="post" action="/action/auto-reply-support">
                            <h3>Suporte IA</h3>
                            <button type="submit">Responder suporte automaticamente</button>
                        </form>

                        <form method="post" action="/action/optimize-campaigns">
                            <h3>Marketing</h3>
                            <button type="submit">Otimizar campanhas</button>
                        </form>

                        <form method="post" action="/action/simulate-campaigns">
                            <h3>Simulação</h3>
                            <button type="submit">Simular campanhas ativas</button>
                        </form>
                    </div>
                </div>
            </div>

            <div class="panel">
                <div class="panel-header">
                    <h2 class="panel-title">System Links</h2>
                    <span class="small">APIs internas</span>
                </div>

                <div class="panel-body">
                    <div class="links">
                        <a class="link-chip" href="/api/dashboard" target="_blank">Dashboard JSON</a>
                        <a class="link-chip" href="/api/products" target="_blank">Produtos</a>
                        <a class="link-chip" href="/api/orders" target="_blank">Encomendas</a>
                        <a class="link-chip" href="/api/campaigns" target="_blank">Campanhas</a>
                        <a class="link-chip" href="/api/notifications" target="_blank">Notificações</a>
                        <a class="link-chip" href="/api/support" target="_blank">Suporte</a>
                    </div>

                    <div style="height: 18px;"></div>

                    <div class="terminal">
                        <div class="terminal-top">Autopilot Config</div>
                        <pre>{{ autopilot_config }}</pre>
                    </div>
                </div>
            </div>
        </section>

        <section class="panel wide" style="margin-top: 18px;">
            <div class="panel-header">
                <h2 class="panel-title">Hermes Raw Telemetry</h2>
                <span class="small">Dados completos do sistema</span>
            </div>

            <div class="panel-body">
                <div class="terminal">
                    <div class="terminal-top">Live System Snapshot</div>
                    <pre>{{ raw }}</pre>
                </div>
            </div>
        </section>
    </div>
</body>
</html>
"""


def create_app():
    app = Flask(__name__)

    hermes = Hermes()
    hermes.kernel.boot()

    running = {"enabled": True}

    def background_loop():
        while running["enabled"]:
            try:
                hermes.kernel.run_tick()
            except Exception as error:
                hermes.logger.info(f"Dashboard runtime error: {error}")

            time.sleep(1)

    thread = threading.Thread(target=background_loop, daemon=True)
    thread.start()

    app.config["HERMES"] = hermes
    app.config["RUNNING"] = running

    def brain():
        return app.config["HERMES"].brain

    def json_text(value):
        return json.dumps(value, indent=2, ensure_ascii=False)

    @app.route("/", methods=["GET"])
    def index():
        data = brain().dashboard_data()

        return render_template_string(
            PAGE,
            data=data,
            summary=data.get("summary", {}),
            money=data.get("money", {}),
            alerts=data.get("alerts", []),
            actions=data.get("next_recommended_actions", []),
            autopilot=data.get("autopilot", {}),
            autopilot_config=json_text(
                data.get("autopilot", {}).get("config", {})
            ),
            raw=json_text(data)
        )

    @app.route("/api/dashboard", methods=["GET"])
    def api_dashboard():
        return jsonify(brain().dashboard_data())

    @app.route("/api/products", methods=["GET"])
    def api_products():
        return jsonify(brain().store_products())

    @app.route("/api/orders", methods=["GET"])
    def api_orders():
        return jsonify(brain().orders_all())

    @app.route("/api/campaigns", methods=["GET"])
    def api_campaigns():
        return jsonify(brain().campaigns_all())

    @app.route("/api/notifications", methods=["GET"])
    def api_notifications():
        return jsonify(brain().notifications_all())

    @app.route("/api/support", methods=["GET"])
    def api_support():
        return jsonify(brain().support_tickets())

    @app.route("/action/store-autopilot", methods=["POST"])
    def action_store_autopilot():
        brain().run_store_autopilot(
            request.form.get("margin", 40),
            request.form.get("budget", 10),
            request.form.get("channel", "facebook_ads"),
            request.form.get("tracking_prefix", "HER")
        )

        return redirect(url_for("index"))

    @app.route("/action/add-supplier-product", methods=["POST"])
    def action_add_supplier_product():
        brain().add_supplier_product(
            request.form.get("title"),
            request.form.get("cost"),
            request.form.get("shipping_days"),
            request.form.get("supplier_url"),
            request.form.get("category")
        )

        return redirect(url_for("index"))

    @app.route("/action/create-order", methods=["POST"])
    def action_create_order():
        brain().create_order(
            request.form.get("product_id"),
            request.form.get("customer_name"),
            request.form.get("customer_email"),
            request.form.get("quantity", 1)
        )

        return redirect(url_for("index"))

    @app.route("/action/create-support-ticket", methods=["POST"])
    def action_create_support_ticket():
        brain().create_support_ticket(
            request.form.get("email"),
            request.form.get("subject"),
            request.form.get("message"),
            request.form.get("order_id")
        )

        return redirect(url_for("index"))

    @app.route("/action/send-notifications", methods=["POST"])
    def action_send_notifications():
        brain().send_notifications()
        return redirect(url_for("index"))

    @app.route("/action/auto-reply-support", methods=["POST"])
    def action_auto_reply_support():
        brain().auto_reply_support_all()
        return redirect(url_for("index"))

    @app.route("/action/optimize-campaigns", methods=["POST"])
    def action_optimize_campaigns():
        brain().optimize_campaigns()
        return redirect(url_for("index"))

    @app.route("/action/simulate-campaigns", methods=["POST"])
    def action_simulate_campaigns():
        for campaign in brain().campaigns_all():
            if campaign.get("status") == "active":
                brain().simulate_campaign(campaign.get("id"))

        return redirect(url_for("index"))

    return app
