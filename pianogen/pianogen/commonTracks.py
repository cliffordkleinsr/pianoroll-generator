import glob as glob, shutil,os, json
from os.path import join
from pypianoroll import Multitrack
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
        files = glob.glob(join(self.fldr, '*mid'))
        return files
        
    def most_common(
        self,
        lst,
    ) -> None:
        return max(set(lst), key=lst.count)
    
    def get_listItems(
        self,
    ) -> None:
        #os.makedirs(self.savez, exist_ok=True)
        files = self.get_items()
        tracks = [len(Multitrack(f).tracks) for f in files]
        mc = self.most_common(tracks)

        '''loop'''
        common = []
        for f in files:
            m = Multitrack(f)
            if len(m.tracks) == mc:
                common +=[f]
                #print('moving:', f, 'with no. of tracks ', len(m.tracks))
                #shutil.move(f, self.savez)
        with open('common_files.json', 'w') as outfile:
            json.dump(common, outfile)      
            
        
        
                  
        
