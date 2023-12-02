import json
import arxiv

client = arxiv.Client()

with open('data/arxiv.jsonl', 'r') as file:
    for line in file:
        data = json.loads(line)
        search_by_id = arxiv.Search(id_list=[t['id'] for t in data['references']])
        data['references'] = [ref.title for ref in list(client.results(search_by_id))]
        try:
            updated_data_small = 'ID: ' + data['id'] + '\nTITLE: ' + data['title'] + '\nSOURCE: ' + data['source'] +\
        '\nAUTHORS: ' + ', '.join(data['authors']) + '\nCATEGORIES: ' + ', '.join(data['categories']) + '\nSUMMARY: ' + data['summary'] +\
        '\nREFERENCES: ' + ', '.join(data['references']) +'\nPUBLISHED: ' + data['published'] +\
        '\nUPDATED: ' + data['updated']
            updated_data_large = updated_data_small + '\nCONTENT: ' + data['content']
            with open('data/small/' + data['id'] + '.txt', 'w') as f:
                f.write(updated_data_small)
        except:
            pass
        # with open('data/large/' + data['id'] + '.txt', 'w') as f:
        #    f.write(updated_data_large)