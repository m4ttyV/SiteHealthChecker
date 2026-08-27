import argparse
import models

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Site HealthChecker.")
    parser.add_argument(
        'mode',
        choices=['daemon', 'check', 'stats'],
        help='Режим работы программы'
    )
    args = parser.parse_args()
    if args.mode == 'check':
        models.check()
    elif args.mode == 'daemon':
        models.deamon()
    elif args.mode == 'stats':
        models.stats()