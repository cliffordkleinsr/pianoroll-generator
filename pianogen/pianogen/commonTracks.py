import glob as glob, shutil,os, json, mido
from os.path import join
from pypianoroll import Multitrack
from tqdm import tqdm
''' pypianoroll == 0.5.3!!!!'''

class MidiFileProcessor(Multitrack):
    def __init__(
        self,
        fldr,
        #savez,
    ) -> None:
        self.fldr = fldr # the folder where your midis are saved
        #self.savez = savez

    def get_items(
        self,
    ) -> None:
        files = glob.glob(join(self.fldr, '*[mM][iI][dD]'))
        str_files, clean_files = [], []

        progress_bar = tqdm(total=len(files), desc="Cleaning Files", unit="file", ncols=80)
        
        for f in files:
            try:
                gud_f =Multitrack(f)
                len(gud_f.tracks)
                str_files +=[f]
                clean_files += [gud_f]
            except (ValueError, IndexError, OSError, mido.midifiles.meta.KeySignatureError) as e:
                continue
            
            progress_bar.update(1)

        progress_bar.close()
        
        return str_files, clean_files
        
    def most_common(
        self,
        lst,
    ) -> None:
        return max(set(lst), key=lst.count)
    
    
    def get_listItems(
        self,
        n_tracks: int=0,
    ) -> None:
        #os.makedirs(self.savez, exist_ok=True)
        str_files, clean_files = self.get_items()
              
        tracks = [len(f.tracks) for f in clean_files]
        mc = self.most_common(tracks)
        ## support for own track input
        if n_tracks > 0:
            mc = n_tracks
            
        cocon = "The most common have {} tracks".format(mc)
        '''loop'''
        common = []
        for f, c in zip(str_files, clean_files):
            if len(c.tracks) == mc:
                common +=[f]
                #print('moving:', f, 'with no. of tracks ', len(m.tracks))
                #shutil.move(f, self.savez)
        os.makedirs('utilities', exist_ok=True)

        
        with open('utilities/common_files.json', 'w') as outfile:
            json.dump(common, outfile)
        
         
        with open('utilities/mc.txt', 'w') as mc_file:
            mc_file.write(cocon)
            
        
        
                  
        
