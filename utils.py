import os
import json
class Argument:
    def __init__(self, args_path):
        self.args_dict = self._load_json_config(args_path)
        for key, value in self.args_dict.items():
            setattr(self, key, value)

    def _load_json_config(self, args_path):
        if os.path.exists(args_path):
            with open(args_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            raise FileNotFoundError(f"Config file not found: {config_path}")
class Metrics:
    def __init__(self, target_class=["Chemical","Disease"]):
        self.target_class = target_class
        self.metrics = {}
        for cls in self.target_class:
            self.metrics[cls] = {
                "true_labels":Counter(),
                "pred_labels":Counter(),
            }
    def add(self,item):
        id=item['id']
        true_labels=item['true_labels']
        pred_labels=item['pred_labels']
        for true_label in true_labels:
            entity_class = true_label['type']
            if entity_class in self.target_class:
                entity_name=true_label['entity_name']
                key=(id,entity_name)
                self.metrics[entity_class]['true_labels'][key] += 1
        for pred_label in pred_labels:
            entity_class = pred_label['type']
            if entity_class in self.target_class:
                entity_name=pred_label['entity_name']
                key=(id,entity_name)
                self.metrics[entity_class]['pred_labels'][key] += 1
    def calculate(self):
        result={}
        for cls in self.target_class:
            
            true_labels=self.metrics[cls]['true_labels']
            pred_labels=self.metrics[cls]['pred_labels']
            tp=len(true_labels&pred_labels)
            p=tp/len(pred_labels)
            r=tp/len(true_labels)
            f1=2*p*r/(p+r)
            result.update({cls:{"tp":tp,"p":p,"r":r,"f1":f1,"support":len(true_labels)} })
        print(result)
                
        



            
        


