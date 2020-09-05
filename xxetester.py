import argparse
import traceback
from lxml import etree

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("payload", help="Path to payload as a file")
    argparser.add_argument("-v","--verbose", help="Verbose error output",action="store_true")
    args = argparser.parse_args()
    try:
        # Create vulnerable XML Parser
        # load_dtd is False by default
        # no_network is True by default
        # resolve_entities is False by default
        parser = etree.XMLParser(recover=False,
                                 dtd_validation=False,
                                 load_dtd=True,
                                 no_network=False,
                                 resolve_entities=True
                                 )

        tree = etree.parse(args.payload, parser=parser)
        # Output the whole XML
        etree.dump(tree.getroot())


    except Exception as err:
        print(err)
        if args.verbose:
            traceback.print_exc()
        else:
            print("If you wish more info execute this script with --verbose flag")




if __name__ == "__main__":
    # execute only if run as a script
    main()


