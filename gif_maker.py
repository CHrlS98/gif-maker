"""
Create a gif from a series of images.

Images will be assembled in the order they are given.
"""
from PIL import Image
import argparse
import os


def _build_arg_parser():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('input', nargs='+',
                   help='Input images in PNG format.')
    p.add_argument('output', help='Output GIF file.')
    p.add_argument('--frame_delay', type=int, default=100,
                   help='Delay between frames in milliseconds. [%(default)s]')
    p.add_argument('--n_repeats', type=int,
                   help='Number of times to repeat the GIF. '
                        'By default, infinite.')
    p.add_argument('-f', action='store_true', dest='overwrite',
                   help='Overwrite output file if it exists.')
    return p


def main():
    parser = _build_arg_parser()
    args = parser.parse_args()

    out_dir, _ = os.path.split(args.output)
    if out_dir and not os.path.exists(out_dir):
        parser.error('Output directory {} does not exist.'.format(out_dir))

    if os.path.exists(args.output) and not args.overwrite:
        parser.error('Output file {} exists. Use -f to overwrite.'
                     .format(args.output))

    images = []
    for fname in args.input:
        if os.path.exists(fname):
            i = Image.open(fname)
            images.append(i)
        else:
            parser.error('Invalid image file: {}'.format(fname))

    loops = args.n_repeats if args.n_repeats is not None else 0
    images[0].save(args.output, save_all=True,
                   append_images=images[1:],
                   duration=args.frame_delay, loop=loops)


if __name__ == '__main__':
    main()
