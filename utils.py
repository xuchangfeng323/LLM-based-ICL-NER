import os
import json
from collections import Counter
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
                entity_name=true_label['entity_name'].lower()
                key=(id,entity_name)
                self.metrics[entity_class]['true_labels'][key] += 1
        for pred_label in pred_labels:
            entity_class = pred_label['type']
            if entity_class in self.target_class:
                entity_name=pred_label['entity_name'].lower()
                key=(id,entity_name)
                self.metrics[entity_class]['pred_labels'][key] += 1
    def calculate(self):
        result={}
        all_tp=0
        all_pred_sum=0
        all_true_sum=0
        macro_p=0
        macro_r=0
        macro_f1=0
        for cls in self.target_class:
            
            true_labels=self.metrics[cls]['true_labels']
            pred_labels=self.metrics[cls]['pred_labels']
            tp=sum((true_labels&pred_labels).values())
            pred_sum = sum(pred_labels.values())
            true_sum = sum(true_labels.values())
            all_tp+=tp
            all_pred_sum+=pred_sum
            all_true_sum+=true_sum
            p = tp / pred_sum if pred_sum > 0 else 0
            r = tp / true_sum if true_sum > 0 else 0
            f1 = 2 * p * r / (p + r) if (p + r) > 0 else 0
            macro_p+=p
            macro_r+=r
            macro_f1+=f1
            result.update({cls:{"tp":tp,"p":p,"r":r,"f1":f1,"support":true_sum} })
        
        p_micro = all_tp / all_pred_sum if all_pred_sum > 0 else 0
        r_micro = all_tp / all_true_sum if all_true_sum > 0 else 0
        f1_micro = 2 * p_micro * r_micro / (p_micro + r_micro) if (p_micro + r_micro) > 0 else 0
        result.update({"micro":{"p":p_micro,"r":r_micro,"f1":f1_micro,"support":all_true_sum}})
        
        n = len(self.target_class)
        result.update({"macro":{"p":macro_p/n,"r":macro_r/n,"f1":macro_f1/n,"support":all_true_sum}})
        return result
                
        



            
        


