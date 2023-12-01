import click
import argparse
from compute_distance.functions import compute_distance

@click.command()
def cli() -> None:
    pass



def main() -> None:
    parser = argparse.ArgumentParser(description='Compute distance using CLI')
    parser.add_argument('admin0_path', help='Path to admin0 file')
    parser.add_argument('vector_file_path', help='Path to vector file')
    parser.add_argument('meta_data_path', help='Path to meta data file')
    parser.add_argument('out_path', help='Path for output')
    parser.add_argument('image_save_path', help='Path to save images')

    args = parser.parse_args()
    compute_distance(
        args.admin0_path,
        args.vector_file_path,
        args.meta_data_path,
        args.out_path,
        args.image_save_path
    )

if __name__ == '__main__':
    main()
