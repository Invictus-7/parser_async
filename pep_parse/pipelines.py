import csv
import datetime as dt

from pep_parse.settings import BASE_DIR

time_format = dt.datetime.now().strftime('%m-%d-%Y_%H-%M-%S')

QTY_DIC = {
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
        count = QTY_DIC[extraction]
        count += 1
        QTY_DIC[extraction] = count

        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        results.extend(QTY_DIC.items())
        total = 0
        for value in QTY_DIC.values():
            total += int(value)
        results.append(('Total', total))

        with open(f'{BASE_DIR}/results/status_summary_{time_format}.csv',
                  'w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            f.write('Статус, Количество\n')
            writer.writerows(results)
