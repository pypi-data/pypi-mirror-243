"""Test ARS et all."""
import json
import os
import ssl
import httpx
import asyncio
import requests
import datetime
import logging
from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List
# We really shouldn't be doing this, but just for now...
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
logging.basicConfig(filename="test_ars.log", level=logging.DEBUG)

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
env_spec = {
    'dev': 'ars-dev',
    'ci': 'ars.ci',
    'test': 'ars.test',
    'prod': 'ars-prod'
}

def get_safe(element, *keys):
    """
    :param element: JSON to be processed
    :param keys: list of keys in order to be traversed. e.g. "fields","data","message","results
    :return: the value of the terminal key if present or None if not
    """
    if element is None:
        return None
    _element = element
    for key in keys:
        try:
            _element = _element[key]
            if _element is None:
                return None
            if key == keys[-1]:
                return _element
        except KeyError:
            return None
    return None

def generate_message(query_type: str, input_curie: str):
    """Create a message to send to Translator services"""

    template_dir = BASE_PATH + "/templates"
    query_type_list = ['treats','treats_creative','upregulate', 'downregulate']

    if query_type in query_type_list:
        predicate = query_type
        with open(template_dir+f'/{predicate}.json') as f:
            template = json.load(f)
            # Fill message template with CURIEs
            query = deepcopy(template)
            nodes = get_safe(query, "message", "query_graph", "nodes")
            for node_val in nodes.values():
                if 'ids' in node_val:
                    node_val['ids'].append(input_curie)
    else:
        logging.error("Unknow Query type")

    return query

async def call_ars(payload: Dict[str,any],ARS_URL: str):
    url = ARS_URL+"submit"
    logging.debug("call_ars")

    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(
            url,
            json=payload,
            timeout=60,
        )
    response.raise_for_status()
    return response.json()

async def test_must_have_curie(ARS_URL: str, query_type: str, expected_output: str, input_curie: str, output_curie: List[str], output_filename: str):
    """" Send Concurrent async queries to ARS and get pass/fail report back  """

    logging.debug("Generating query message for %s" % input_curie)
    message = generate_message(query_type, input_curie)
    logging.debug("query= " + json.dumps(message, indent=4, sort_keys=True))

    children, merged_data, parent_pk, merged_pk = await get_children(message, ARS_URL)
    report_card = await ARS_semantic_analysis(children, parent_pk, output_curie, expected_output, merged_pk, merged_data)

    with open(output_filename, "w") as f:
        json.dump(report_card, f, indent=4)

async def ARS_semantic_analysis(children: List[List], pk: str, output_curie: List[str], expected_output: str, merged_pk: str, merged_data: Dict[str,any]):
    """" function to perform pass fail analysis on individual ARA's results """
    report_card={}
    report_card['pks']={}
    report_card['pks']['parent_pk'] = pk
    report_card['pks']['merged_pk'] = merged_pk
    report_card['results'] = []
    #report_card[pk]['merged_data'] = merged_data
    for idx, out_curie in enumerate(output_curie):
        expect_output = expected_output[idx]
        print(f'analysis for expected_output: {expect_output} for output {out_curie}')
        report={}
        report[out_curie]={}
        for data in children:
            infores = data[0]
            agent = infores.split('-')[1]
            child = data[1]
            child_pk = data[2]
            results = get_safe(child, "fields", "data", "message", "results")
            if results is not None and infores.startswith('ara-'):
                print(f'the length of results is: {len(results)}')
                print(f'analyzing agent: {agent}')
                report_card['pks'][agent] = child_pk
                report = await pass_fail_analysis(report, agent, results, out_curie, expect_output)
                print(f'report before the merge pass/fail analysis {report}')
        #adding the merged data to the report
        ARS_agent = get_safe(merged_data, "fields","name")
        agent = ARS_agent.split('-')[1]
        ARS_results = get_safe(merged_data, "fields", "data", "message", "results")
        report = await pass_fail_analysis(report, agent, ARS_results, out_curie, expect_output)
        print(f'report after the merge pass/fail analysis {report}')
        report_card['results'].append(report)

    return report_card

async def pass_fail_analysis(report: Dict[str,any], agent: str, results: List[Dict[str,any]], out_curie: str, expect_output: str):
    """" function to run pass fail analysis on individual results"""
    print(f'report inside the pass/fail analysis {report}')
    #get the top_n result's ids
    res_sort = sorted(results, key=lambda x: x['normalized_score'], reverse=True)
    all_ids=[]
    for res in res_sort:
        for res_node, res_value in res["node_bindings"].items():
            for val in res_value:
                ids = str(val["id"])
                all_ids_flat = [item for sublist in all_ids for item in sublist]
                if ids not in all_ids_flat:
                    all_ids.append(ids)

    if expect_output == 'TopAnswer':
        n_perc_res = res_sort[0:int(len(res_sort) * (float(10) / 100))]
    elif expect_output == 'Acceptable':
        n_perc_res = res_sort[0:int(len(res_sort) * (float(50) / 100))]
    elif expect_output == 'BadButForgivable':
        n_perc_res = res_sort[int(len(res_sort) * (float(50) / 100)):]
    elif expect_output == 'NeverShow':
        n_perc_res = res_sort
    else:
        logging.error("you have indicated a wrong category for expected output")

    n_perc_ids=[]
    for res in n_perc_res:
        for res_value in res["node_bindings"].values():
            for val in res_value:
                ids=str(val["id"])
                if ids not in n_perc_ids:
                    n_perc_ids.append(ids)

    if expect_output in ['TopAnswer', 'Acceptable','BadButForgivable']:
        if out_curie in n_perc_ids:
            report[out_curie][agent] = 'Pass'
        else:
            report[out_curie][agent] = 'Fail'
    elif expect_output == 'NeverShow':
        if out_curie in n_perc_ids:
            report[out_curie][agent] = 'Fail'
        else:
            report[out_curie][agent] = 'Pass'

    #case where the drug not even in the results
    if out_curie not in all_ids:
        if expect_output in ['TopAnswer', 'Acceptable','BadButForgivable']:
            report[out_curie][agent] = 'Fail'
        elif expect_output == 'NeverShow':
            report[out_curie][agent] = 'Pass'

    return report

async def get_children(query: Dict[str,Any], ARS_URL: str, timeout=None):
    logging.debug("get_children")
    children = []
    response = await call_ars(query, ARS_URL)
    await asyncio.sleep(300)
    parent_pk = response["pk"]
    print(f'the parent pk is {parent_pk}')
    logging.debug("parent_pk for query {}  is {} ".format(query, str(parent_pk)))
    url = ARS_URL + "messages/" + parent_pk + "?trace=y"
    if timeout is None:
        timeout = 60
    async with httpx.AsyncClient(verify=False) as client:
        r = await client.get(
            url,
            timeout=10,
        )
    data = r.json()
    for child in data["children"]:
        agent = child["actor"]["agent"]
        childPk = child["message"]
        logging.debug("---Checking child for " + agent + ", pk=" + parent_pk)
        childData = await get_child(childPk, ARS_URL)
        if childData is None:
            pass
        else:
            # append each child with its results
            children.append([agent, childData, childPk])

    #getting merged data
    print(f'going to get the merged pk')
    merged_pk = data['merged_version']
    print(f'getting merged data for merged_pk:  {merged_pk}')
    merged_data = await get_merged_data(ARS_URL, merged_pk, timeout=60)

    return children, merged_data, parent_pk, merged_pk

async def get_merged_data(ARS_URL: str, merged_pk: str, timeout=120):
    """ function to retrieve completed merged data """
    wait_time=10
    merged_url = ARS_URL + "messages/" + merged_pk
    async with httpx.AsyncClient(verify=False) as client:
        rr = await client.get(
            merged_url,
            timeout=60,
        )
    merged_data = rr.json()
    status = get_safe(merged_data, "fields", "status")
    print(f'the merged_data status is: {status}')
    if status is not None:
        if status == "Done":
            print('the merged data status is finally Done')
            return merged_data
        elif status == 'Running':
            if timeout > 0:
                logging.debug(
                    "Query merged response is still running\n"
                    + "Wait time remaining is now "
                    + str(timeout)
                    + "\n"
                    + "What we have so far is: "
                    + json.dumps(merged_data, indent=4, sort_keys=True)
                )
                await asyncio.sleep(wait_time)
                return await get_merged_data(ARS_URL,merged_pk, timeout - wait_time)
        else:
            print(f"even after timeout {merged_pk} is still Running")
            logging.debug("even after timeout" +merged_pk+ "is still Running") # sorry bud, time's up
            return None

async def get_child(pk: str, ARS_URL: str, timeout=60):
    logging.debug("get_child(" + pk + ")")
    wait_time = 10  # amount of seconds to wait between checks for a Running query result
    url = ARS_URL + "messages/" + pk
    async with httpx.AsyncClient(verify=False) as client:
        child_response = await client.get(
            url,
            timeout=10.0
        )
    data = child_response.json()
    status = get_safe(data, "fields", "status")
    result_count = get_safe(data, "fields", "result_count")
    if status is not None:
        if status == "Done" and result_count is not None:
            if  result_count > 0:
                logging.debug("get_child for " +pk+ "returned"+ str(result_count )+"results")
                return data
            elif result_count == 0:
                logging.debug("get_child for " +pk+ "returned 0 results")
                return None
        elif status == "Running":
            if timeout > 0:
                logging.debug(
                    "Query response is still running\n"
                    + "Wait time remaining is now "
                    + str(timeout)
                    + "\n"
                    + "What we have so far is: "
                    + json.dumps(data, indent=4, sort_keys=True)
                )
                await asyncio.sleep(wait_time)
                return await get_child(pk, ARS_URL, timeout - wait_time)
            else:
                logging.debug("even after timeout" +pk+ "is still Running") # sorry bud, time's up
                return None
        else:
            # status must be some manner of error
            logging.debug(
                "Error status found in get_child for "
                + pk
                + "\n"
                + "Status is "
                + status
                + "\n"
                + json.dumps(data, indent=4, sort_keys=True)
            )
            return None
    else:
        # Should I be throwing an exception here instead?
        logging.error("Status in get_child for " + pk + " was no retrievable")
        logging.error(json.dumps(data, indent=4, sort_keys=True))
    # We shouldn't get here
    logging.error("Error in get_child for \n" + pk + "\n No child retrievable")
    return None


def run_semantic_test(env: str, query_type: str, expected_output: str, input_curie: List[str], output_curie: List[str]):
    
    ars_env = env_spec[env]
    ARS_URL = f'https://{ars_env}.transltr.io/ars/api/'
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    output_filename = f"ARS_smoke_test_{timestamp}.json"
    asyncio.run(test_must_have_curie(ARS_URL, query_type, expected_output, input_curie, output_curie,output_filename))




# if __name__ == "__main__":
#     ARS_URL = 'https://ars.test.transltr.io/ars/api/'
#     query_type = 'treats_creative'
#     expected_output = 'TopAnswer'
#     input_curie = 'MONDO:0015564'
#     output_curie = ['PUBCHEM.COMPOUND:5284616','UNII:4F4X42SYQ6']
#
#     timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
#     output_filename = f"ARS_smoke_test_{timestamp}.json"
#
#     for out_curie in output_curie:
#         asyncio.run(test_must_have_curie(ARS_URL, query_type, expected_output, input_curie, out_curie,output_filename))
#     with open(output_filename, 'w') as f:
#         json.dump(output, f, indent=2)

    #print(report_cards)
