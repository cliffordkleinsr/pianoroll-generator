# pianoroll-generator
Pianoroll-generator A package to generate pianoroll (NPZ) datasets

### Getting Started
------------------------
1. Using the PYPI package.
   - To use it use the command: `pip install pianogen` to install all the necessary packages

2. Building from the source 
   - First clone the repository to your local directory with `git`
   - Open your local Terminal/Command Shell and run the following commands:
   
      ```shell
      cd pianoroll-generator # change directory to the cloned repository
      #use any of the following some will work dependent on your operating system
      #try
      python3 setup.py develop # works on both osx and linux
      #or
      pip install . 
      ```
    
    ### Usage
    - TO GENERATE A DENSE NPZ DATASET, first Download some midi files and place them in the ***midis*** directory 
    > ***Note*** the midis is an arbitrary dir, it can be named A anything
    - On either your python terminal or idle shell run the following codes:
    1. To create a list of files with common tracks
 
        ```PY
        from pianogen import MidiFileProcessor

        fldr = 'midis' #specify the folder where your midis are stored
        processor = MidiFileProcessor(fldr) # midi processor object
        processor.get_listItems()# generate a list of miifiles in json format
        # the json will be stored at the root directory of your project
        ```
    2. To now generate the dense dataset run the following  code
        ```py
        from pianogen import MidiParser
        
        fname = 'train_x_phr.npz'#output fname of your pianoroll
        
        drive = MidiParser(fname) # parser object
        drive.parse() # parse the midi dir based on the json conditional list of same track files
        # you will endup with a pianoroll dataset at the root of your project dir
        ```

TODO
==================
1. [ ] command line arguments with user defined inputs
2. [ ] GUI
3. [ ] PYPI
        
    
    
    
    
    
