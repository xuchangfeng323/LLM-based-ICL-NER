import os
import json
def get_prompt(k=0,data_dir="./data",system_prompt=""):
    if k <0:
        raise ValueError("k must be greater than 0")
    elif k == 0:
        return system_prompt
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
                            
                            "entity": parts[3],
                            "type": parts[4]
                        }
                        entities.append(entity)
                examples.append({'text':text,'entities':entities})

        return system_prompt+k_shot_prompt+json.dumps(examples,ensure_ascii=False)[1:-1]

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

                title_list=title.split('|')
                abstract_list=abstract.split('|')
                id=title_list[0]
                text=title_list[2]+' '+abstract_list[2]
                
                for line in lines[2:]:
                    parts=line.split('\t')
                    if len(parts) < 5:
                        continue
                    
                    if  (parts[4] == 'Chemical' or parts[4] == 'Disease'):
                        entity={
                            "entity": parts[3],
                            "type": parts[4]
                        }
                        entities.append(entity)
                examples.append({'id':id,'text':text,'entities':entities})
    return examples



                        
                
if __name__ == "__main__":
    
    eval_data=get_eval_data(data_dir="./data",data_num=500)
    print(eval_data[0])
            

        
    