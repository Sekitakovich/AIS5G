from dataclasses import dataclass
from typing import Dict


@dataclass()
class Nation(object):
    name2: str
    name3: str
    # code3: str
    nameJP: str
    nameEN: str


if __name__ == '__main__':

    world: Dict[str, Nation] = {}

    with open('nation.csv', 'rt', encoding='utf-8') as f:
        all = f.read().split('\n')
        id: int = 1
        for line in all:
            if line:
                item = line.split('\t')
                # print(item[:-1])
                name2 = item[0]
                name3 = item[1]
                code3 = item[2]
                jp = item[3]
                en = item[4].replace("'", "''")

                q = "insert into nation(id,name2,name3,code3,jp,en) values(%d,'%s','%s','%s','%s','%s');" % (id,name2,name3,code3,jp,en)
                print(q)
                id += 1

                # code3 = item[2]
                # nation = Nation(name2=item[0], name3=item[1], nameJP=item[3], nameEN=item[4])
                # world[code3] = nation

    # print(world)
