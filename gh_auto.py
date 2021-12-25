from autoscraper import AutoScraper
url='https://github.com/saidineshpola/finetuning-hf-gpt6b/'
wanted_list=['deepspeed']
scraper=AutoScraper()
result=scraper.build(url,wanted_list)
print(result)