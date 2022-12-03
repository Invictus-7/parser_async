import csv
import datetime as dt

from pep_parse.settings import BASE_DIR

PEP_STATUSES_COUNT_DIC = {
    'Accepted': 0,
    'Active': 0,
    'Deferred': 0,
    'Draft': 0,
    'Final': 0,
    'Provisional': 0,
    'Rejected': 0,
    'Superseded': 0,
    'Withdrawn': 0
}

results = []


class PepParsePipeline:

    def process_item(self, item, spider):
        extraction = item['status']
        try:
            count = PEP_STATUSES_COUNT_DIC[extraction]
            count += 1
            PEP_STATUSES_COUNT_DIC[extraction] = count
        except KeyError:
            print(f'В словарь {PEP_STATUSES_COUNT_DIC} поступил'
                  f'непредусмотренный ключ')

        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        results.extend(PEP_STATUSES_COUNT_DIC.items())
        total = sum(PEP_STATUSES_COUNT_DIC.values())
        results.append(('Total', total))

        with open(f'{BASE_DIR}/results/status_summary_'
                  f'{dt.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")}.csv',
                  'w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            f.write('Статус, Количество\n')
            writer.writerows(results)
