
import os
from uuid import uuid4
from random import randint
from zipfile import ZipFile


DIR_NAME = 'archives'
ZIPFILES_CNT = 50
XMLFILES_CNT = 100


def get_random_xml() -> str:
    xml_pattern = '''<root>
    <var name="id" value="{unique_name}"/>
    <var name="level" value="{unique_number}"/>
    <objects>
        {objects_list}
    </objects>
    </root>'''
    unique_name = uuid4().hex
    unique_number = randint(1, 100)
    object_pattern = '<object name="{0}"/>'
    objects_list = [object_pattern.format(
        uuid4().hex) for _ in range(randint(1, 10))]
    return xml_pattern.format(
        unique_name=unique_name,
        unique_number=unique_number,
        objects_list='\n'.join(objects_list),
    )


def create_xmls_in_zips(xmls_cnt: int, zips_cnt: int):
    if not os.path.exists(DIR_NAME):
        os.makedirs(DIR_NAME)
    os.chdir(DIR_NAME)
    for zipfile_num in range(zips_cnt):
        zipfile_name = 'file{0}.zip'.format(zipfile_num)
        zipfile = ZipFile(zipfile_name, mode='w')
        for xmlfile_num in range(xmls_cnt):
            xmlfile_name = 'file{0}.xml'.format(xmlfile_num)
            zipfile.writestr(xmlfile_name, get_random_xml())



if __name__ == '__main__':
    create_xmls_in_zips(XMLFILES_CNT, ZIPFILES_CNT)
