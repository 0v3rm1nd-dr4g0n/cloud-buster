from buster import CloudBuster
from cli import args, parser
import os.path


def scan(args):
    buster = CloudBuster(args.target)
    buster.scan_main()

    if not buster.resolving():
        print('>> NOT FOUND <<')
        return

    if not buster.protected():
        print('>> NOT BEHIND CLOUDFLARE <<')
        return

    if 'subdomains' in args.scan:
        target_found = buster.scan_subdomains(
            args.sub if args.sub else None
        )

        if target_found:
            print('>> MATCH <<')
            return

    # TODO : Make this useful, cause it's not solving anything
    if 'panels' in args.scan:
        target_found = buster.scan_panels(
            args.pan if args.sub else None
        )

        if target_found:
            print('>> MATCH <<')
            return

    if 'crimeflare' in args.scan:
        target_found = buster.search_crimeflare()

        if target_found:
            print('>> MATCH <<')
            return

    if 'mx' in args.scan:
        target_found = buster.scan_mx_records()

        if target_found:
            print('>> MATCH <<')
            return

    buster.scan_summary()
    print('>> UNABLE TO CONFIRM <<')


def scan_list(args):
    file = args.target
    for target in open(file).read().splitlines():
        args.target = target
        print('====================================')
        scan(args)


def main(args):
    if not args.target:
        parser.print_help()
    if os.path.isfile(args.target):
        scan_list(args)
    else:
        scan(args)


main(args)
