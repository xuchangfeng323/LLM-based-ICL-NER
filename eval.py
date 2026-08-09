from data_process import get_prompt, get_eval_data
from get_response import get_deeppseek_response
from utils import Metrics, Argument
class Evaluator: 
    def __init__(self, args):
        self.model_name = args.model_name
        self.prompt = args.prompt
        self.system_prompt = get_prompt(k=0,data_dir="./data",system_prompt=args.prompt)
       
        self.metrics = Metrics()
    def evaluate(self, eval_data):
        for item in eval_data:
            id = item['id']
            text = item['text']
            entities = item['entities']
            response = get_deeppseek_response(self.model_name, self.system_prompt, text)
            print(id)
            print(response)
            print(id)
        
if __name__ == "__main__":
    args = Argument(args_path="./args/config.json")
    evaluator = Evaluator(args)
    eval_data=get_eval_data(data_dir="./data",data_num=1)
    evaluator.evaluate(eval_data)
            