import logging

def setup_logger(name, log_file, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Creazione di un gestore per il file di log
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    # Creazione di un gestore per la console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Creazione di un formatter e aggiunta al gestore
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Aggiunta dei gestori al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
