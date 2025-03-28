# **ExportToDir plugin for Prism Pipeline 2**
A plugin to be used with version 2 of Prism Pipeline 

Prism automates and simplifies the workflow of animation and VFX projects.

You can find more information on the website:

https://prism-pipeline.com/

<br/>

**Tested up to Prism 2.0.16**

<br/>

## **Plugin Usage**

ExportToDir adds a right-click item to Prism2's GUI that opens a dialogue to export Prism items such as an entire Project folder, entire Asset/Shot folders, Scene Files, Products, Media, and Library items.  The user may customize the export file name and directory, and has the option to have the file(s) zipped.  Using ExportToDir does not alter the original files or information data.

The ExportToDir plugin adds a menu tab in Prism2's User Settings that allows the user to create template filenames, and custom directories used for the export.  The template filenames can be configured separately for each export type (Project, Asset, Shot, Scene file, Product, Media item, Library item) and are denoted with @@ and contain data such as "Project Name", "Shot Name", "Version" etc.  Tooltips in each template box show what data is available for each type.

*example:*
		@PROJECT@--@SEQUENCE@\_@SHOT@\_@TASK@\_@VERSION@@EXTENSION@
		
When the dialogue is shown, the template items will be replaced with the actual data if it exists.  The resulting filename can always be edited afterwards in the dialogue.  Projects can be exported using the right-click menu from the "i" icon in the Project widget.  For Media items, the right-click will be from the image in the Media Viewer and has the ability to export a single image (current viewed frame of a sequence), or the entire sequence.

Directories added to the ExportToDir menu will be available for all projects.  An example is if you have a client or studio share folder setup and want to quickly drop a file that will be synced to the cloud.  These directories will be in the dropdown of the dialogue, along with any directories listed in Project Settings -> Locations.  The dialogue also allows for a custom output directory to be selected.

Using the .zip checkbox will create an archive and copy the files using DEFLATE.  If the selected export is an image sequence, it will copy all the image files into the .zip file.

Export settings are saved on a per-project basis.  The last five project recents will be saved in order to speed up exports.

## **Installation**

This plugin is for Windows only, as Prism2 only supports Windows at this time.

You can either download the latest stable release version from: [Latest Release](https://github.com/AltaArts/ExportToDir--Prism-Plugin/releases/latest)

or download the current code zip file from the green "Code" button above or on [Github](https://github.com/JBreckeen/ExportToDir--Prism-Plugin/tree/main)

Copy the directory named "ExportToDir" to a directory of your choice, or a Prism2 plugin directory.

Prism's default plugin directories are: *{installation path}\Plugins\Apps* and *{installation Path}\Plugins\Custom*.

It is suggested to have all custom plugins in a seperate folder suchs as: *{drive}\ProgramData\Prism2\plugins\CustomPlugins*

You can add the additional plugin search paths in Prism2 settings.  Go to Settings->Plugins and click the gear icon.  This opens a dialogue and you may add additional search paths at the bottom.

Once added, you can either restart Prism2, or select the "Add existing plugin" (plus icon) and navigate to where you saved the ExportToDir folder.


## **Issues / Suggestions**

For any bug reports or suggestions, please add to the GitHub repo.
