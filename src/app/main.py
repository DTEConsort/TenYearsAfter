import logging


LOGGER = logging.getLogger(__name__)


def run() -> None:
    LOGGER.info("Exécution de la fonction run")
    print("Base OK : environnement opérationnel.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    run()
