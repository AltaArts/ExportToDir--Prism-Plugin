# **ExportToDir plugin for Prism Pipeline 2**
A plugin to be used with version 2 of Prism Pipeline 

Prism automates and simplifies the workflow of animation and VFX projects.

You can find more information on the website:

https://prism-pipeline.com/


## **Installation**

### Copy method
Download the zip file from the green "Code" button above, or at Github https://github.com/JBreckeen/ExportToDir--Prism-Plugin/tree/main

Copy the directory named "ExportToDir" to a Prism2 plugin directory.  Prism's default plugin directories are: *{installation path}\Plugins\Apps* and *{installation Path}\Plugins\Custom*.

You can add additional plugin search paths in Prism2 settings.  Go to Settings->Plugins and click the gear icon.  This opens a dialogue and you may add additional search paths at the bottom.

I perfer this option so I have all my custom plugins in one sub directory where the other Prism plugins are: *{drive}\ProgramData\Prism2\plugins\CustomPlugins\


### Install method


## **Plugin Usage**
ExportToDir adds a right-click item to Prism2's GUI that opens a dialogue to customize an export file name, directory, and allow the file(s) to be zipped.  Using ExportToDir does not alter the original files at all.

The ExportToDir plugin adds a menu tab in Prism2's user settings that allows the user to create template filenames, and custom directoies used for the export.

The template filenames can be configured seperatly for each export type (Scene file, Product, Media item, Library item) and are denoted with @@ and contain data such as "Project Name", "Shot Name", "Version" etc.  When the dialogue is show, the template items will be replaced with the actual data if it exists.  The filename in the dialogue can always be edited

Directories added to the ExportToDir menu will be available for all projects.  An example is if you have a client share setup and want to quickly drop in a file that will be synced to the cloud.  These directories will be in the dropdown of the dialogue, along with any directories listed in Project Settings -> Locations.  The dialogue also allow for a custom output directory to be selected.

  
