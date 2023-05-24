import glob as glob, numpy as np, json
from os.path import join
from pypianoroll import Multitrack

class MidiParser(Multitrack):
    def __init__(
        self,
        #fldr, # The list MIDI filenames
        resulting_fname, # The resulting filename
    ) -> None:
        
        #self.fldr = fldr # the folder where your midis are saved
        self.resulting_fname = resulting_fname
        #self.N_TRACKS = [len(Multitrack(f).tracks) for f in self.fldr][0]
        self.BEAT_RESOLUTION : int = 12
        self.NUM_BAR : int = 4
        self.results = []
        
    def get_items(
        self,
    ) -> None:
        
        #all_files = glob.glob(join(self.fldr, '*mid'))
        with open('common_files.json','r') as opfile:
            common_files = json.load(opfile)   
        return common_files

    def parse(
        self,
    ) -> None:
        N_TRACKS = [len(Multitrack(f).tracks) for f in self.get_items()][0]
        ## -- Params --
        RESHAPE_PARAMS = {    # Data
                'num_bar': self.NUM_BAR,
                'num_pitch': 84,
                'num_track': N_TRACKS,
                'num_timestep': 48,
                'beat_resolution': self.BEAT_RESOLUTION,
        }
        
        for filename in self.get_items():
            # Parse the MIDI file into multitrack pianoroll
            try:
                multitrack  = Multitrack(filename, beat_resolution=self.BEAT_RESOLUTION)
            except:
                continue

            # Pad to multtple
            multitrack.pad_to_multiple(4 * self.BEAT_RESOLUTION)

            # Binarize the pianoroll
            multitrack.binarize()

            # Sort the tracks according to program number
            multitrack.tracks.sort(key=lambda x: x.program)

            # Bring the drum track to the first track
            multitrack.tracks.sort(key=lambda x: ~x.is_drum)

            # Get the stacked pianoroll
            pianoroll = multitrack.get_stacked_pianoroll()

            # Check length
            if pianoroll.shape[0] < 4 * 4 * self.BEAT_RESOLUTION:
                continue

            # Keep only the mid-range pitches
            pianoroll = pianoroll[:, 24:108]

            # Reshape and get the phrase pianorolls
            pianoroll = pianoroll.reshape(-1, 4 * self.BEAT_RESOLUTION, 84, N_TRACKS)
            self.results.append(np.concatenate(
                [pianoroll[:-3], pianoroll[1:-2], pianoroll[2:-1], pianoroll[3:]], 1))

            result = np.concatenate(self.results, 0)
            
            print('Original shape: ', result.shape)
            
            result = result.reshape(-1, RESHAPE_PARAMS['num_bar'], RESHAPE_PARAMS['num_timestep'],
                        RESHAPE_PARAMS['num_pitch'], RESHAPE_PARAMS['num_track'])

            print('New shape: ', result.shape)
            
        # NOTE: You might want to shuffle the training data here
        np.savez_compressed(
            self.resulting_fname, nonzero=np.array(result.nonzero()),
            shape=result.shape
            )
