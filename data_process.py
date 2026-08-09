import os
import json
def get_k_shot_data(k=0,data_dir="./data"):
    if k <0:
        raise ValueError("k must be greater than 0")
    elif k == 0:
        return ''
    else:
        with open(os.path.join(data_dir, f"CDR_TrainingSet.PubTator.txt"), 'r', encoding='utf-8') as f:
            data = f.read()
            blocks=data.strip().split('\n\n')
            blocks=[b for b in blocks if b.strip()]
            k_shot_prompt='Here are some examples of the data:\n'
            examples=[]
            for i in range(k):

                lines=blocks[i].strip().split('\n')
              
                title=lines[0]
                abstract=lines[1]
                entities=[]
                title=title.split('|')[2]
                abstract=abstract.split('|')[2]
                text=title+' '+abstract
                
                for line in lines[2:]:
                    parts=line.split('\t')
                    if len(parts) < 5:
                        continue
                    
                    if  (parts[4] == 'Chemical' or parts[4] == 'Disease'):
                        entity={
                            
                            "entity_type": parts[3],
                        
                            "entity_text": parts[4]
                        }
                        entities.append(entity)
                examples.append({'text':text,'entities':entities})

        return k_shot_prompt+json.dumps(examples,ensure_ascii=False)[1:-1]

def get_eval_data(data_dir="./data",data_num=500):
    with open(os.path.join(data_dir, f"CDR_TrainingSet.PubTator.txt"), 'r', encoding='utf-8') as f:
            data = f.read()
            blocks=data.strip().split('\n\n')
            blocks=[b for b in blocks if b.strip()]
            
            examples=[]
            for i in range(data_num):

                lines=blocks[i].strip().split('\n')
              
                title=lines[0]
                abstract=lines[1]
                entities=[]
                title=title.split('|')[2]
                abstract=abstract.split('|')[2]
                text=title+' '+abstract
                
                for line in lines[2:]:
                    parts=line.split('\t')
                    if len(parts) < 5:
                        continue
                    
                    if  (parts[4] == 'Chemical' or parts[4] == 'Disease'):
                        entity={
                            
                            "entity_type": parts[3],
                        
                            "entity_text": parts[4]
                        }
                        entities.append(entity)
                examples.append({'text':text,'entities':entities})
    return examples



                        
                
if __name__ == "__main__":
    prompt=get_k_shot_data(k=2,data_dir="./data")
    eval_data=get_eval_data(data_dir="./data",data_num=500)
    print(eval_data[0])
            

        
    