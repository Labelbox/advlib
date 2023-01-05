import argparse
import sys

from advlib.app import App
from advlib.util import UploadProgress

APIKEY = None

"""
You can hard code your API key here or use an environment variable method to
specify the API key.  If you use an environment variable, then set the value of
APIKEY to None

LABELBOX_API_KEY - should contain the API key itself
LABELBOX_API_KEY_FILE - an absolute path to a file containing the Labelbox API key.
"""

try:
    app = App()
except Exception as e:
    print(f"Unable to init ADVClient, {e}")

def handle_create_args(args):
    emb = app.create_embedding_type(args.name, args.dims)
    print(f"Embedding type created id={emb['id']}")


def handle_import_args(args):
    progress = UploadProgress(args.path)
    print(f"Uploading file: {args.path} ")
    app.import_vectors_from_file(args.id, args.path, callback=progress.callback)
    print("Check 'advtool count <embedding id>' for total searchable embeddings")


def handle_count_args(args):
    print(app.get_imported_vector_count(args.id))


def handle_list_args(args):
    for item in app.get_embedding_types():
        print(f"{item['id']} - {item['name']}")


def create_embeddings_parser(subparsers):
    subparser = subparsers.add_parser('embeddings', help='Embeddings Commands')
    embeddings = subparser.add_subparsers()

    list_parser = embeddings.add_parser('list', help='List Embeddings')
    list_parser.set_defaults(func=handle_list_args)

    create_parser = embeddings.add_parser('create', help='Create Embedding Type')
    create_parser.add_argument('name', metavar='NAME',
                               help='A unique name for the embedding type')
    create_parser.add_argument('dims', metavar='DIMENSIONS', type=int,
                               help='The number of dimensions this embedding has.')
    create_parser.set_defaults(func=handle_create_args)

    import_parser = embeddings.add_parser('import', help='Import Feature Vectors')
    import_parser.add_argument('id', metavar='ID',
                               help='The ID of the Embedding type')
    import_parser.add_argument('path', metavar='PATH',
                               help='The path to the embedding')
    import_parser.set_defaults(func=handle_import_args)

    import_parser = embeddings.add_parser('count', help='Get Imported Vector Count')
    import_parser.add_argument('id', metavar='ID',
                               help='The ID of the Embedding type')
    import_parser.set_defaults(func=handle_count_args)


def main():
    parser = argparse.ArgumentParser(description='')
    parser.set_defaults(func=lambda _: parser.print_help())
    subparsers = parser.add_subparsers(title='Commands', dest='command')
    create_embeddings_parser(subparsers)

    pargs = parser.parse_args(sys.argv[1:])
    pargs.func(pargs)


if __name__ == '__main__':
    main()
