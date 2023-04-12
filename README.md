# RBR-HUD-EDITOR (Digidash editor)
Visual RBR HUD(Digidash) editor. Made for Richard Burns Rally RallySimFans mod.

<img width="601" alt="image" src="https://user-images.githubusercontent.com/104921631/231551308-2cfbb120-ea24-4eaa-8d22-6116822254c5.png">

# Warning:
- When you select any dashboard in RSF launcher contents in "RBR/generic/" and "RBR/misc/" folders will get overwritten. 
- I recommend creating a dashboard following the format of dashboards in "RBR/rsf_launcer/dashboards/**some_dashboard**"
- You can also use my **template(https://github.com/Tomas-B5/RBR-Digidash-modified-template)**. It has a much better layout and is much easier to edit.

# How to run:
- `pip install -r requirements.txt`
- Run `main.py`

# How to use:
- In RSF launcher select a **Custom** dashboard.
- Open the game, go into practice mode or hotlap mode.
- Run the program
- Click **Open**, select your RBR folder
- The program will automatically open one of the digidash files in "RBR/misc/" folders based on your games resolution.
- **Make sure in RSF launcher you have **Cockpit and dashbaord** page open, otherwise you won't see any changes in game.
- Make changes, each change will be saved to "RBR/misc/digidash*.ini" file immediately
- After you are done I recommend using **File -> Save As** to save your dashboard permantently into "RBR/rsf_launcer/dashboards/**some_dashboard**" folder you have created for your dashboard

# If you want to have your dashboard support 99.99% resolutions you should do this:
- Start with 1080p res. Make your dash using "digidash_1280.ini" file.
- After you are done make a copy and rename it "digidash.ini"
- Launch your game in 1440p or 4k res.
- Fix your dash(Usually multiplying all coords by 0.5, then multiplying all by 0.99 till it looks works decently enough, usually some manual touchups are required to finish it)
- Now you have two files **digidash_1280.ini** - works with 1080p 1280x960 and **digidash.ini** - works with 1440p, 4K and higher.

# Bugs 
- If your dashboard has non standard or non full structued(disabled) you will probably crash when trying to open it.

# Maybe add later:
- Add an option to export to all res or convert to another res(For now this can be by selecting all coordinates and multiplying them by a certain multiplier). 

# Useful links:
- Bnk file editor(https://github.com/Tomas-B5/RBR-bnk-editor)
- Template with a much better bank file already included(https://github.com/Tomas-B5/RBR-Digidash-modified-template)
