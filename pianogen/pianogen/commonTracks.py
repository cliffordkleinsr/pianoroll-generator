import glob as glob
import shutil
import os
import json
from os.path import join
from pypianoroll import Multitrack

class MidiFileProcessor(Multitrack):
    def __init__(self, fldr):
        """
        Initialize the MidiFileProcessor object.

        Parameters:
        - fldr: The folder where the MIDI files are saved.
        """
        self.fldr = fldr
        # self.savez = savez

    def get_items(self):
        """
        Get a list of MIDI filenames from the specified folder.

        Returns:
        - files: List of MIDI filenames.
        """
        files = glob.glob(join(self.fldr, '*mid'))
        return files

    def most_common(self, lst):
        """
        Find the most common element in a list.

        Parameters:
        - lst: List of elements.

        Returns:
        - The most common element in the list.
        """
        return max(set(lst), key=lst.count)

    def get_listItems(self):
        """
        Process the MIDI files and save a list of common files.

        Returns:
        None
        """
        # Create the savez folder if it doesn't exist
        # os.makedirs(self.savez, exist_ok=True)

        # Get the list of MIDI files
        files = self.get_items()

        # Get the number of tracks for each MIDI file
        tracks = [len(Multitrack(f).tracks) for f in files]

        # Find the most common number of tracks
        mc = self.most_common(tracks)

        # Iterate over the MIDI files
        common = []
        for f in files:
            m = Multitrack(f)
            if len(m.tracks) == mc:
                common.append(f)
                # Move the file to the savez folder
                # shutil.move(f, self.savez)

        # Save the list of common files to a JSON file
        with open('common_files.json', 'w') as outfile:
            json.dump(common, outfile)
