import csv
import json
import pdb
import pickle
import sys
import os
import pdb

src = sys.argv[1] # input from 'train','test_freq','test_rare','valid_freq','valid_rare'
conversations = json.load(open(os.path.join('../../alexa-prize-topical-chat-dataset/conversations',src+'.json')))
reading_sets = json.load(open(os.path.join('../../alexa-prize-topical-chat-dataset/reading_sets/post-build',src+'.json')))
writer = csv.writer(open('./data/flat_data_'+src+'.tsv', 'wt', newline='\n'), delimiter='\t')

header = ['conv_id', 'i', 'agent', 'utt', 'knowledge_sources', 'knowledge_strs', 'entities' ]
writer.writerow(header)

for conv_id, conversation in conversations.items():
    for i, turn in enumerate(conversation['content']):
        agent = turn['agent']
        utt = turn['message']

        # get knowledge strings
        knowledge_base = reading_sets[conv_id]
        knowledge_sources = turn['knowledge_source']

        knowledge_strs = []
        entities = []
        
        article_source = []
        fun_fact_source = []
        for source in knowledge_sources:
            if source.startswith('FS'):
                fun_fact_source.append(source)
            if source.startswith('AS'):
                article_source.append(source)

        if fun_fact_source!=[]:
            k = None
            e = None
            for source in fun_fact_source:
                #TODO:k is reading meterials that the utterance is using but here, k should not choose [int(source[-1])] fun_fact. it should choose all fun fact or select using other methods. 
                k = knowledge_base[agent][source]['fun_facts'][int(source[-1])]
                e = [knowledge_base[agent][source]['entity']]
                entities = entities+e
                knowledge_strs.append(k)
        elif article_source!=[]:
            k = None
            e = None
            e = [ r['entity'] for r in knowledge_base[agent].values()  ]
            entities = entities+e
            for source in article_source:
                k = knowledge_base['article'][source]
                knowledge_strs.append(k)
        else:
            e = [ r['entity'] for r in knowledge_base[agent].values()   ]
            entities = entities + e
            k = None
        #for source in knowledge_sources:
        #    if source == 'Personal Knowledge':
        #        pass
        #    if source.startswith('FS'):
        #        k = knowledge_base[agent][source]['fun_facts'][int(source[-1])]
        #        e = [knowledge_base[agent][source]['entity']]
        #    if source.startswith('AS'):
        #        k = knowledge_base['article'][source]
        #        e = [ r['entity'] for r in knowledge_base[agent].values() ]
        #    entities = entities+e
        #    #entities.append(e)
        #    knowledge_strs.append(k)
        if entities!=[]:
            #entities = list(set(entities)).sort()
            if len(entities)!=len(set(entities)):
                pdb.set_trace()

        row = [ conv_id, i, agent, utt, json.dumps(knowledge_sources), json.dumps(knowledge_strs), json.dumps(entities) ]
        writer.writerow(row)
