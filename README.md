#   FMDataset

FMDataset is a application developed with python and Flask. It acts like a scouting tool for visualization of footballers' information in 
the format of the video game Football Manager®. Based on a csv file with the players' information, the tool displays a web application that allows 
to visualize such information in a friendly way. It uses [seaborn](https://seaborn.pydata.org/examples/index.html) and [plotly](https://plotly.com/)  

Based on the native attributes of the game, it defines a series of new attributes that allow the player to be evaluated more reliably.
These custom parameters are defined in pipeline.py file, so you can view them and define some new ones.

It also lets you record a preselection list where you can add players to get them saved.

To test the tool, you can use the file players.csv inside the csv directory or you can get a csv with your custom data, but please note that this 
file must have a specific format, as defined in the pipeline.py file

It is possible to use a facepack so that the real images of the players are shown instead of a generic one. To do this, download a facepack (you 
can find many of them on the web, for example at https://df11faces.com/) and place it in the static/faces directory.

Note that this is a tool that is still under development.