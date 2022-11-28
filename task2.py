import os
import asyncio
import aiofiles
from zipfile import ZipFile, Path
import xml.etree.ElementTree as ET


DIR_NAME = 'archives'
ZIPFILES_CNT = 50
ID_OBJECT_NAME = 'id_object_name.csv'
ID_LEVEL = 'id_level.csv'


async def write_csv_data(csv_file_name: str, data):
    async with aiofiles.open(csv_file_name, 'a+', newline='') as csvfile:
        await csvfile.write('\n'.join(data)+'\n')


def xmls_to_csv(xmlfiles_list: list, zipfile: ZipFile):
    str_id = ''
    level = 0
    objects = []
    id_levels = []
    id_object_name = []
    for xmlfile_name in xmlfiles_list:
        xmlfile = zipfile.read(xmlfile_name)
        root = ET.fromstring(xmlfile)
        for child in root:
            if child.tag == 'var':
                name = child.attrib.get('name')
                if name == 'id':
                    str_id = child.attrib.get('value')
                if name == 'level':
                    level = int(child.attrib.get('value'))
            else:
                for ch in child:
                    objects.append(ch.attrib.get('name'))
        id_levels.append('{0},{1}'.format(str_id, level))
    id_object_name.extend(['{0},{1}'.format(str_id, elem) for elem in objects])
    asyncio.run(write_csv_data(ID_OBJECT_NAME, id_object_name))
    asyncio.run(write_csv_data(ID_LEVEL, id_levels))


def create_csv_files():
    files_list = os.listdir(DIR_NAME)
    asyncio.run(write_csv_data(ID_OBJECT_NAME, ['id,object_name']))
    asyncio.run(write_csv_data(ID_LEVEL, ['id,level']))
    zipfiles_list = [file for file in files_list if file.find('.zip') > 0]
    for zipfile_name in zipfiles_list:
        zipfile = ZipFile(os.path.join(DIR_NAME, zipfile_name), mode='r')
        arch_path = Path(zipfile)
        if not arch_path.is_dir():
            continue
        xmlfiles_list = [
            file.name for file in arch_path.iterdir() if file.name.find('.xml') > 0]
        xmls_to_csv(xmlfiles_list, zipfile)


if __name__ == "__main__":
    create_csv_files()
