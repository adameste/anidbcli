import click
import os
import pyperclip
import anidbcli.libed2k as libed2k
import anidbcli.anidbconnector as anidbconnector
import anidbcli.output as output
import anidbcli.operations as operations

@click.group(name="anidbcli")
@click.version_option(version="1.22", prog_name="anidbcli")
@click.option("--recursive", "-r", is_flag=True, default=False, help="Scan folders for files recursively.")
@click.option("--extensions", "-e",  help="List of file extensions separated by , character.")
@click.option("--quiet", "-q", is_flag=True, default=False, help="Display only warnings and errors.")
@click.pass_context
def cli(ctx, recursive, extensions, quiet):
    ctx.obj["recursive"] = recursive
    ctx.obj["extensions"] = None
    ctx.obj["output"] = output.CliOutput(quiet)
    if extensions:
        ext = []
        for i in extensions.split(","):
            i = i.strip()
            i = i.replace(".","")
            ext.append(i)
        ctx.obj["extensions"] = ext


@cli.command(help="Outputs file hashes that can be added manually to anidb.")
@click.option("--clipboard", "-c", is_flag=True, default=False, help="Copy the results to clipboard when finished.")
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.pass_context
def ed2k(ctx , files, clipboard):
    to_process = get_files_to_process(files, ctx)
    links = []
    for file in to_process:
        link = libed2k.get_ed2k_link(file)
        print(link)
        links.append(link)
    if clipboard:
        pyperclip.copy("\n".join(links))
        ctx.obj["output"].success("All links were copied to clipboard.")

@cli.command(help="Utilize the anidb API. You can add files to mylist and/or organize them to directories using "
+ "information obtained from AniDB.")
@click.option('--username', "-u", prompt=True)
@click.option('--password', "-p", prompt=True, hide_input=True)
@click.option('--apikey', "-k")
@click.option("--add", "-a", is_flag=True, default=False, help="Add files to mylist.")
@click.option("--rename", "-r",  default=None, help="Rename the files according to provided format. See documentation for more info.")
@click.option("--keep-structure", "-s",  default=False, is_flag=True, help="Prepends file original directory path to the new path. See documentation for info.")
@click.option("--date-format", "-d", default="%Y-%m-%d", help="Date format. See documentation for details.")
@click.option("--delete-empty", "-x", default=False, is_flag=True, help="Delete empty folders after moving files.")
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.pass_context
def api(ctx, username, password, apikey, add, rename, files, keep_structure, date_format, delete_empty):
    if (not add and not rename):
        ctx.obj["output"].info("Nothing to do.")
        return
    try:
        if apikey:
            conn = anidbconnector.AnidbConnector.create_secure(username, password, apikey)
        else:
            conn = anidbconnector.AnidbConnector.create_plain(username, password)
    except Exception as e:
        ctx.obj["output"].error(e)
        exit(1)
    pipeline = []
    pipeline.append(operations.HashOperation(ctx.obj["output"]))
    if add:
        pipeline.append(operations.MylistAddOperation(conn, ctx.obj["output"]))
    if rename:
        pipeline.append(operations.GetFileInfoOperation(conn, ctx.obj["output"]))
        pipeline.append(operations.RenameOperation(ctx.obj["output"], rename, date_format, delete_empty, keep_structure))
    to_process = get_files_to_process(files, ctx)
    for file in to_process:
        file_obj = {}
        file_obj["path"] = file
        ctx.obj["output"].info("Processing file \"" + file +"\"")
        for operation in pipeline:
            res = operation.Process(file_obj)
            if not res: # Critical error, cannot proceed with pipeline
                break
    conn.close()
        
def get_files_to_process(files, ctx):
    to_process = []
    for file in files:
        if os.path.isfile(file):
            to_process.append(file)
        elif ctx.obj["recursive"]:
            for folder, _, files in os.walk(file):
                for filename in files:
                    to_process.append(os.path.join(folder,filename))
    ret = []
    for f in to_process:
        if (check_extension(f, ctx.obj["extensions"])):
            ret.append(f)
    return ret

def check_extension(path, extensions):
    if not extensions:
        return True
    else:
        _, file_extension = os.path.splitext(path)
        return file_extension.replace(".", "") in extensions


def main():
    cli(obj={})

if __name__ == "__main__":
    main()