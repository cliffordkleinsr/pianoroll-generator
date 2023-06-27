from pianogen.pianogen import MidiParser, MidiFileProcessor
import argparse
import warnings
warnings.filterwarnings("ignore")

def functiones(args):
    mode = 'parse'
    #Process 
    if mode == args.mode:
        processor = MidiFileProcessor(args.filepath)
        processor.get_listItems(args.tracks)
    #Parse
    else:
        drive = MidiParser(args.output) # parser object
        drive.parse() # parse the midi dir based on the json conditional list of same track files
        # you will endup with a pianoroll dataset at the root of your project dir


def main():
    """Parse and return the command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--filepath",type=str, default='midis', help="Path to your midi files.")
    parser.add_argument(
        "-t",
        "--tracks",
        type=int,
        default=0,
        help="Number of tracks.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default='train_x_phr.npz',
        help="output fname of your pianoroll.",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default='parse',
        help="mode processing or parsing.",
    )
    args = parser.parse_args()
    functiones(args)
    
if __name__ == '__main__':
    main()
