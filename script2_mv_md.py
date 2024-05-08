from pathlib import Path
import subprocess
mydir = Path(".")

for file in mydir.glob('**/*.md'):
    file = file.absolute()
    print(f"{file.parent.parent.name} . {file.parent.name} . {file.stem}.md")


    subprocess.call(["mv",
            f"{file}",
            f"./{file.parent.parent.name} . {file.parent.name} . {file.stem}.md"
        ])
    print()