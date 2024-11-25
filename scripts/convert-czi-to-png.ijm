// This macro process .czi files and converts them to PNGs colored according to the LUTs stored in the .czi settings.
// Before running the macro, create the input and output directories and add them to inpath and outpath in this script.

inpath = "/Users/jlabyer/Projects/oc-input/"
outpath = "/Users/jlabyer/Projects/oc-output/"

f = File.open(outpath + "oc-dims.csv");
print(f,"block,oc,file,basefile,height,width,slices,channels");

dirs = getFileList(inpath);

for (m = 0; m < dirs.length; m++){
	// make a corresponding directory in the output directory
	newdir = outpath + dirs[m];
	File.makeDirectory(newdir);
	// get a list of all files in the input directory
	files = getFileList(inpath + dirs[m]);
	// process the files and save them in the output directory
	for (n = 0; n < files.length; n++){
		print(files[n]);
		run("Bio-Formats Macro Extensions");
		//open .czi
		run("Bio-Formats Importer", "open=[" + inpath + dirs[m] + files[n] + "]");
		getDimensions(width, height, channels, slices, frames);
		fnoext = substring(files[n], 0, lengthOf(files[n]) - 4);
		block = substring(dirs[m], 0, lengthOf(dirs[m]) - 1);
		oc = block + "-" + toString(n + 1);
		print(f, block + "," + oc + "," + files[n] + "," + fnoext + "," + height + ","+ width + "," + slices + "," + channels);
		newdir2 = outpath + dirs[m] + fnoext;
		File.makeDirectory(newdir2);
		Ext.setId(inpath + dirs[m] + files[n]);
		// get channel colors
		colors = newArray(channels);
		for (j=1; j<=channels; j++){
			Ext.getMetadataValue("Experiment|AcquisitionBlock|MultiTrackSetup|TrackSetup|Detector|Color #"+j, value);
			colors[j-1] = value;
			print(colors[j-1]);
		}
		// convert to 8-bit if needed
		run("8-bit");
		// save each channel as a .tif
		run("Bio-Formats Exporter", "save=[/" + outpath + dirs[m] + fnoext + ".tif] write_each_channel compression=Uncompressed");
		close();
		// open each tif with the correct color
		for (k=0; k<channels; k++){
			r = 255;
			g = 255;
			b = 255;
			strcolor = toString(colors[k]);
			if (lengthOf(strcolor) == 7) {
				if(substring(colors[k], 1, 3)=="00"){
					r = 0;
					}
				if(substring(colors[k], 3, 5)=="00"){
					g = 0;
					}
				if(substring(colors[k], 5, 7)=="00"){
					b = 0;
					} 
			} else {
				print("invalid channel color, using white for LUT");
				}
					
			run("Bio-Formats Importer", "open=[" + outpath + dirs[m] + fnoext + "_C" + k + ".tif] color_mode=Custom rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT series_0_channel_0_red=" + r + " series_0_channel_0_green=" + g + " series_0_channel_0_blue=" + b);
			if (height > 600) {
				ar = width / height;
				nw = ar * 600;
				run("Size...", "width=" + nw + " height=600 depth=" + slices + " constrain interpolation=Bicubic");
				}
			// export to PNG sequence
			run("Image Sequence... ", "select=[" + outpath + dirs[m] + fnoext + "] dir=[" + outpath + dirs[m] + fnoext + "] format=PNG");
			close();
			}
		}
	}

File.close(f)
