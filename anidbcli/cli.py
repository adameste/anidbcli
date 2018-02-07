import click
import libed2k
import os

@click.group(name="anidbcli")
@click.version_option(version="1.0", prog_name="anidbcli")
@click.option("--recursive", "-r", is_flag=True, default=False, help="Scan folders for files recursively.")
@click.option("--extensions", "-e",  help="List of file extensions separated by , character.")
@click.pass_context
def cli(ctx, recursive, extensions):
    ctx.obj["recursive"] = recursive
    ctx.obj["extensions"] = None
    if extensions:
        ext = []
        for i in extensions.split(","):
            i = i.strip()
            i = i.replace(".","")
            ext.append(i)
        ctx.obj["extensions"] = ext


@cli.command(help="Outputs file hashes that can be added manually to anidb.")
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.pass_context
def ed2k(ctx , files):
    to_process = []
    for file in files:
        if os.path.isfile(file):
            to_process.append(file)
        elif ctx.obj["recursive"]:
            for folder, subs, files in os.walk(file):
                for filename in files:
                    to_process.append(os.path.join(folder,filename))
    for file in to_process:
        if check_extension(file, ctx.obj["extensions"]):
            print(libed2k.get_ed2k_link(file))
        

def check_extension(path, extensions):
    if not extensions:
        return True
    else:
        filename, file_extension = os.path.splitext(path)
        return file_extension.replace(".", "") in extensions


def main():
    cli(obj={})

if __name__ == "__main__":
    main()