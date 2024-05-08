from pathlib import Path
import subprocess
mydir = Path(".")

for file in mydir.glob('**/*.md'):
    file = file.absolute()
    print(file)


    print(["pandoc",
            "-t",
            "markdown_strict",
            f"{file}",
            "-o",
            f"{file.parent}/{file.stem}.md"
        ])
    print()