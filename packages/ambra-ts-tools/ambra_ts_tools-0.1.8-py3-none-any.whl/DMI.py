# %pip install ambra-ts-tools --upgrade
from ambra_ts_tools.Ambra_Clone.V2.ambra_environment import ambra_environment
from ambra_ts_tools.authenticate_ambra import authenticate_ambra
import os
import pandas as pd
import __main__ as main
# from google.colab import userdata
from ambra_ts_tools.runner import runner
import json
from tqdm import tqdm
import concurrent.futures
from multiprocessing.pool import ThreadPool
from functools import partial

# from google.colab import drive

# drive.mount('/content/drive')
study_data_params = {}

# def multiprocess_ambra_request(env,func,iter,threads=30,pbar = False):
#         if len(iter) < threads:
#             threads = len(iter)
#             if threads == 0:
#                 return []
#         # func = partial(env.handle_ambra_request,endpoint)
#         p = ThreadPool(threads)
#         if pbar == True:
#             threaded_response = list(tqdm(p.imap(func,iter),total=len(iter)))
#         else:
#             threaded_response = list(p.map(func,iter))
#         return threaded_response

def get_schema(study):
    
    schema = env.handle_ambra_request("host/{engine_fqdn}/api/v3/storage/study/{storage_namespace}/{study_uid}/schema?sid={sid}&phi_namespace={phi_namespace}".format(**study,sid=sid),data={},request_type="GET")
    try:
        output = []
        for series in schema['series']:
            output.append([study['study_uid'], series['series_uid'], len(series['images']),study['uuid']])
    except Exception as e:
        output = [[study['study_uid'], None, None,study['uuid']]]
    return output




##RUN multi-threaded script
if __name__ == '__main__':
    for i in ["2","4","5","6","7","8","9"]:
        sid = authenticate_ambra(username="ethan.york@intelerad.com",password=os.getenv('AMBRA_PASSWORD'))
        print(sid)
        url = "https://access.ambrahealth.com"
        env = ambra_environment(url=url, sid=sid)
        flat_result = []
        study_data = pd.read_csv(r"G:\Shared drives\Ambra\Professional Services\Technical Services\Python Notebooks\Customer Notebooks\Spectrum Health\study_lists\study_data"+i+".csv")
        p = ThreadPool(10)
##RUN multi-threaded script

# Create a ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Use the executor to map the function to each study in study_data
            results = list(tqdm(executor.map(get_schema, (row._asdict() for row in study_data.itertuples())),total=len(study_data)))
            flat_result = []
            for study in results:
                for series in study:
                    if isinstance(series, tuple):        
                        flat_result.append(list(series))
                    else:
                        flat_result.append(series)

        result = pd.DataFrame(flat_result,columns=["study_uid","series_uid","image_count","uuid"])
        result.to_csv(r"G:\Shared drives\Ambra\Professional Services\Technical Services\Python Notebooks\Customer Notebooks\Spectrum Health\study_lists\DMI_study_data"+i+".csv")
        del flat_result
        del study_data
        # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     # Use the executor to map the function to each study in study_data
    #     results = list(tqdm(executor.map(get_schema, (row._asdict() for row in study_data.itertuples())),total=len(study_data)))

    # flat_result = []
    # for study in threaded_response:
    #     for series in study:
    #         if isinstance(series, tuple):
    #             flat_result.append(list(series))
    #         else:
    #             flat_result.append(series)

    result = pd.DataFrame(flat_result,columns=["study_uid","series_uid","image_count","uuid"])
    result.to_csv(r"G:\Shared drives\Ambra\Professional Services\Technical Services\Python Notebooks\Customer Notebooks\Spectrum Health\study_lists\DMI_study_data"+i+".csv")
