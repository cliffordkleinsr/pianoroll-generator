# pianoroll-generator
Pianoroll-generator A package to generate pianoroll (NPZ) datasets

### Getting Started
------------------------
1. Building from the source 
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
        python inference.py -t 'Your specified number of tracks'
        ```
        The default mode is processing the list of midi files
    2. To now generate the dense dataset run the following  code set the inference mode to parsing
        ```py
         python inference.py --mode 'parse' 
        ```

    3. Run help:
       ```py
       python inference.py --help
       ```
       returns:
       ```bash
       usage: inference.py [-h] [-i FILEPATH] [-t TRACKS] [-o OUTPUT] [--mode MODE]
       options:
        -h, --help            show this help message and exit
        -i FILEPATH, --filepath FILEPATH
                              Path to your midi files.
        -t TRACKS, --tracks TRACKS
                              Number of tracks.
        -o OUTPUT, --output OUTPUT
                              output fname of your pianoroll.
        --mode MODE           mode processing or parsing.
       ```
       

TODO
==================
1. [x] command line arguments with user defined inputs
2. [x] Add support for own track checking from list of midis
3. [x] ~~PYPI~~ (cancelled)
        
    
    
    
    
    
