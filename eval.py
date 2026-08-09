import json
from data_process import get_prompt, get_eval_data
from get_response import get_deeppseek_response
from utils import Metrics, Argument
class Evaluator: 
    def __init__(self, args):
        self.model = args.model
        self.prompt = args.prompt
        self.system_prompt = get_prompt(k=0,data_dir="./data",system_prompt=args.prompt)
        self.model_name = args.model_name
        self.metrics = Metrics()
        self.responses_map = {
            "deepseek":get_deeppseek_response,
        }
        self.model_fn = self.responses_map[self.model]
    def evaluate(self, eval_data):
        for item in eval_data:
            id = item['id']
            text = item['text']
            entities = item['entities']
            response = self.model_fn(self.model_name, self.system_prompt, text)
            print(json.dumps(json.loads(response)["entities"], indent=2))
            print(len(entities))
        
if __name__ == "__main__":
    args = Argument(args_path="./args/config.json")
    evaluator = Evaluator(args)
    eval_data=get_eval_data(data_dir="./data",data_num=1)
    evaluator.evaluate(eval_data)
            