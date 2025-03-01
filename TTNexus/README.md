Executable is stored in dist\ btw

I mean, you can use the python file instead if you want... :D

Commands:

1. "--help"
    Opens help.

    Command: "path\to\TTNexus" --help


2. "fetch_everestyaml"
    Turns an everest.yaml file into a readable format (JSON) for GameMaker.

    Command: "path\to\TTNexus" fetch_everestyaml "path\to\Celeste\install" "mod_folder_name"

    For example, if I wanted to change my map "Cabin"'s everest.yaml into JSON, I'd run the following commands:

    cd "C:\Users\daxar\TeaTree\TTNexus\dist"
    .\TTNexus fetch_everestyaml "C:\Program Files (x86)\Steam\steamapps\common\Celeste" "Cabin"


3. "merge_everestjson"
    Turns everest.TTNexus.temp back into everest.yaml

    Command: same as the one above, but replace "fetch_everestyaml" with "merge_everest.json"