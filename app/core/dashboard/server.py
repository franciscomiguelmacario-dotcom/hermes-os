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
    <title>Hermes OS</title>

    <style>
        :root {
            --bg: #020617;
            --panel: rgba(15, 23, 42, 0.82);
            --border: rgba(34, 211, 238, 0.28);
            --soft: rgba(148, 163, 184, 0.18);
            --text: #e5e7eb;
            --muted: #94a3b8;
            --cyan: #22d3ee;
            --blue: #3b82f6;
            --purple: #8b5cf6;
            --green: #22c55e;
            --yellow: #eab308;
            --red: #ef4444;
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
                radial-gradient(circle at 20% 20%, rgba(34, 211, 238, 0.18), transparent 28%),
                radial-gradient(circle at 80% 5%, rgba(139, 92, 246, 0.16), transparent 30%),
                linear-gradient(135deg, #020617, #030712 50%, #0f172a);
        }

        body::before {
            content: "";
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(rgba(34, 211, 238, 0.04) 1px, transparent 1px),
                linear-gradient(90deg, rgba(34, 211, 238, 0.04) 1px, transparent 1px);
            background-size: 42px 42px;
            pointer-events: none;
        }

        .shell {
            width: min(1500px, calc(100% - 32px));
            margin: 0 auto;
            padding: 22px 0 44px;
            position: relative;
            z-index: 1;
        }

        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 18px;
            padding: 18px;
            border: 1px solid var(--border);
            border-radius: 24px;
            background: var(--panel);
            backdrop-filter: blur(18px);
            box-shadow: 0 0 40px rgba(34, 211, 238, 0.10);
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
        }

        .status-pill {
            padding: 9px 12px;
            border: 1px solid rgba(34, 197, 94, 0.5);
            border-radius: 999px;
            color: #bbf7d0;
            background: rgba(22, 163, 74, 0.12);
            font-size: 13px;
            text-transform: uppercase;
        }

        .timestamp {
            color: var(--muted);
            font-size: 12px;
            margin-top: 8px;
            text-align: right;
        }

        .hero,
        .layout {
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 18px;
            margin-top: 18px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
            margin-top: 18px;
        }

        .panel,
        .metric-card,
        .money-card,
        form,
        .list-item,
        .terminal {
            border: 1px solid var(--soft);
            background: rgba(15, 23, 42, 0.72);
            backdrop-filter: blur(16px);
        }

        .panel {
            border-radius: 24px;
            overflow: hidden;
        }

        .panel-header {
            padding: 16px 18px;
            border-bottom: 1px solid var(--soft);
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

        .small {
            color: var(--muted);
            font-size: 12px;
        }

        .panel-body {
            padding: 18px;
        }

        .money-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
        }

        .money-card,
        .metric-card {
            padding: 18px;
            border-radius: 18px;
        }

        .money-label,
        .metric-title {
            color: var(--muted);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1.1px;
        }

        .money-value {
            margin-top: 10px;
            font-size: 30px;
            font-weight: 800;
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

        .green { color: var(--green); }
        .cyan { color: var(--cyan); }
        .yellow { color: var(--yellow); }
        .red { color: var(--red); }
        .purple { color: #c4b5fd; }

        .actions-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 14px;
        }

        form {
            border-radius: 18px;
            padding: 14px;
        }

        form h3 {
            margin: 0 0 10px;
            font-size: 13px;
            letter-spacing: 1px;
            color: var(--cyan);
            text-transform: uppercase;
        }

        input,
        select {
            width: 100%;
            margin-bottom: 8px;
            padding: 11px 12px;
            color: var(--text);
            border: 1px solid rgba(148, 163, 184, 0.26);
            border-radius: 12px;
            background: rgba(2, 6, 23, 0.74);
            outline: none;
        }

        label {
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--muted);
            font-size: 13px;
            margin-bottom: 8px;
        }

        input[type="checkbox"] {
            width: auto;
            margin: 0;
        }

        button {
            width: 100%;
            border: 0;
            border-radius: 12px;
            padding: 11px 14px;
            color: white;
            cursor: pointer;
            font-weight: 700;
            background: linear-gradient(135deg, var(--blue), var(--purple));
        }

        button:hover {
            filter: brightness(1.15);
        }

        .alert {
            padding: 12px;
            border-radius: 14px;
            border: 1px solid var(--soft);
            background: rgba(2, 6, 23, 0.48);
            margin-bottom: 10px;
        }

        .alert.ok { color: #bbf7d0; border-color: rgba(34, 197, 94, 0.35); }
        .alert.warning { color: #fef08a; border-color: rgba(234, 179, 8, 0.38); }
        .alert.danger { color: #fecaca; border-color: rgba(239, 68, 68, 0.38); }
        .alert.info { color: #a5f3fc; border-color: rgba(34, 211, 238, 0.35); }

        .mini-list {
            display: grid;
            gap: 10px;
        }

        .list-item {
            padding: 12px;
            border-radius: 14px;
        }

        .list-item span {
            display: block;
            color: var(--muted);
            font-size: 13px;
            margin-top: 4px;
        }

        .terminal {
            border-radius: 18px;
            overflow: hidden;
        }

        .terminal-top {
            padding: 10px 12px;
            border-bottom: 1px solid var(--soft);
            color: var(--muted);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
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
            padding: 9px 12px;
            border-radius: 999px;
            border: 1px solid rgba(34, 211, 238, 0.28);
            color: #a5f3fc;
            text-decoration: none;
            background: rgba(2, 6, 23, 0.44);
            font-size: 13px;
        }

        .wide {
            grid-column: 1 / -1;
        }

        @media (max-width: 1100px) {
            .hero,
            .layout {
                grid-template-columns: 1fr;
            }

            .grid,
            .money-grid {
                grid-template-columns: repeat(2, 1fr);
            }

            .actions-grid {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 640px) {
            .grid,
            .money-grid {
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
                    <div class="subtitle">Dropshipping Autonomous Command Center</div>
                </div>
            </div>

            <div>
                <div class="status-pill">Sistema operacional</div>
                <div class="timestamp">{{ data.get('generated_at') }}</div>
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
                            <div class="money-value cyan">{{ money.get('revenue', 0) }}€</div>
                        </div>

                        <div class="money-card">
                            <div class="money-label">Custos</div>
                            <div class="money-value yellow">{{ money.get('costs', 0) }}€</div>
                        </div>

                        <div class="money-card">
                            <div class="money-label">Lucro</div>
                            <div class="money-value {% if money.get('profit', 0) < 0 %}red{% else %}green{% endif %}">
                                {{ money.get('profit', 0) }}€
                            </div>
                        </div>

                        <div class="money-card">
                            <div class="money-label">Ticket Médio</div>
                            <div class="money-value purple">{{ money.get('average_order_value', 0) }}€</div>
                        </div>
                    </div>

                    <div class="grid">
                        <div class="metric-card">
                            <div class="metric-title">Produtos</div>
                            <div class="metric-value">{{ summary.get('products', 0) }}</div>
                            <div class="metric-sub">Ativos: {{ summary.get('active_products', 0) }}</div>
                        </div>

                        <div class="metric-card">
                            <div class="metric-title">Encomendas</div>
                            <div class="metric-value">{{ summary.get('orders', 0) }}</div>
                            <div class="metric-sub">Pendentes: {{ summary.get('pending_orders', 0) }}</div>
                        </div>

                        <div class="metric-card">
                            <div class="metric-title">Campanhas</div>
                            <div class="metric-value">{{ summary.get('campaigns', 0) }}</div>
                            <div class="metric-sub">Ativas: {{ summary.get('active_campaigns', 0) }}</div>
                        </div>

                        <div class="metric-card">
                            <div class="metric-title">Fulfillment</div>
                            <div class="metric-value">{{ summary.get('fulfillment_events', 0) }}</div>
                            <div class="metric-sub">Eventos pipeline</div>
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
                            {{ alert.get('message') }}
                        </div>
                    {% endfor %}

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
                <div class="metric-value">{{ summary.get('supplier_products', 0) }}</div>
                <div class="metric-sub">Produtos disponíveis</div>
            </div>

            <div class="metric-card">
                <div class="metric-title">Store API</div>
                <div class="metric-value">{{ summary.get('store_api_events', 0) }}</div>
                <div class="metric-sub">
                    {{ store_api.get('config', {}).get('provider', 'dry_run') }}
                    /
                    {% if store_api.get('config', {}).get('dry_run') %}dry-run{% else %}real{% endif %}
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-title">Supplier API</div>
                <div class="metric-value">{{ summary.get('supplier_api_events', 0) }}</div>
                <div class="metric-sub">
                    {{ supplier_api.get('config', {}).get('provider', 'dry_run') }}
                    /
                    {% if supplier_api.get('config', {}).get('dry_run') %}dry-run{% else %}real{% endif %}
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-title">Tracking</div>
                <div class="metric-value">{{ summary.get('fulfilled_orders', 0) }}</div>
                <div class="metric-sub">Encomendas enviadas</div>
            </div>
        </section>

        <section class="layout">
            <div class="panel">
                <div class="panel-header">
                    <h2 class="panel-title">Quick Actions</h2>
                    <span class="small">Operação</span>
                </div>

                <div class="panel-body">
                    <div class="actions-grid">
                        <form method="post" action="/action/store-autopilot">
                            <h3>Executar Store Autopilot</h3>
                            <input name="margin" value="40" placeholder="Margem %">
                            <input name="budget" value="10" placeholder="Budget">
                            <input name="channel" value="facebook_ads" placeholder="Canal">
                            <input name="tracking_prefix" value="HER" placeholder="Tracking prefix">
                            <button type="submit">Iniciar ciclo</button>
                        </form>

                        <form method="post" action="/action/add-supplier-product">
                            <h3>Adicionar produto fornecedor</h3>
                            <input name="title" value="Relógio inteligente" placeholder="Produto">
                            <input name="cost" value="12.50" placeholder="Custo">
                            <input name="shipping_days" value="8" placeholder="Dias envio">
                            <input name="supplier_url" value="https://fornecedor.local/produto" placeholder="URL">
                            <input name="category" value="gadgets" placeholder="Categoria">
                            <button type="submit">Adicionar</button>
                        </form>

                        <form method="post" action="/action/create-order">
                            <h3>Criar encomenda teste</h3>
                            <input name="product_id" value="1" placeholder="ID produto">
                            <input name="customer_name" value="Francisco" placeholder="Cliente">
                            <input name="customer_email" value="teste@email.com" placeholder="Email">
                            <input name="quantity" value="1" placeholder="Quantidade">
                            <button type="submit">Criar encomenda</button>
                        </form>

                        <form method="post" action="/action/send-notifications">
                            <h3>Comunicações</h3>
                            <button type="submit">Enviar notificações</button>
                        </form>
                    </div>
                </div>
            </div>

            <div class="panel">
                <div class="panel-header">
                    <h2 class="panel-title">Fulfillment Pipeline</h2>
                    <span class="small">Fornecedor / Tracking</span>
                </div>

                <div class="panel-body">
                    <div class="actions-grid">
                        <form method="post" action="/action/submit-order-supplier">
                            <h3>Enviar encomenda ao fornecedor</h3>
                            <input name="order_id" value="1" placeholder="ID encomenda">
                            <button type="submit">Preparar / enviar</button>
                        </form>

                        <form method="post" action="/action/submit-pending-orders-supplier">
                            <h3>Enviar pendentes ao fornecedor</h3>
                            <button type="submit">Processar pendentes</button>
                        </form>

                        <form method="post" action="/action/mark-supplier-tracking">
                            <h3>Registar tracking</h3>
                            <input name="order_id" value="1" placeholder="ID encomenda">
                            <input name="tracking_number" value="TRACK-FORN-123" placeholder="Tracking">
                            <button type="submit">Marcar como enviada</button>
                        </form>

                        <form method="post" action="/action/auto-reply-support">
                            <h3>Suporte IA</h3>
                            <button type="submit">Responder suporte</button>
                        </form>
                    </div>

                    <div style="height: 14px;"></div>

                    <div class="terminal">
                        <div class="terminal-top">Último evento fulfillment</div>
                        <pre>{{ fulfillment_latest }}</pre>
                    </div>
                </div>
            </div>
        </section>

        <section class="layout">
            <div class="panel">
                <div class="panel-header">
                    <h2 class="panel-title">Store API Bridge</h2>
                    <span class="small">Shopify / WooCommerce</span>
                </div>

                <div class="panel-body">
                    <form method="post" action="/action/store-api-config">
                        <h3>Configurar Store API</h3>

                        <select name="provider">
                            <option value="dry_run" {% if store_api.get('config', {}).get('provider') == 'dry_run' %}selected{% endif %}>Dry Run</option>
                            <option value="shopify" {% if store_api.get('config', {}).get('provider') == 'shopify' %}selected{% endif %}>Shopify</option>
                            <option value="woocommerce" {% if store_api.get('config', {}).get('provider') == 'woocommerce' %}selected{% endif %}>WooCommerce</option>
                            <option value="custom" {% if store_api.get('config', {}).get('provider') == 'custom' %}selected{% endif %}>Custom API</option>
                        </select>

                        <input name="base_url" value="{{ store_api.get('config', {}).get('base_url', '') }}" placeholder="Base URL">
                        <input name="access_token" type="password" placeholder="Access token">
                        <input name="api_key" type="password" placeholder="API key">
                        <input name="api_secret" type="password" placeholder="API secret">

                        <label>
                            <input type="checkbox" name="enabled" {% if store_api.get('config', {}).get('enabled') %}checked{% endif %}>
                            Ativar Store API
                        </label>

                        <label>
                            <input type="checkbox" name="dry_run" {% if store_api.get('config', {}).get('dry_run') %}checked{% endif %}>
                            Dry-run
                        </label>

                        <label>
                            <input type="checkbox" name="auto_sync_on_publish" {% if store_api.get('config', {}).get('auto_sync_on_publish') %}checked{% endif %}>
                            Auto sync
                        </label>

                        <button type="submit">Guardar Store API</button>
                    </form>

                    <div style="height: 14px;"></div>

                    <form method="post" action="/action/sync-store-products">
                        <h3>Sincronizar produtos ativos</h3>
                        <button type="submit">Sincronizar loja</button>
                    </form>
                </div>
            </div>

            <div class="panel">
                <div class="panel-header">
                    <h2 class="panel-title">Supplier API Bridge</h2>
                    <span class="small">Fornecedor real</span>
                </div>

                <div class="panel-body">
                    <form method="post" action="/action/supplier-api-config">
                        <h3>Configurar Supplier API</h3>

                        <select name="provider">
                            <option value="dry_run" {% if supplier_api.get('config', {}).get('provider') == 'dry_run' %}selected{% endif %}>Dry Run</option>
                            <option value="custom" {% if supplier_api.get('config', {}).get('provider') == 'custom' %}selected{% endif %}>Custom API</option>
                            <option value="aliexpress" {% if supplier_api.get('config', {}).get('provider') == 'aliexpress' %}selected{% endif %}>AliExpress</option>
                            <option value="cj_dropshipping" {% if supplier_api.get('config', {}).get('provider') == 'cj_dropshipping' %}selected{% endif %}>CJ Dropshipping</option>
                        </select>

                        <input name="base_url" value="{{ supplier_api.get('config', {}).get('base_url', '') }}" placeholder="Base URL">
                        <input name="access_token" type="password" placeholder="Access token">
                        <input name="api_key" type="password" placeholder="API key">
                        <input name="api_secret" type="password" placeholder="API secret">

                        <label>
                            <input type="checkbox" name="enabled" {% if supplier_api.get('config', {}).get('enabled') %}checked{% endif %}>
                            Ativar Supplier API
                        </label>

                        <label>
                            <input type="checkbox" name="dry_run" {% if supplier_api.get('config', {}).get('dry_run') %}checked{% endif %}>
                            Dry-run
                        </label>

                        <button type="submit">Guardar Supplier API</button>
                    </form>
                </div>
            </div>
        </section>

        <section class="layout">
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
                        <a class="link-chip" href="/api/store-api" target="_blank">Store API</a>
                        <a class="link-chip" href="/api/supplier-api" target="_blank">Supplier API</a>
                        <a class="link-chip" href="/api/fulfillment" target="_blank">Fulfillment</a>
                        <a class="link-chip" href="/api/campaigns" target="_blank">Campanhas</a>
                        <a class="link-chip" href="/api/notifications" target="_blank">Notificações</a>
                        <a class="link-chip" href="/api/support" target="_blank">Suporte</a>
                    </div>

                    <div style="height: 14px;"></div>

                    <div class="terminal">
                        <div class="terminal-top">Autopilot Config</div>
                        <pre>{{ autopilot_config }}</pre>
                    </div>
                </div>
            </div>

            <div class="panel">
                <div class="panel-header">
                    <h2 class="panel-title">API Logs</h2>
                    <span class="small">Últimos eventos</span>
                </div>

                <div class="panel-body">
                    <div class="terminal">
                        <div class="terminal-top">Store API</div>
                        <pre>{{ store_api_history }}</pre>
                    </div>

                    <div style="height: 14px;"></div>

                    <div class="terminal">
                        <div class="terminal-top">Supplier API</div>
                        <pre>{{ supplier_api_history }}</pre>
                    </div>
                </div>
            </div>
        </section>

        <section class="panel wide" style="margin-top: 18px;">
            <div class="panel-header">
                <h2 class="panel-title">Hermes Raw Telemetry</h2>
                <span class="small">Dados completos</span>
            </div>

            <div class="panel-body">
                <div class="terminal">
                    <div class="terminal-top">Live Snapshot</div>
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

    def mask_sensitive_config(config):
        if not isinstance(config, dict):
            return config

        masked = dict(config)

        for key in ["api_key", "api_secret", "access_token"]:
            if masked.get(key):
                masked[key] = "***configured***"
            else:
                masked[key] = ""

        return masked

    def json_text(value):
        return json.dumps(value, indent=2, ensure_ascii=False)

    @app.route("/", methods=["GET"])
    def index():
        data = brain().dashboard_data()
        store_api = data.get("store_api", {})
        supplier_api = data.get("supplier_api", {})
        fulfillment = data.get("fulfillment", {})

        return render_template_string(
            PAGE,
            data=data,
            summary=data.get("summary", {}),
            money=data.get("money", {}),
            alerts=data.get("alerts", []),
            actions=data.get("next_recommended_actions", []),
            autopilot=data.get("autopilot", {}),
            store_api=store_api,
            supplier_api=supplier_api,
            fulfillment=fulfillment,
            autopilot_config=json_text(
                data.get("autopilot", {}).get("config", {})
            ),
            store_api_history=json_text(
                store_api.get("latest_sync", {})
            ),
            supplier_api_history=json_text(
                supplier_api.get("latest_sync", {})
            ),
            fulfillment_latest=json_text(
                fulfillment.get("latest_event", {})
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

    @app.route("/api/store-api", methods=["GET"])
    def api_store_api():
        return jsonify({
            "config": mask_sensitive_config(brain().store_api_config()),
            "history": brain().store_api_history()
        })

    @app.route("/api/supplier-api", methods=["GET"])
    def api_supplier_api():
        return jsonify({
            "config": mask_sensitive_config(brain().supplier_api_config()),
            "history": brain().supplier_api_history()
        })

    @app.route("/api/fulfillment", methods=["GET"])
    def api_fulfillment():
        return jsonify({
            "history": brain().fulfillment_pipeline_history()
        })

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

    @app.route("/action/send-notifications", methods=["POST"])
    def action_send_notifications():
        brain().send_notifications()
        return redirect(url_for("index"))

    @app.route("/action/auto-reply-support", methods=["POST"])
    def action_auto_reply_support():
        brain().auto_reply_support_all()
        return redirect(url_for("index"))

    @app.route("/action/store-api-config", methods=["POST"])
    def action_store_api_config():
        brain().set_store_api_config(
            "provider",
            request.form.get("provider", "dry_run")
        )

        brain().set_store_api_config(
            "base_url",
            request.form.get("base_url", "")
        )

        brain().set_store_api_config(
            "enabled",
            "enabled" in request.form
        )

        brain().set_store_api_config(
            "dry_run",
            "dry_run" in request.form
        )

        brain().set_store_api_config(
            "auto_sync_on_publish",
            "auto_sync_on_publish" in request.form
        )

        access_token = request.form.get("access_token", "").strip()
        api_key = request.form.get("api_key", "").strip()
        api_secret = request.form.get("api_secret", "").strip()

        if access_token:
            brain().set_store_api_config("access_token", access_token)

        if api_key:
            brain().set_store_api_config("api_key", api_key)

        if api_secret:
            brain().set_store_api_config("api_secret", api_secret)

        return redirect(url_for("index"))

    @app.route("/action/sync-store-products", methods=["POST"])
    def action_sync_store_products():
        brain().sync_products_to_store()
        return redirect(url_for("index"))

    @app.route("/action/supplier-api-config", methods=["POST"])
    def action_supplier_api_config():
        brain().set_supplier_api_config(
            "provider",
            request.form.get("provider", "dry_run")
        )

        brain().set_supplier_api_config(
            "base_url",
            request.form.get("base_url", "")
        )

        brain().set_supplier_api_config(
            "enabled",
            "enabled" in request.form
        )

        brain().set_supplier_api_config(
            "dry_run",
            "dry_run" in request.form
        )

        access_token = request.form.get("access_token", "").strip()
        api_key = request.form.get("api_key", "").strip()
        api_secret = request.form.get("api_secret", "").strip()

        if access_token:
            brain().set_supplier_api_config("access_token", access_token)

        if api_key:
            brain().set_supplier_api_config("api_key", api_key)

        if api_secret:
            brain().set_supplier_api_config("api_secret", api_secret)

        return redirect(url_for("index"))

    @app.route("/action/submit-order-supplier", methods=["POST"])
    def action_submit_order_supplier():
        brain().submit_order_to_supplier(
            request.form.get("order_id", "1")
        )

        return redirect(url_for("index"))

    @app.route("/action/submit-pending-orders-supplier", methods=["POST"])
    def action_submit_pending_orders_supplier():
        brain().submit_pending_orders_to_supplier()
        return redirect(url_for("index"))

    @app.route("/action/mark-supplier-tracking", methods=["POST"])
    def action_mark_supplier_tracking():
        brain().mark_supplier_tracking(
            request.form.get("order_id", "1"),
            request.form.get("tracking_number", "")
        )

        return redirect(url_for("index"))

    return app
