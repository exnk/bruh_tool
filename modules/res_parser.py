from modules.models import CVE
import os


class ResultParser:

    def __init__(self, cve_result: str):
        self.__cve_result = cve_result
        self.__get_cves()
        self.result = []
        self.source_models: list[CVE] = []

    def __get_cves(self):
        res = self.__cve_result.find('[+]')
        self.__cve_result = self.__cve_result[res:]

    @staticmethod
    def __make_json(attributes: list) -> dict:

        data = {}
        for item in attributes:
            item_parts = item.split(':', maxsplit=1)
            data.update({item_parts[0].strip(): item_parts[1].strip()})
        return data

    def convert_cve_to_model(self):
        cves = list(filter(lambda x: x != '', self.__cve_result.split('[+]')))
        for cve in cves:
            cve_info = list(map(lambda x: x.strip(), cve.split('\n   ')))
            res = self.__make_json(cve_info[1:])
            cve_basic = cve_info[0].split(' ', maxsplit=1)
            cve_basic[0] = cve_basic[0][cve_basic[0].find("m[")+2: cve_basic[0].find("]")].replace('.c', '')

            data = {'name': cve_basic[1],
                    'cve_name': cve_basic[0],
                    'attributes': res}
            model = CVE(**data)
            if os.path.exists(f'./cve_repo/{cve_basic[0]}.c'):
                model.source = f'./cve_repo/{cve_basic[0]}.c'
                self.source_models.append(model)
            print(model.cve_name, model.attributes.download)
            self.result.append(model)
