# Preparing optical clearing files for display on the website
This document details how to prepare scientific images for display on this website without using the configuration portal. Parts of this process will ultimately be superceded by the configuration portal.

## Generate large PNGs for viewing on optical clearing file view pages

1. Download the optical clearing files from Dropbox

2. Move all .czi files into their own folder, and sort them into subfolders by tissue block

3. Replace any parentheses in filenames

4. Update `scripts/convert-czi-to-png.ijm` with the locations of the input folder and a destination folder. Then, run the macro. If the macro fails, you may need to separate out the largest files for another run.

5. Once you have completed a successful run of the ImageJ macro, save the output file `oc-dims.csv` in another location to preserve its content, and proceed with processing any leftover files.
    * For large .czi files, this probably means running the script again just on those files. If you have to do this multiple times, save the content of `oc-dims.csv` elsewhere after each successful run because the file will be overwritten on the next run. 
    * For .jpg files, resize the file if its height is greather than 600px, and save a copy of the file as a .png.
    * For .avi files, create an image sequence by opening the file in Fiji, then selecting Save As.. -> Image Sequence. 
      * Set the directory to your preference
      * Set format as PNG
      * Add the characters _C0 to the end of the filename (for consistency with how `scripts/convert-czi-to-png.ijm` names files)
      * Start at: 0
      * Digits: 4

6. Once all of the images have been converted to PNGs, update `app/assets/optical-clearing-czi/oc-files.csv` with entries for each of the source files. Most of these will come from `oc-dims.csv` but you will need to add entries for anything you processed by hand. If you are pulling values from multiple copies of `oc-dims.csv`, you will need to reassign values in the `oc` column to avoid conflicts.

7. Move the PNG files created in steps 1-6 into `app/assets/optical-clearing-czi`. Files should be sorted into folders by block.

8. Move the source files that were originally downloaded from Dropbox into the appropriate folders in `app/assets/optical-clearing-czi`.

9. Add new exceptions to `.gitignore` to avoid tracking the new .czi files

10. Test that individual pages are working for each new optical clearing file.

11. Check the new PNG files and `app/assets/optical-clearing-czi/oc-files.csv` into GitHub. Break this up into batches if there are many files.

## Generate thumbnails for view on optical clearing file summary pages and update homepage

1. From the previously generated PNG files, copy one PNG per channel per source file into a new folder. Do not sort into subfolders. Add a list of these files to a CSV file. Add a column for the parent file that was used to generate the PNG. See the other CSV files named like `thumbnails{block}.csv` for formatting.

2. Update `make-thumbnails.py` with the name of the new CSV created in step 12. Then run `poetry run python make-thumbnails.py` from the `scripts` folder.

3. Add a new folder for each new tissue block to `app/assets/thumbnails` and move the new thumbnail images into the appropriate folders.

4. Add entries for the new thumbnails to `app/assets/optical-clearing-czi/oc-thumbnails.csv`

5. Test that the optical clearing file summary pages work for each new tissue block.

6. Add links to the new optical clearing file summary pages into `app/assets/block-data.csv`. If the new files belong to a pancreas that doesn't have a section on the homepage yet, add a section for the new pancreas to `app/pages/home.py`.

7. Run all tests with pytest and run the app. When successful, check the changes into GitHub.