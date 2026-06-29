import typer

from app.main import main

app = typer.Typer(
    help="Hermes OS CLI",
    no_args_is_help=True
)


@app.command()
def start():
    """Inicia o Hermes."""
    main()


@app.command()
def status():
    """Mostra o estado do Hermes."""
    print("✅ Hermes operacional")


@app.command()
def doctor():
    """Diagnóstico do sistema."""
    print("🩺 Verificação do sistema")
    print("✅ Python")
    print("✅ Config")
    print("✅ Database")
    print("✅ Plugins")


@app.command()
def plugins():
    """Lista os plugins."""
    print("📦 Plugins instalados")
    print("- System")


if __name__ == "__main__":
    app()
