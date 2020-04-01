# Giffer : Templatize GIFs.

### Why?

This code is setup to create Multilingual GIFs/Images for increasing the awareness of COVID-19 pandemic. 

### Folder structure
.  
├── code  
│   ├── data -> ../data  
│   ├── out -> ../out/   
├── data  
│   ├── fonts  
│   │   └── indic  
│   └── src  
├── nbs  
│   ├── code -> ../code/  
│   ├── data -> ../data/  
│   └── out -> ../out/  
└── out  
    ├── gif  
    └── image  
    
```

nbs/ - Experimental code 
code/ - Scripts to run
data/ - Data files
  - data/fonts - Fonts used in creating the GIFs, add more font styles here
  - data/src   - Source of Template GIFs, add more templates for GIFs here
out/ - Stores the newly baked GIFs
```

*Resources*  
[Fonts](https://drive.google.com/open?id=1n2x_uE_MHusDcMTsSghA-XAUP5eytNxN) . Download & extract it inside the `data/` dir.

[Google Sheet](https://docs.google.com/spreadsheets/d/1EiuYQQL98vR2SBUFbCbPOw4Rpe-A-sm5TwrTo46jUGQ/edit?usp=sharing) Download as CSV & place it inside the  `data/` dir.


### Dependencies:

For Ubuntu, use `conda env create -f environment.yml`.  
For Windows, most of the code setup should work. Will soon update with `yml` file.


### Process
1. Select a GIF or Image that you wish to translate to multiple languages, then, download inside `data/src/` folder and save as `{filename}.{suffix}`

2. Move into the `code` dir.
```
cd code
``` 

3. Split the GIF into frames
```
python split_merge.py split -p data/src/{filename}.gif
```

4. Clean the slate, remove texts from the GIF using Photoshop/GIMP/Paint or if you have a designer friend, take their help!  
This process is manual for now, automating this would require building a UI which is somthing we are thinking to build, but not right now.

5. Create a template JSON file, name it {filename}.json & put inside the `data` directory. For eg: look into `data/social-distance.json`.  
Again take the help of a designer friend or use application like Photoshop/GIMP to find the box coordinates `(left, top, right, bottom)`

6. Merge the frames back into GIF
```
python split_merge.py merge -p data/src/frames/{filename} -n {filename}.{suffix}
```

7. Create the translated GIF/Image files
```
python parser.py -p data/src/{filename}.{suffix} -l hindi,odia,tamil...
```

8. Create Mp4 files for GIF to share with others
```
python gif2mp4 out/gif/{filename}
```


### How to run?

```
cd code/
make splitgif filename='data/src/social-distance.gif' #Only for GIFs.
make translation filename='data/src/social-distance.gif'
make mp4

# Note this above approach works only when the CSV name aligns with that of gif's/png's name.
# For ex: covid-spread - {social-distance}.csv with {social-distance}.gif
```

`make gif`: 
- Reads a CSV file
- Reads the template (.json) file for the GIF
- Calls `gifware` or `imgware` to create the content

`make mp4`:
- Converts the `gif` to `mp4` (Execute this only when you want to create GIFs, not for images)

### How to create a template file?

- Put the GIF or Image inside the `data/src/` dir, and call `python splitter {path_to_file}`. This will split GIFs into individial frames & store it inside `data/src/frames/`.
- Use the frames as reference and create a template file, for eg: Template file for `data/src/social-distance.gif` file is `data/social-distance.json`.
#### Structure
```
{
  "num_frames": 34,
  "duration": "[0.12] * 26 + [1] + [1] + [0.5] + [2.5] * 4",
  "tags": {
    "T1": { "frames": [27],                 "box": [515, 275, 870, 460], "color":  "black"},
    "T2": { "frames": [29, 30, 31, 32, 33], "box": [186, 102, 450, 255], "color":  "black"},
    "T3": { "frames": [30, 31, 32, 33],     "box": [520, 107, 756, 255], "color":  "black"},
    "T4": { "frames": [31, 32, 33],         "box": [405, 565, 683, 674], "color":  "black"},
    "T5": { "frames": [32, 33],             "box": [818, 641, 1005,738], "color":  "black"}
  }
}
```
num_frames - Total number of frames in the GIF, zero indexed
duration   - List, how much time in seconds should a frame appear for in the GIF
tags:
  - T$ - unique id to tag that maps it to the [Google Sheet](https://docs.google.com/spreadsheets/d/1EiuYQQL98vR2SBUFbCbPOw4Rpe-A-sm5TwrTo46jUGQ/edit?usp=sharing)
  - frames - Frame number in which the Tag is supposed to appear
  - box    - [left, top, right, bottom] position of the text (Use GIMP, Photoshop or Matplotlib axis to find the positions)
  - color  - color of the text


### How it Works?

We write on a GIF with empty template. For example, look at `data/src/social-distance.gif`. 

### Demo

![Giffer](https://drive.google.com/uc?export=view&id=1pJ83HvNGBuTX1nqKjf28dxPbZVj4l6rt)
