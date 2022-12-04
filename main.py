import asyncio
import argparse
from aiopath import AsyncPath
from aioshutil import copyfile
from datetime import datetime

"""
--source [-s] folder
--output [-o]
"""

parser = argparse.ArgumentParser(description="Folder sorter")
parser.add_argument("--source", "-s", help="Source folder for sorting", required=True)
parser.add_argument("--output", "-o", help="Output folder to save files", default="sorted")

args = vars(parser.parse_args())
source = args.get("source")
output = args.get("output")


async def folders_handler(path: AsyncPath) -> None:
    async for el in path.iterdir():
        if await el.is_dir():
            await folders_handler(el)
        else:
            await copy_file(el)


async def copy_file(file: AsyncPath) -> None:
    extension = file.suffix
    new_path = folder_to_save / extension[1:]
    try:
        await new_path.mkdir(exist_ok=True, parents=True)
        await copyfile(file, new_path / file.name)
    except OSError as err:
        print(err)


if __name__ == '__main__':

    start_time = datetime.now()
    print(f"Process is started at {start_time}")

    folder_for_sorting = AsyncPath(source)
    folder_to_save = AsyncPath(output)

    asyncio.run(folders_handler(folder_for_sorting))

    end_time = datetime.now()
    total_time = end_time - start_time

    print(f"Files was sorted and copied into new folder '{output}'\n"
          f"Old folder '{source}' with garbage-files could be deleted.")
    print(f"Process is finished at {end_time}")
    print(f"Total time for sorting: {total_time.total_seconds()} seconds")


"""
Process is started at 2022-12-04 12:12:37.083636
Files was sorted and copied into new folder 'sorted'
Old folder 'garbage' with garbage-files could be deleted.
Process is finished at 2022-12-04 12:12:37.316090
Total time for sorting: 0.232454 seconds
"""