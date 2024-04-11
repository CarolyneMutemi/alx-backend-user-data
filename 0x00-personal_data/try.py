import logging
logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(level=logging.INFO)
    logger.info('Started')
    logger.info('Finished')
    print(logger.log)

if __name__ == '__main__':
    main()