import glob as glob
import numpy as np
import json
from os.path import join
from pypianoroll import Multitrack

class MidiParser(Multitrack):
    def __init__(self, resulting_fname):
        """
        Initialize the MidiParser object.

        Parameters:
        - resulting_fname: The resulting filename.
        """
        self.resulting_fname = resulting_fname
        self.BEAT_RESOLUTION: int = 12  # Beat resolution for the MIDI files
        self.NUM_BAR: int = 4  # Number of bars for the pianoroll
        self.results = []  # List to store the parsed results

    def get_items(self):
        """
        Get a list of MIDI filenames from a JSON file.

        Returns:
        - common_files: List of MIDI filenames.
        """
        with open('common_files.json', 'r') as opfile:
            common_files = json.load(opfile)
        return common_files

    def parse(self):
        """
        Parse MIDI files and generate the resulting pianoroll.

        Returns:
        None
        """
        # Get the number of tracks in the MIDI files
        N_TRACKS = [len(Multitrack(f).tracks) for f in self.get_items()][0]

        # Reshape parameters
        RESHAPE_PARAMS = {
            'num_bar': self.NUM_BAR,
            'num_pitch': 84,
            'num_track': N_TRACKS,
            'num_timestep': 48,
            'beat_resolution': self.BEAT_RESOLUTION,
        }

        # Iterate over each MIDI file
        for filename in self.get_items():
            try:
                # Parse the MIDI file into a multitrack pianoroll
                multitrack = Multitrack(filename, beat_resolution=self.BEAT_RESOLUTION)
            except:
                continue  # Skip if parsing fails

            # Pad the multitrack pianoroll to a multiple of the beat resolution
            multitrack.pad_to_multiple(4 * self.BEAT_RESOLUTION)

            # Binarize the pianoroll
            multitrack.binarize()

            # Sort the tracks according to the program number
            multitrack.tracks.sort(key=lambda x: x.program)

            # Bring the drum track to the first track
            multitrack.tracks.sort(key=lambda x: ~x.is_drum)

            # Get the stacked pianoroll
            pianoroll = multitrack.get_stacked_pianoroll()

            # Check if the pianoroll has enough length
            if pianoroll.shape[0] < 4 * 4 * self.BEAT_RESOLUTION:
                continue  # Skip if too short

            # Keep only the mid-range pitches
            pianoroll = pianoroll[:, 24:108]

            # Reshape the pianoroll into phrases
            pianoroll = pianoroll.reshape(-1, 4 * self.BEAT_RESOLUTION, 84, N_TRACKS)

            # Append the reshaped pianoroll to the results list
            self.results.append(np.concatenate(
                [pianoroll[:-3], pianoroll[1:-2], pianoroll[2:-1], pianoroll[3:]], 1))

        # Concatenate the results into a single array
        result = np.concatenate(self.results, 0)

        print('Original shape:', result.shape)

        # Reshape the result array
        result = result.reshape(-1, RESHAPE_PARAMS['num_bar'], RESHAPE_PARAMS['num_timestep'],
                                RESHAPE_PARAMS['num_pitch'], RESHAPE_PARAMS['num_track'])

        print('New shape:', result.shape)

        # Save the resulting pianoroll to a compressed npz file
        np.savez_compressed(self.resulting_fname, nonzero=np.array(result.nonzero()),
                            shape=result.shape)
