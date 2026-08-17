import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from data_process import get_prompt, get_eval_data
from get_response import get_deepseek_response, get_gpt_response, get_qwen_response, get_ollama_response, get_mimo_response
from utils import Metrics, Argument
import json_repair
import os
class Evaluator: 
    def __init__(self, args):
        self.args = args
        self.model = args.model
        self.prompt = args.prompt
        self.system_prompt = get_prompt(k=args.k_shot,data_dir="./data",system_prompt=args.prompt)
        print(self.system_prompt)
        print("-"*150)
        self.model_name = args.model_name
        self.metrics = Metrics(target_class=args.target_class)
        self.responses_map = {
            "deepseek":get_deepseek_response,
            "openai":get_gpt_response,
            "qwen":get_qwen_response,
            "ollama":get_ollama_response,
            "mimo":get_mimo_response,
        }
        self.model_fn = self.responses_map[self.model]
    def evaluate_item(self, item):
            try:
                id = item['id']
                text = item['text']
                entities = item['entities']
                response = self.model_fn(self.model_name, self.system_prompt, text)
                response_repair=json_repair.loads(response)
                entities_pred=response_repair["entities"]
                # print("pred")
                # print(entities_pred)
                # print("true")
                # print(entities)
                self.metrics.add({"id":id,"true_labels":entities,"pred_labels":entities_pred})
            except:
                print(item)
    def evaluate(self, eval_data):
        with ThreadPoolExecutor(max_workers=self.args.num_workers) as executor:
            futures= [executor.submit(self.evaluate_item, item) for item in eval_data]
            for future in tqdm(as_completed(futures), desc="Evaluating", total=len(futures)):
                future.result()
        result=self.metrics.calculate()
        output_data={
            "args":self.args.args_dict,
            "result":result,
        }
        out_filename=f"{self.args.model}-{self.args.model_name}-{self.args.k_shot}shot-{self.args.data_num}data.json"
        os.makedirs(self.args.output_dir, exist_ok=True)
        with open(os.path.join(self.args.output_dir, out_filename), "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)

        return result
        
        
if __name__ == "__main__":
    args = Argument(args_path="./args/config.json")
    evaluator = Evaluator(args)
    eval_data=get_eval_data(data_dir="./data",data_num=args.data_num )
    result=evaluator.evaluate(eval_data)
    print(result)
            