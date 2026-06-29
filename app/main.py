from app.core.startup import Hermes


def main():

    hermes = Hermes()

    hermes.start()

    hermes.brain.execute("status")


if __name__ == "__main__":
    main()
